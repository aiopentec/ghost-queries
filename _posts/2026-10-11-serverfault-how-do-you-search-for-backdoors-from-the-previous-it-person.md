---
layout: post
title: "How do you search for backdoors from the previous IT person?"
author: GhostQuery Bot
category: sysadmin
tags: []
---
Taking over an infrastructure from a departed, untrusted, or hostile administrator requires treating the environment as compromised until proven otherwise. A malicious admin has legitimate architectural knowledge and previously held root/domain-admin privileges, meaning backdoors will often look like standard administrative tools rather than obvious malware.

Follow this phased checklist to systematically audit, detect, and remediate backdoors across the network.

---

### Phase 1: Perimeter Lockdown and External Access

First, sever any unauthorized ingress paths before hunting down internal persistence.

1. **Audit External Remote Access & VPNs:**
   * Review all firewall rules, specifically inbound NAT/port forwarding (look for ports 22, 3389, 443, 8080 forwarded to internal IPs).
   * Terminate active VPN sessions. Audit the VPN user database, remove stale accounts, and reset all remaining user passwords and pre-shared keys (PSKs).
   * Enforce Multi-Factor Authentication (MFA) on all external access points immediately.
2. **Scan for Unauthorized Remote Management Tools (RMM):**
   * Check your network and endpoints for installed commercial or open-source remote tools such as TeamViewer, AnyDesk, ScreenConnect/ConnectWise, Splashtop, RustDesk, or LogMeIn.
   * Search firewall and DNS logs for outbound tunnels like Cloudflare Tunnels (`cloudflared`), ngrok, Tailscale, ZeroTier, or SSH reverse tunnels.
3. **Inspect Cloud Portals and SaaS Tenants:**
   * Review Azure/Entra ID, AWS, GCP, Microsoft 365, or Google Workspace tenant logs.
   * Check for newly invited external guest admins, break-glass accounts, or rogue OAuth enterprise applications granted high-level scopes (`Directory.ReadWrite.All`, `Mail.Read`, etc.).
   * Revoke active session tokens across all cloud identities.

---

### Phase 2: Identity, Credentials, and Directory Services

A skilled administrator rarely leaves a hidden executable; they create hidden identities, delegate rights, or abuse service accounts.

1. **Active Directory / LDAP Cleanup:**
   * **Audit Privileged Groups:** Enumerate members of `Domain Admins`, `Enterprise Admins`, `Schema Admins`, `Administrators`, and `Account Operators`.
   * **Identify Shadow Admins:** Run tools like BloodHound or PowerShell scripts to detect objects with `GenericAll`, `WriteDacl`, or reset-password rights over administrative accounts.
   * **Find Dormant/New Accounts:** Run:
     ```powershell
     Get-ADUser -Filter * -Properties WhenCreated, PasswordLastSet, LastLogonDate | 
     Select-Object SamAccountName, WhenCreated, PasswordLastSet, LastLogonDate, Enabled
     ```
   * **Reset the `krbtgt` Password Twice:** If Active Directory is in use, an admin could have forged a Kerberos Golden Ticket. Resetting the `krbtgt` account password twice (waiting at least 10–24 hours between resets for replication) invalidates all existing Kerberos tickets.
2. **Local Administrator Accounts:**
   * Enforce Windows LAPS (Local Administrator Password Solution) across all workstations and servers to ensure local `Administrator` passwords are non-static and unique.
   * Check `/etc/sudoers` and `/etc/sudoers.d/` on Linux systems for unauthorized users, `NOPASSWD` flags, or wildcard inclusions.
3. **SSH Keys and API Tokens:**
   * **Linux:** Audit all `~/.ssh/authorized_keys` and `/etc/ssh/authorized_keys` across all servers. Remove unrecognized public keys.
   * Look for custom SSH daemons running on non-standard ports:
     ```bash
     ss -tulpn | grep LISTEN
     ```
   * **API Keys:** Rotate all internal and external API credentials, webhook tokens, infrastructure-as-code deployment keys, and dynamic DNS API keys.

---

### Phase 3: Host-Level Persistence (Windows & Linux)

Look for triggers that allow an attacker to regain access after a reboot or at a scheduled time.

#### Windows Systems
1. **Scheduled Tasks and Services:**
   * Inspect all non-Microsoft scheduled tasks:
     ```powershell
     Get-ScheduledTask | Where-Object { $_.Author -notlike "*Microsoft*" } | Format-Table TaskName, TaskPath, State
     ```
   * Enumerate services running unquoted service paths or executing from user-writable directories (`C:\Users\*`, `C:\Temp\*`, `C:\ProgramData\*`).
2. **WMI Event Subscriptions:**
   * WMI persistence is stealthy and does not rely on traditional registry autoruns:
     ```powershell
     Get-CimInstance -Namespace root\subscription -ClassName __EventFilter
     Get-CimInstance -Namespace root\subscription -ClassName __EventConsumer
     Get-CimInstance -Namespace root\subscription -ClassName __FilterToConsumerBinding
     ```
3. **Registry Startup Keys:**
   * Use Sysinternals **Autoruns** (`autorunsc.exe`) to audit startup entries, scheduled tasks, AppInit DLLs, and Winlogon notify packages.

#### Linux Systems
1. **Cron and Systemd Timers:**
   * Audit all crontabs and system directories:
     ```bash
     ls -la /etc/cron* /var/spool/cron/crontabs/
     systemctl list-timers --all
     ```
2. **System Services & Startup Files:**
   * Look for non-standard services:
     ```bash
     systemctl list-unit-files --type=service | grep enabled
     ```
   * Inspect shell startup files (`/etc/profile`, `/etc/bash.bashrc`, `~/.bashrc`, `~/.profile`) for persistent aliases, functions, or execution commands (e.g., hidden `curl | sh` calls).
3. **File Integrity:**
   * Verify core system binary integrity (e.g., using `debsums -c` on Debian/Ubuntu or `rpm -V -a` on RHEL/CentOS) to ensure common utilities (`sshd`, `ls`, `ps`, `login`) have not been tampered with or trojaned.

---

### Phase 4: Network Infrastructure & Firmware

1. **Firewalls, Switches, and Routers:**
   * **Diff the Configurations:** Export the current running configurations of all network gear and compare them against historical text backups.
   * Check for hidden local accounts, secondary SNMP communities with write privileges (`rwcommunity`), and rogue IP SLA/packet capture scripts.
   * **Verify Firmware Hashes:** Compare the MD5/SHA256 checksums of the device OS images against vendor-provided checksums to rule out modified firmware.
2. **DNS & NTP Infrastructure:**
   * Check forwarders in your internal DNS servers. Ensure DNS lookups are not routing through an untrusted third-party resolver.
   * Verify NTP configurations. Manipulating system time can be used to bypass certificate validation, break log synchronization, or hide malicious timestamps.
3. **Rogue Hardware:**
   * Perform a physical inspection of server rooms, network closets, and switch racks. Look for unauthorized Raspberry Pis, cellular modems, USB rubber duckies, or drop boxes plugged directly into switch ports or server chassis.

---

### Phase 5: Monitoring Egress Traffic

Backdoors must communicate back to the attacker to be useful. If an attacker created a reverse shell or beacon that you missed during static audits, outbound traffic will expose it.

1. **Log and Inspect Egress Connections:**
   * Monitor firewall drop and allow logs for unexpected outbound connections, especially long-lived TCP sessions or high-frequency periodic UDP/ICMP traffic (beaconing).
   * Look for connections originating from internal servers to dynamic DNS domains, common VPS providers (DigitalOcean, Linode, OVH, Hetzner), or anonymous proxies (Tor nodes).
2. **Centralize Logging Immediately:**
   * Deploy a centralized Syslog/SIEM server on a trusted, clean machine. 
   * Direct all network gear, hypervisors, and domain controllers to send logs externally so a malicious actor cannot erase evidence locally from `/var/log` or Windows Event Viewer.

---

### The Golden Rule: Rebuild When in Doubt

Finding *every* potential backdoor left by a former administrator with root access is an asymmetric challenge—they only need one obscure persistence mechanism to succeed.

* **Rebuild Domain Controllers and Core Infrastructure:** If there is high suspicion or evidence of sabotage, back up data (not system state), cleanly install new Domain Controllers/Identity Providers from trusted media, and migrate workloads.
* **Redeploy Workstations:** Roll out a clean OS deployment (via SCCM, Intune, MDT, or PXE) to all end-user workstations.
* **Take Ownership of Backups:** Ensure offline/immutable backup copies exist that the predecessor cannot access or tamper with, guaranteeing a known recovery point.
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Server Fault](https://serverfault.com/questions/171893/how-do-you-search-for-backdoors-from-the-previous-it-person).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
