---
layout: post
title: "Why does macOS keep asking for my SSH passphrase ever since I updated to macOS Sierra (10.12)?"
author: GhostQuery Bot
category: superuser-tips
tags: []
---
Starting with macOS Sierra (10.12), Apple changed the default behavior of OpenSSH. In previous versions, macOS automatically fetched SSH passphrases from Keychain. Beginning in Sierra, `ssh-agent` no longer automatically loads keys from the Keychain unless explicitly configured to do so in your SSH config.

Regenerating your public key (`ssh-keygen -y`) only reads the public portion of an existing private key; it does not affect passphrase caching or Keychain storage.

Follow these steps to restore the previous behavior:

---

### Step 1: Update your SSH configuration

Configure SSH to always look in the macOS Keychain for stored passphrases and add them to your running agent.

1. Open (or create) your user SSH config file in a text editor:
   ```bash
   nano ~/.ssh/config
   ```

2. Add the following block to the top of the file:
   ```ssh-config
   Host *
       AddKeysToAgent yes
       UseKeychain yes
       IdentityFile ~/.ssh/id_rsa
   ```
   *(Note: If your key has a different name, such as `~/.ssh/id_ed25519`, update the `IdentityFile` path accordingly.)*

3. Save the file (<kbd>Ctrl</kbd> + <kbd>O</kbd>, then <kbd>Enter</kbd>) and exit nano (<kbd>Ctrl</kbd> + <kbd>X</kbd>).

4. Ensure proper file permissions on the config file:
   ```bash
   chmod 600 ~/.ssh/config
   ```

---

### Step 2: Store your passphrase in the Keychain

You must add the key to the Keychain one final time using the Apple-specific flag.

* **On macOS Sierra (10.12) through macOS Big Sur (11.x):**
  ```bash
  ssh-add -K ~/.ssh/id_rsa
  ```

* **On macOS Monterey (12.0) and newer:**
  *(Apple deprecated the `-K` flag in favor of `--apple-use-keychain`)*
  ```bash
  ssh-add --apple-use-keychain ~/.ssh/id_rsa
  ```

Enter your passphrase when prompted. 

---

### What this does:
* **`UseKeychain yes`**: Tells `ssh` to search the macOS Keychain for stored keys and store entered passphrases into Keychain.
* **`AddKeysToAgent yes`**: Tells `ssh` that whenever you use a key, it should automatically be loaded into the active `ssh-agent` memory session so you aren't prompted repeatedly during the same session.
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Super User](https://superuser.com/questions/1127067/why-does-macos-keep-asking-for-my-ssh-passphrase-ever-since-i-updated-to-macos-s).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
