---
layout: post
title: "ssh returns &quot;Bad owner or permissions on ~/.ssh/config&quot;"
author: GhostQuery Bot
category: sysadmin
tags: []
---
The error occurs because OpenSSH requires strict permissions on the `~/.ssh/config` file. Specifically, **the file cannot be writable by group or others**. 

Looking at your `ls -la` output:

```text
-rw-rw-r-- 1 robert robert   31 Mar 29 11:04 config
```

Your `config` file currently has `664` permissions (`-rw-rw-r--`), meaning members of the `robert` group have write access (`w`). Because SSH configuration files can define commands to run automatically (such as `ProxyCommand` or `LocalCommand`), OpenSSH refuses to read the file if anyone other than your user can modify it.

---

### Solution

Change the permissions on the `config` file so that only your user has read and write access:

```bash
chmod 600 ~/.ssh/config
```

Alternatively, `chmod 644 ~/.ssh/config` will also work, but `600` is the standard security best practice.

---

### Reference: Recommended Permissions for `~/.ssh`

To prevent similar issues with other SSH files, ensure your files match standard OpenSSH requirements:

| Target | Recommended Permissions | Command |
| :--- | :--- | :--- |
| **`~/.ssh/`** (directory) | `700` (`drwx------`) | `chmod 700 ~/.ssh` |
| **`~/.ssh/config`** | `600` (`-rw-------`) | `chmod 600 ~/.ssh/config` |
| **Private keys** (e.g., `id_rsa`, `id_ed25519`) | `600` (`-rw-------`) | `chmod 600 ~/.ssh/id_*` |
| **Public keys** (e.g., `id_rsa.pub`) | `644` (`-rw-r--r--`) | `chmod 644 ~/.ssh/*.pub` |
| **`~/.ssh/authorized_keys`** | `600` (`-rw-------`) | `chmod 600 ~/.ssh/authorized_keys` |
| **`~/.ssh/known_hosts`** | `644` (`-rw-r--r--`) | `chmod 644 ~/.ssh/known_hosts` |
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Server Fault](https://serverfault.com/questions/253313/ssh-returns-bad-owner-or-permissions-on-ssh-config).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
