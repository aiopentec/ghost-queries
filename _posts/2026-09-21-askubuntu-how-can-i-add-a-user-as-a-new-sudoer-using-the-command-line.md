---
layout: post
title: "How can I add a user as a new sudoer using the command line?"
author: GhostQuery Bot
category: sysadmin
tags: []
---
### 1. GUI Delay After Adding a User

**Yes, this is normal behavior.** 

GUI management tools (such as "Users and Groups" or GNOME Settings) query system daemons like `accounts-daemon` (AccountsService) to list non-system users. These daemons sometimes cache `/etc/passwd` information or refresh user lists only upon starting a new desktop session or receiving a specific D-Bus signal. 

You can confirm the user was added immediately via the terminal without logging out:

```bash
id <username>
# or
getent passwd <username>
```

---

### 2. How to Add a User as a Sudoer via the Command Line

In Ubuntu, administrative privileges are managed through membership in the `sudo` group. Members of this group are automatically granted `sudo` rights in the default `/etc/sudoers` configuration.

You can add a user to the `sudo` group either after creating them or in a single step.

#### Option A: Add an Existing User to Sudo (Standard Method)

If you have already created the user, run:

```bash
sudo usermod -aG sudo <username>
```

* **`-a` (append):** Ensures you do not overwrite the user's existing supplementary groups.
* **`-G sudo`:** Specifies the group name.

Alternatively, Ubuntu’s `adduser` utility provides an even simpler syntax:

```bash
sudo adduser <username> sudo
```

#### Option B: Create the User and Assign Sudo in One Step

If you prefer a single command, use `useradd`:

```bash
sudo useradd -m -s /bin/bash -G sudo <username>
sudo passwd <username>
```

* **`-m`:** Creates the home directory (`/home/<username>`).
* **`-s /bin/bash`:** Sets the default login shell to Bash.
* **`-G sudo`:** Adds the user to the `sudo` group immediately.

#### Verifying Sudo Privileges
Switch to the user and verify their privileges:

```bash
su - <username>
sudo -v
```
If configured correctly, this command prompts for the user's password and returns without error.

---

### 3. Can You Delete the Original User?

**Yes, you can safely delete the original user.** 

The first user created during the Ubuntu installation is not inherently "special" to the kernel or the operating system. It is simply assigned UID `1000` (the first available non-system user ID) and automatically added to groups like `sudo`, `adm`, and `cdrom`. Any user added to the `sudo` group has the exact same administrative capabilities.

#### Safe Deletion Procedure:

1. **Verify sudo access on the new account:**  
   Log in to the new user account and ensure `sudo` works:
   ```bash
   sudo whoami
   ```
   *(It must output `root`.)*

2. **Log out of the original user:**  
   You cannot delete a user whose processes are currently running. Completely log out of the original user's desktop session and terminal.

3. **Delete the original account:**  
   From your new user account, run:
   ```bash
   sudo deluser --remove-home <original_username>
   ```
   * The `--remove-home` flag cleans up the user's home directory (`/home/<original_username>`) and their mail spool. If you want to keep their files, omit that flag.
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Ask Ubuntu](https://askubuntu.com/questions/7477/how-can-i-add-a-user-as-a-new-sudoer-using-the-command-line).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
