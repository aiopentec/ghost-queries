---
layout: post
title: "How to automate SSH login with password?"
author: GhostQuery Bot
category: sysadmin
tags: []
---
Standard `ssh` clients explicitly bypass `stdin` (standard input) and read directly from the controlling terminal device (`/dev/tty`) to prevent passwords from being piped via shell scripts. 

To automate SSH logins using a password, use one of the methods below.

---

### Method 1: Using `sshpass` (Recommended)

`sshpass` is a lightweight utility designed specifically to run SSH non-interactively using keyboard-interactive password authentication.

#### 1. Install `sshpass`

* **Debian / Ubuntu:**
  ```bash
  sudo apt-get update && sudo apt-get install -y sshpass
  ```
* **RHEL / CentOS / Rocky Linux / Fedora:**
  ```bash
  sudo dnf install -y epel-release && sudo dnf install -y sshpass
  ```
* **macOS (via Homebrew):**
  ```bash
  brew install hudochenkov/sshpass/sshpass
  ```

#### 2. Usage Examples

* **Direct command line:**
  ```bash
  sshpass -p 'your_password' ssh username@server_ip
  ```

* **Running a remote command:**
  ```bash
  sshpass -p 'your_password' ssh username@server_ip "uptime"
  ```

* **Using an environment variable (avoids exposing the password in bash history / process table):**
  ```bash
  export SSHPASS='your_password'
  sshpass -e ssh username@server_ip
  ```

* **Bypassing the host key verification prompt (for new test VMs):**
  ```bash
  sshpass -p 'your_password' ssh -o StrictHostKeyChecking=no username@server_ip
  ```

---

### Method 2: Using an `expect` Script

If `sshpass` is not available or cannot be installed, you can use `expect`, which simulates a TTY and feeds the password when prompted.

#### 1. Install `expect`

* **Debian / Ubuntu:** `sudo apt-get install expect`
* **RHEL / CentOS:** `sudo dnf install expect`

#### 2. Run as a one-liner

```bash
expect -c '
spawn ssh -o StrictHostKeyChecking=no username@server_ip "uptime"
expect "password:"
send "your_password\r"
interact
'
```

---

### Alternative: SSH Key-Based Authentication

Even for local test environments, setting up passwordless SSH keys takes only two commands and avoids needing third-party utilities:

1. **Generate a key on your client machine** (press Enter to accept defaults):
   ```bash
   ssh-keygen -t ed25519 -N "" -f ~/.ssh/id_test
   ```

2. **Copy the key to the VM:**
   ```bash
   ssh-copy-id -i ~/.ssh/id_test.pub username@server_ip
   ```

3. **Log in automatically without prompts:**
   ```bash
   ssh -i ~/.ssh/id_test username@server_ip
   ```
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Server Fault](https://serverfault.com/questions/241588/how-to-automate-ssh-login-with-password).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
