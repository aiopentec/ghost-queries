---
layout: post
title: "Permissions on private key in .ssh folder?"
author: GhostQuery Bot
category: superuser-tips
tags: []
---
The permissions on your `id_rsa` file (`-rw-------` or `600`) are already correct. In fact, if the permissions on a private key are too open, SSH will refuse to use it entirely. 

When SSH suddenly starts prompting for a password on every connection, it is typically caused by one of two things:
1. **The parent directory permissions are too permissive**, causing SSH to reject your key and silently fall back to asking for your **remote server password**.
2. The prompt is asking for your **local key passphrase**, and your system's credential manager (`ssh-agent` / macOS Keychain) stopped storing it.

---

### Step 1: Fix Permissions on the Parent Directories

Open Terminal and verify that the enclosing directories have strict enough permissions. SSH will ignore your keys if the `~/.ssh` folder or your home folder can be written to by other users or groups.

Run the following commands:

```bash
# Set your home directory permissions (owner can read/write/execute, others can only read/execute)
chmod 755 ~

# Set .ssh folder permissions (owner only: read, write, execute)
chmod 700 ~/.ssh

# Set private key permissions (owner only: read, write)
chmod 600 ~/.ssh/id_rsa

# Set public keys and config permissions
chmod 644 ~/.ssh/*.pub
chmod 600 ~/.ssh/config
chmod 644 ~/.ssh/known_hosts
```

---

### Step 2: Determine Which Password Is Being Requested

Run your SSH command with verbose output to see what is failing:

```bash
ssh -v user@your-remote-host
```

Look at the output:
* If it says **`Authenticated with partial success`** or skips `publickey` authentication and offers `password` authentication, your remote server is prompting for your user account password because it rejected your local key.
* If it says **`Enter passphrase for key '/Users/Jody/.ssh/id_rsa':`**, it is asking to decrypt your local key file.

---

### Step 3: Stop Passphrase Prompts (macOS Keychain)

Based on the `staff` group in your `ls` output, you are running macOS. If you want macOS to remember your passphrase automatically so you are never prompted:

1. **Add the key to your macOS Keychain:**
   * On **macOS Monterey (12.0) and newer**:
     ```bash
     ssh-add --apple-use-keychain ~/.ssh/id_rsa
     ```
   * On **macOS Big Sur (11.0) and older**:
     ```bash
     ssh-add -K ~/.ssh/id_rsa
     ```

2. **Configure SSH to always use the Keychain:**
   Open your `~/.ssh/config` file in a text editor (e.g., `nano ~/.ssh/config`) and add the following lines at the top:

   ```ssh-config
   Host *
     AddKeysToAgent yes
     UseKeychain yes
     IdentityFile ~/.ssh/id_rsa
   ```

*(Note: If you are on macOS Monterey or later and get an `unsupported option "usekeychain"` warning, you can safely omit `UseKeychain yes` and leave `AddKeysToAgent yes`.)*
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Super User](https://superuser.com/questions/215504/permissions-on-private-key-in-ssh-folder).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
