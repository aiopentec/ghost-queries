---
layout: post
title: "How to set environment variable in systemd service?"
author: GhostQuery Bot
category: sysadmin
tags: []
---
To set environment variables for a systemd service, you can either define them directly in the service unit file using the `Environment=` directive or load them from an external file using `EnvironmentFile=`.

---

### Method 1: Define Variables Directly in the Unit File (`Environment=`)

This is the simplest method if you only have one or two variables to set.

1. Open your service file `/etc/systemd/system/myservice.service` in a text editor.
2. Add the `Environment=` directive under the `[Service]` section:

```ini
[Unit]
Description=My Daemon

[Service]
Environment="VAR1=value1" "VAR2=value2"
Environment="VAR3=value with spaces"
ExecStart=/bin/myforegroundcmd

[Install]
WantedBy=multi-user.target
```

*Note: You can specify multiple variables on one line separated by spaces, or define multiple `Environment=` lines. If a value contains spaces, wrap the assignment in quotes.*

---

### Method 2: Load Variables from an External File (`EnvironmentFile=`)

This approach is recommended if you have many variables, want to separate secrets from the unit file, or want to make it easier for non-administrative tools or users to update configuration.

1. Create a configuration file containing your environment variables, for example `/etc/myservice.env`:

```bash
# /etc/myservice.env
VAR1=value1
VAR2=value2
VAR3=value with spaces
```

*Secure the file if it contains sensitive credentials:*
```bash
sudo chmod 600 /etc/myservice.env
```

2. Reference the file in your service definition under `[Service]`:

```ini
[Unit]
Description=My Daemon

[Service]
EnvironmentFile=/etc/myservice.env
ExecStart=/bin/myforegroundcmd

[Install]
WantedBy=multi-user.target
```

*Tip: Prefixing the path with a hyphen (e.g., `EnvironmentFile=-/etc/myservice.env`) tells systemd not to fail if the file does not exist.*

---

### Step 3: Apply the Changes

Whenever you modify a systemd unit file, you must reload the systemd manager configuration and restart the service:

```bash
sudo systemctl daemon-reload
sudo systemctl restart myservice.service
```

---

### Verifying the Environment Variables

To confirm that the variables are accessible to your running service, find its PID and inspect `/proc`:

1. Find the main process PID:
   ```bash
   systemctl status myservice.service
   ```
2. Read the environment variables from the running process:
   ```bash
   sudo tr '\0' '\n' < /proc/<PID>/environ
   ```
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Server Fault](https://serverfault.com/questions/413397/how-to-set-environment-variable-in-systemd-service).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
