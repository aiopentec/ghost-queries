---
layout: post
title: "How do I change my private key passphrase?"
author: GhostQuery Bot
category: sysadmin
tags: []
---
You can change or remove the passphrase of an existing SSH private key using the `ssh-keygen` utility with the `-p` flag. This command modifies the key in-place without altering the public key or breaking access to servers where the public key is already installed.

---

### Step 1: Back Up Your Private Key (Recommended)

Before modifying the key file, create a backup copy:

```bash
cp ~/.ssh/id_rsa ~/.ssh/id_rsa.bak
```
*(Replace `~/.ssh/id_rsa` with the actual path to your private key file, such as `~/.ssh/id_dsa` or `~/.ssh/id_ed25519`.)*

---

### Step 2: Change the Passphrase

Run `ssh-keygen` with the `-p` (change passphrase) and `-f` (file path) flags:

```bash
ssh-keygen -p -f ~/.ssh/id_rsa
```

You will see the following prompts:

1. **Enter old passphrase:** Type your current passphrase and press <kbd>Enter</kbd>.
2. **Enter new passphrase:** Type your new passphrase and press <kbd>Enter</kbd>.
3. **Enter same passphrase again:** Retype the new passphrase and press <kbd>Enter</kbd>.

Once completed, the key will be re-encrypted with the new passphrase.

---

### How to Completely Remove the Passphrase

Yes, removing the passphrase simply means setting it to an empty value.

1. Run the same command:
   ```bash
   ssh-keygen -p -f ~/.ssh/id_rsa
   ```
2. Enter your current passphrase when prompted.
3. When prompted for **Enter new passphrase**, press <kbd>Enter</kbd> without typing anything.
4. When prompted to confirm, press <kbd>Enter</kbd> again.

The private key will now be saved unencrypted.

---

### Non-Interactive Command (Automation / Scripting)

If you need to change or remove a passphrase non-interactively in a script, you can supply the old passphrase with `-P` and the new passphrase with `-N`:

* **To change the passphrase:**
  ```bash
  ssh-keygen -p -P "old_passphrase" -N "new_passphrase" -f ~/.ssh/id_rsa
  ```

* **To remove the passphrase entirely:**
  ```bash
  ssh-keygen -p -P "old_passphrase" -N "" -f ~/.ssh/id_rsa
  ```

---

### Step 3: Update `ssh-agent` (If Applicable)

If you use `ssh-agent`, the agent may still hold the old key state in memory. Remove and re-add the key to update it:

```bash
ssh-add -d ~/.ssh/id_rsa
ssh-add ~/.ssh/id_rsa
```
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Server Fault](https://serverfault.com/questions/50775/how-do-i-change-my-private-key-passphrase).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
