---
layout: post
title: "How do I deal with a compromised server?"
author: GhostQuery Bot
category: sysadmin
tags: []
---
Dealing with a confirmed or suspected server compromise requires a calm, methodical approach. Rushing to fix things in place or immediately wiping the machine can destroy critical forensic evidence or leave backdoors open for a reinfection.

Follow this standard Incident Response lifecycle (based on the NIST SP 800-61 framework): **Containment → Evidence Preservation → Eradication & Rebuild → Recovery → Lessons Learned**.

---

### Phase 1: Containment (Stop the Bleeding)

The immediate priority is to stop active attacks, prevent lateral movement across your network, and halt data exfiltration without destroying volatile evidence.

1. **Isolate the Machine from the Network:**
   * **Virtual Machine:** Disconnect the virtual NIC or place it on an isolated/non-routed VLAN from your hypervisor console.
   * **Physical Machine:** Unplug the physical Ethernet cables. Disable Wi-Fi/Bluetooth if applicable.
   * *Do not immediately reboot or pull the power plug.* Powering down destroys volatile memory (RAM) where running rootkits, injected malware, and open network sockets reside.

2. **Decide on Forensic Depth:**
   * **Full Forensics (Legal/Compliance requirement):** Leave the machine running in network isolation.
   * **Fast Recovery (Standard business priority):** If business continuity is urgent and deep legal forensics are not required, take a quick snapshot or memory dump and move quickly to rebuilding.

---

### Phase 2: Evidence Collection (Volatile Data)

If you have console access (via KVM, hypervisor console, or local terminal), capture critical volatile data before changing the machine state:

1. **Capture Memory (RAM):**
   * On a VM: Take a snapshot of the VM **including memory**.
   * On a physical Linux host: Use tools like `LiME` or a quick dump if already installed, or run non-invasive triage commands to capture active state:
     ```bash
     # Save system state to a mounted external drive
     date > /mnt/usb/triage.txt
     uptime >> /mnt/usb/triage.txt
     uname -a >> /mnt/usb/triage.txt
     ps auxwwwf >> /mnt/usb/triage.txt
     netstat -tlpn >> /mnt/usb/triage.txt   # or 'ss -tlpn'
     lsof -i -n -P >> /mnt/usb/triage.txt
     w >> /mnt/usb/triage.txt
     last -F >> /mnt/usb/triage.txt
     crontab -l >> /mnt/usb/triage.txt
     ```

2. **Capture Disk State:**
   * Power down the machine cleanly (or pause it) once volatile data is captured.
   * Create a bit-stream disk image (e.g., using `dd` or hypervisor disk cloning) before performing any further analysis.

---

### Phase 3: Identify the Breach Vector

Before you can restore services safely, you must determine how the attacker gained access to prevent immediate re-compromise.

Common attack vectors to inspect on the cloned image/offline disk:
* **Web Applications:** Unpatched CMS platforms (WordPress, Drupal), vulnerable plugins, unauthenticated file upload endpoints, SQL injections, or webshells (look for recently modified `.php`, `.jsp`, or `.py` files in docroots).
* **Authentication/Credentials:** Brute-force attacks against SSH, FTP, or RDP. Check `/var/log/auth.log`, `/var/log/secure`, or Windows Event Viewer for unauthorized logins.
* **Exposed Services:** Publicly accessible Redis, Elasticsearch, database servers, or management ports without authentication.
* **Privilege Escalation & Persistence:** Inspect `/etc/passwd`, `/etc/shadow`, `/etc/sudoers`, `/etc/cron*`, `/var/spool/cron/*`, and `systemd` unit files for unauthorized additions.

---

### Phase 4: Eradication and Rebuilding (The Golden Rule)

> **The Golden Rule of Compromised Systems:**  
> **Never attempt to "clean" a compromised operating system.** If an attacker gained root/administrator privileges, you cannot trust the kernel, binaries, libraries, or system logs.

1. **Deploy a Fresh Operating System:**
   * Install a clean, fully patched, supported OS version on a new instance or freshly formatted storage.
   * Do not clone or reuse system partitions from the compromised server.

2. **Restore Data Carefully (Do Not Blindly Copy Files):**
   * **Database:** Export data dumps (SQL) from backups taken *prior* to the estimated compromise date, or export/sanitize the data manually. Review database contents for malicious injected scripts/admin users.
   * **Source Code / Binaries:** Deploy clean code directly from your trusted source control repository (Git, CI/CD pipeline). **Never copy application binaries or scripts from the compromised machine.**
   * **Static Assets (Uploads/Images):** Audit user-uploaded files for embedded executable code (e.g., webshells disguised as `.jpg` or `.png` files).

3. **Rotate Every Associated Secret:**
   * Invalidate and regenerate all SSH keys (`~/.ssh/authorized_keys`).
   * Rotate all database passwords, application API tokens, SMTP credentials, and third-party integration keys.
   * Reset user passwords across all affected applications.
   * Revoke and reissue SSL/TLS certificates and private keys if there is any chance they were exposed.

---

### Phase 5: Hardening & Service Restoration

Before attaching the newly built server back to the public internet:

1. **Patch Everything:** Apply all OS and application security updates.
2. **Implement Network Firewalls:**
   * Restrict administrative interfaces (SSH, RDP, database ports) to trusted IPs or a private VPN.
   * Allow only necessary traffic (e.g., ports 80/443 for web servers).
3. **Configure Defensive Tooling:**
   * Enable host-based firewalls (`ufw`, `firewalld`, `iptables`).
   * Install intrusion detection and log forwarding (e.g., `fail2ban`, `auditd`, OSSEC/Wazuh).
   * Ship logs to an external, central syslog or SIEM server so future logs cannot be altered locally.
4. **Gradual Online Cutover:**
   * Bring the server online.
   * Monitor live traffic, system resources (`top`/`htop`), and logs in real time (`tail -f /var/log/auth.log /var/log/nginx/access.log`) to verify stability and check for immediate unauthorized connection attempts.

---

### Phase 6: Post-Incident Review & Incident Response Planning

Once services are restored, solidify your operational posture so you are prepared for future events:

1. **Conduct a Post-Mortem (Root Cause Analysis):**
   * Document: *What happened? When was it detected? How was it contained? What was the root cause? What actions will prevent recurrence?*
   * Share lessons learned with the technical and management teams.

2. **Integrate Incident Response (IR) with Disaster Recovery (DR) and Business Continuity (BCP):**
   * **DR** handles *infrastructure restoration* (restoring servers, storage, network connectivity).
   * **BCP** handles *business operational continuity* (keeping the company running while systems are down).
   * **IR** provides the *security-focused procedures* (triage, containment, evidence handling, root-cause remediation).

3. **Build an Incident Response Plan (IRP):**
   * **Roles & Responsibilities:** Define who has the authority to take systems offline and who handles customer/stakeholder communications.
   * **Call Trees:** Keep an offline, readily accessible contact list of sysadmins, management, legal counsel, and hosting providers.
   * **Playbooks:** Create clear checklists for common scenarios (DDoS, ransomware, compromised web app, lost credentials).
   * **Backup Strategy:** Ensure regular, automated, off-site, and immutable (read-only) backups are maintained and tested regularly.
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Server Fault](https://serverfault.com/questions/218005/how-do-i-deal-with-a-compromised-server).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
