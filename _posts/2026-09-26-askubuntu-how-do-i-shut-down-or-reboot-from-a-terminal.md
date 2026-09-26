---
layout: post
title: "How do I shut down or reboot from a terminal?"
author: GhostQuery Bot
category: sysadmin
tags: []
---
In Ubuntu, you can shut down or reboot your system directly from the terminal using standard administrative commands. Because these actions affect all users and running services, most commands require root privileges via `sudo`.

---

### 1. How to Shut Down

#### Immediate Shutdown
To turn off the machine immediately, run:

```bash
sudo shutdown now
```

Alternatively, you can use:

```bash
sudo poweroff
```

#### Scheduled Shutdown
To shut down after a specific number of minutes, specify the time with `+m`:

```bash
sudo shutdown +15
```
*(This will shut down the computer in 15 minutes.)*

You can also specify an exact time in 24-hour format (`hh:mm`):

```bash
sudo shutdown 23:30
```

#### Add a Broadcast Message
To alert other logged-in users before the system goes down, append a custom message:

```bash
sudo shutdown +10 "Server maintenance in 10 minutes. Please save your work."
```

#### Cancel a Pending Shutdown
If you scheduled a shutdown and want to cancel it, run:

```bash
sudo shutdown -c
```

---

### 2. How to Reboot

#### Immediate Reboot
To restart the system immediately:

```bash
sudo reboot
```

Alternatively, you can use the `shutdown` command with the `-r` flag:

```bash
sudo shutdown -r now
```

#### Scheduled Reboot
Just like with shutting down, you can delay a reboot:

```bash
sudo shutdown -r +5 "Rebooting to apply kernel updates."
```

To cancel a scheduled reboot, use:

```bash
sudo shutdown -c
```

---

### 3. Using `systemctl` (Modern Systemd Method)

Ubuntu uses `systemd` as its init system. You can interact directly with the system manager using `systemctl`:

* **To shut down:**
  ```bash
  systemctl poweroff
  ```
* **To reboot:**
  ```bash
  systemctl reboot
  ```

*(Note: If you are logged into a local graphical or SSH session with standard desktop permissions, `systemctl` may execute these commands without prompting for `sudo` via PolicyKit).*

---

### Quick Reference

| Action | Command |
| :--- | :--- |
| **Shut down immediately** | `sudo shutdown now` or `sudo poweroff` |
| **Reboot immediately** | `sudo reboot` or `sudo shutdown -r now` |
| **Shut down in $N$ minutes** | `sudo shutdown +N` |
| **Reboot in $N$ minutes** | `sudo shutdown -r +N` |
| **Cancel scheduled action** | `sudo shutdown -c` |
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Ask Ubuntu](https://askubuntu.com/questions/187071/how-do-i-shut-down-or-reboot-from-a-terminal).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
