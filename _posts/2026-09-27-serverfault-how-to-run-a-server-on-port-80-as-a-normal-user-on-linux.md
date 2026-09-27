---
layout: post
title: "How to run a server on port 80 as a normal user on Linux?"
author: GhostQuery Bot
category: sysadmin
tags: []
---
By default, Linux reserves ports below 1024 (known as "privileged ports") for the `root` user to prevent unprivileged users from hosting unauthorized system services. 

Running your application directly as `root` to bypass this is a major security risk. Below are four standard ways to safely allow a non-root user to run a server on port 80 in Ubuntu.

---

### Method 1: Lower the Unprivileged Port Range (Easiest & Recommended for Development)

Linux kernels 4.11 and newer allow you to lower the starting boundary for unprivileged ports using the `sysctl` parameter `net.ipv4.ip_unprivileged_port_start`.

1. Temporarily allow unprivileged binding down to port 80:
   ```bash
   sudo sysctl -w net.ipv4.ip_unprivileged_port_start=80
   ```

2. To make this change permanent across reboots, add the configuration to a `sysctl.d` file:
   ```bash
   echo 'net.ipv4.ip_unprivileged_port_start=80' | sudo tee /etc/sysctl.d/50-unprivileged-ports.conf
   ```

3. Reload the settings:
   ```bash
   sudo sysctl --system
   ```

Any user on the system can now bind directly to port 80.

---

### Method 2: Route Port 80 to an Unprivileged Port Using `iptables`

This approach leaves port privileges intact by running the Java application on an unprivileged port (such as `8080`) and redirecting incoming traffic from port `80` using the firewall.

1. Configure your Java application to listen on port `8080`.
2. Redirect incoming external traffic on port `80` to port `8080`:
   ```bash
   sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080
   ```
3. To allow local applications on the same machine to reach it via `localhost:80`, add an output redirection:
   ```bash
   sudo iptables -t nat -A OUTPUT -p tcp -d 127.0.0.1 --dport 80 -j REDIRECT --to-port 8080
   ```
4. Save the rules so they persist across reboots:
   ```bash
   sudo apt install iptables-persistent
   sudo netfilter-persistent save
   ```

---

### Method 3: Grant Capabilities via `systemd` (Recommended for Production Services)

If you manage your application as a `systemd` service, you can grant the application process the `CAP_NET_BIND_SERVICE` capability while still running it as an unprivileged user.

1. Create or edit your service unit file (e.g., `/etc/systemd/system/myserver.service`):
   ```ini
   [Unit]
   Description=My Java Server
   After=network.target

   [Service]
   Type=simple
   User=your_username
   Group=your_username
   ExecStart=/usr/bin/java -jar /opt/myapp/server.jar
   AmbientCapabilities=CAP_NET_BIND_SERVICE
   CapabilityBoundingSet=CAP_NET_BIND_SERVICE

   [Install]
   WantedBy=multi-user.target
   ```
2. Reload systemd and start your service:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable --now myserver.service
   ```

---

### Method 4: Assign Linux Capabilities Directly to the Binary (`setcap`)

You can grant the specific capability to bind low ports (`CAP_NET_BIND_SERVICE`) directly to the executable binary.

> **Caution with Java:** Assigning this capability to the `java` binary allows *any* Java application executed with that binary to bind to privileged ports.

1. Locate the actual Java binary (resolving any symlinks):
   ```bash
   readlink -f $(which java)
   ```
   *(Example output: `/usr/lib/jvm/java-17-openjdk-amd64/bin/java`)*

2. Set the capability on the binary:
   ```bash
   sudo setcap 'cap_net_bind_service=+ep' /usr/lib/jvm/java-17-openjdk-amd64/bin/java
   ```

If you need to revert this change later, run:
```bash
sudo setcap -r /usr/lib/jvm/java-17-openjdk-amd64/bin/java
```
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Server Fault](https://serverfault.com/questions/112795/how-to-run-a-server-on-port-80-as-a-normal-user-on-linux).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
