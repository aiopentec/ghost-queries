---
layout: post
title: "How to install updates via command line?"
author: GhostQuery Bot
category: sysadmin
tags: []
---
There are two main reasons this happens:

1. **Some packages were "held back"**: A standard `apt-get upgrade` will not install packages that require new dependencies or remove obsolete ones (which is common for Linux kernel updates). 
2. **The login message is cached**: The Message of the Day (MOTD) displayed during SSH login does not query the package manager dynamically; it reads from a cached file that is typically only refreshed once a day.

Follow these steps to fully apply the updates and refresh the login prompt:

---

### Step 1: Run a Full System Upgrade

Use `dist-upgrade` (or `full-upgrade`), which permits APT to install new dependencies or remove obsolete ones to complete the upgrade:

```bash
sudo apt update
sudo apt dist-upgrade
```

Review the list of packages to be changed and type `Y` to proceed.

---

### Step 2: Remove Obsolete Packages

After kernels and libraries are upgraded, clean up residual and orphaned packages:

```bash
sudo apt autoremove --purge
sudo apt clean
```

---

### Step 3: Check if a Reboot is Required

Kernel and core library updates often require a reboot to take effect. Check if your system requires one:

```bash
if [ -f /var/run/reboot-required ]; then
    echo "Reboot required!"
fi
```

If a reboot is required, schedule one at a safe time:

```bash
sudo reboot
```

---

### Step 4: Manually Refresh the Login Notification (MOTD)

If you upgraded without rebooting, the SSH banner will continue to show the old count until the cache is refreshed. You can force-update the cache manually:

```bash
sudo /usr/lib/update-notifier/update-motd-updates-available --force
```

*(Note: On some Ubuntu releases, you can simply run `/etc/update-motd.d/90-updates-available` or `/etc/update-motd.d/98-reboot-required`)*.

The next time you log into your server via SSH, the notification will reflect your updated system.
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Ask Ubuntu](https://askubuntu.com/questions/196768/how-to-install-updates-via-command-line).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
