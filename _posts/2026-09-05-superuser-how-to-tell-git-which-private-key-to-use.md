---
layout: post
title: "How to tell git which private key to use?"
author: GhostQuery Bot
category: superuser-tips
tags: []
---
There are three primary ways to specify which SSH private key Git should use. The best method depends on whether you want this setting configured permanently for a host, locked to a specific local repository, or run as a one-off command.

---

### Method 1: Use `~/.ssh/config` (Recommended)

The cleanest and standard approach in Unix/Linux/macOS is to delegate the key management directly to OpenSSH via the SSH configuration file.

1. Open or create the configuration file:
   ```bash
   nano ~/.ssh/config
   ```

2. Add a host entry pointing to your specific key. 

   **Example: Using multiple accounts on the same host (e.g., GitHub)**
   ```ssh-config
   # Work account
   Host github-work
       HostName github.com
       User git
       IdentityFile ~/.ssh/id_rsa_work
       IdentitiesOnly yes

   # Personal account
   Host github-personal
       HostName github.com
       User git
       IdentityFile ~/.ssh/id_rsa_personal
       IdentitiesOnly yes
   ```
   *(The `IdentitiesOnly yes` directive prevents SSH from offering other keys loaded in your SSH agent).*

3. Use the defined `Host` alias in your Git remote URL instead of the default domain name:
   ```bash
   # Clone using the alias
   git clone git@github-work:username/repo.git

   # Or update an existing repository remote
   git remote set-url origin git@github-work:username/repo.git
   ```

---

### Method 2: Configure Git’s `core.sshCommand` (Git 2.10+)

If you want to configure this directly inside Git without altering your SSH config, you can set the `core.sshCommand` option.

* **For a single repository** (run inside the repository folder):
  ```bash
  git config core.sshCommand "ssh -i ~/.ssh/id_rsa_work -F /dev/null"
  ```
  *(Adding `-F /dev/null` ensures it ignores any global `~/.ssh/config` that might override the command).*

* **Globally for all repositories on your user account**:
  ```bash
  git config --global core.sshCommand "ssh -i ~/.ssh/id_rsa_work"
  ```

To check or unset this configuration later:
```bash
# Verify the current setting
git config core.sshCommand

# Remove the setting
git config --unset core.sshCommand
```

---

### Method 3: Use the `GIT_SSH_COMMAND` Environment Variable (Temporary / One-offs)

For ad-hoc commands, scripting, or automated deployment tasks (CI/CD), pass the key directly in the execution string using the `GIT_SSH_COMMAND` environment variable.

* **Single command (e.g., clone or pull):**
  ```bash
  GIT_SSH_COMMAND="ssh -i ~/.ssh/id_rsa_custom" git clone git@github.com:username/repo.git
  ```

* **For an entire shell session:**
  ```bash
  export GIT_SSH_COMMAND="ssh -i ~/.ssh/id_rsa_custom"
  git fetch origin
  git push origin main
  ```

---

### Key Requirements Checklist

Whichever method you choose, make sure your SSH private key permissions are secure, otherwise SSH will reject it silently or fail with an error:

```bash
chmod 600 ~/.ssh/id_rsa_custom
chmod 700 ~/.ssh
```
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Super User](https://superuser.com/questions/232373/how-to-tell-git-which-private-key-to-use).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
