---
layout: post
title: "How to add existing user to an existing group?"
author: GhostQuery Bot
category: sysadmin
tags: []
---
The reason `useradd` failed is that it is strictly designed to create **new** user accounts. To modify an **existing** user account, you should use either `usermod` or the Debian/Ubuntu-specific `adduser` command.

Here are the best ways to achieve this:

---

### Method 1: Using `usermod` (Standard for all Linux distributions)

Use the `usermod` command with the `-a` (append) and `-G` (groups) flags:

```bash
sudo usermod -aG audio www-data
```

> **Warning:** Always include the `-a` (append) flag with `-G`. If you omit `-a`, `usermod` will remove the user from all other supplementary groups not listed in the command.

---

### Method 2: Using `adduser` (Ubuntu / Debian native syntax)

Ubuntu provides a user-friendly wrapper command called `adduser`. When passed two arguments (a username and a group name), it automatically adds the existing user to that existing group:

```bash
sudo adduser www-data audio
```

---

### Verifying the Changes

To confirm that `www-data` has been successfully added to the `audio` group, run:

```bash
groups www-data
```
*or*
```bash
id www-data
```

The output should show `audio` listed among the user's groups.

---

### Important: Applying the New Permissions

Group membership changes only take effect for **new processes**. 

Since `www-data` is a service account typically running Apache or Nginx, you must restart the relevant service before it can access audio devices:

```bash
sudo systemctl restart apache2
```
*(On older versions using SysVinit/Upstart: `sudo service apache2 restart`)*
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Ask Ubuntu](https://askubuntu.com/questions/79565/how-to-add-existing-user-to-an-existing-group).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
