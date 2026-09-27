---
layout: post
title: "Error message &quot;sudo: unable to resolve host (none)&quot;"
author: GhostQuery Bot
category: sysadmin
tags: []
---
This error occurs because your system's hostname is either empty or explicitly set to `(none)`, and the system cannot resolve this name through `/etc/hosts` or DNS. When you execute `sudo`, it attempts to look up the current hostname, times out after a few seconds, and throws the error.

To resolve this, you need to assign a valid hostname and map it in `/etc/hosts`.

---

### Step 1: Set a Valid Hostname

Choose a name for your system (for example, `ubuntu` or `myserver`). 

Run the following command, replacing `<new-hostname>` with your chosen name:

```bash
sudo hostnamectl set-hostname <new-hostname>
```

*Note: Because `sudo` is currently slow, the command will pause for a few seconds before executing. This is normal until the fix is complete.*

If you are using a minimal container or older release without `systemd`/`hostnamectl`, run:

```bash
sudo hostname <new-hostname>
echo "<new-hostname>" | sudo tee /etc/hostname
```

---

### Step 2: Update `/etc/hosts`

The system needs to map your new hostname to a loopback IP address.

1. Open `/etc/hosts` in a text editor:

   ```bash
   sudo nano /etc/hosts
   ```

2. Look for the local loopback entries at the top of the file. Ensure you have lines that look like this:

   ```text
   127.0.0.1   localhost
   127.0.1.1   <new-hostname>
   ```

   *(Replace `<new-hostname>` with the exact name you set in Step 1.)*

3. Save and exit (in Nano, press `Ctrl+O`, `Enter`, then `Ctrl+X`).

---

### Step 3: Verify the Changes

1. Verify the current hostname:

   ```bash
   hostname
   ```
   It should return your `<new-hostname>`.

2. Test `sudo` to confirm it runs immediately without delay or warnings:

   ```bash
   sudo true
   ```

3. Restart your shell session or run `exec bash` to update the shell prompt so it displays `ubuntu@<new-hostname>:~$` instead of `ubuntu@(none):~$`.
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Ask Ubuntu](https://askubuntu.com/questions/59458/error-message-sudo-unable-to-resolve-host-none).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
