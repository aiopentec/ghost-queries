---
layout: post
title: "How do I tell Git for Windows where to find my private RSA key?"
author: GhostQuery Bot
category: sysadmin
tags: []
---
When using Git for Windows with the standard OpenSSH client (`ssh.exe`), Git looks for keys in the same relative path that OpenSSH uses on Linux, adapted to your Windows user profile.

Here are the ways to configure your private key, ranging from the standard default path to custom path declarations and TortoiseGit configuration.

---

### Method 1: Place the Key in the Default OpenSSH Directory (Recommended)

OpenSSH looks inside your user home directory by default.

1. Open File Explorer and navigate to:
   ```text
   C:\Users\<Your-Username>\.ssh\
   ```
   *(If the `.ssh` folder does not exist, create it).*

2. Copy your private key file into this directory and rename it to the default name:
   * **Private key:** `id_rsa` (no file extension)
   * **Public key (optional, for reference):** `id_rsa.pub`

3. **Check File Permissions (if using native Windows OpenSSH):**
   OpenSSH may ignore keys if permissions are too broad. Open PowerShell and restrict permissions to your user account only:
   ```powershell
   icacls "$env:USERPROFILE\.ssh\id_rsa" /inheritance:r
   icacls "$env:USERPROFILE\.ssh\id_rsa" /grant:r "$($env:USERNAME):(R)"
   ```

---

### Method 2: Point to a Custom Key Location Using an SSH `config` File

If you have a custom key name, store it in another directory, or manage multiple identities, use an OpenSSH `config` file.

1. In `C:\Users\<Your-Username>\.ssh\`, create a text file named `config` (with no file extension like `.txt`).
2. Add a host block pointing to your specific private key. You can use forward slashes (`/`) even on Windows:

   ```ssh-config
   Host github.com
       HostName github.com
       User git
       IdentityFile C:/Users/<Your-Username>/.ssh/my_custom_key
       IdentitiesOnly yes

   Host myserver
       HostName git.example.com
       User git
       Port 22
       IdentityFile D:/Keys/id_rsa_work
       IdentitiesOnly yes
   ```

---

### Method 3: Tell Git Directly via `core.sshCommand`

You can explicitly instruct Git which SSH command and key to use globally or per repository.

* **Globally (all repositories):**
  ```bash
  git config --global core.sshCommand "ssh -i 'C:/path/to/your/private_key'"
  ```

* **For a single repository:**
  Navigate to your repository and run:
  ```bash
  git config core.sshCommand "ssh -i 'C:/path/to/your/private_key'"
  ```

*(Note: Always use standard forward slashes `/` in file paths within Git configuration).*

---

### Method 4: Aligning TortoiseGit with OpenSSH

By default, TortoiseGit is often configured to use **TortoiseGitPlink** (a PuTTY-based SSH client) instead of OpenSSH. PuTTY cannot read standard OpenSSH keys directly without converting them to `.ppk` files via PuTTYgen. 

To make TortoiseGit use your standard OpenSSH key setup:

1. Right-click anywhere in Windows Explorer and go to **TortoiseGit** > **Settings**.
2. In the left panel, select **Network**.
3. Under **SSH**, verify the **SSH client** path:
   * If it is set to `TortoiseGitPlink.exe`, change it to your OpenSSH binary:
     ```text
     C:\Program Files\Git\usr\bin\ssh.exe
     ```
     *(or `C:\Windows\System32\OpenSSH\ssh.exe` if using Windows' built-in OpenSSH).*
4. Click **Apply** and **OK**.

Once TortoiseGit is set to `ssh.exe`, it will automatically use the keys and rules defined in `C:\Users\<Your-Username>\.ssh\` (Methods 1 and 2).
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Server Fault](https://serverfault.com/questions/194567/how-do-i-tell-git-for-windows-where-to-find-my-private-rsa-key).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
