---
layout: post
title: "How can I update my nodeJS to the latest version?"
author: GhostQuery Bot
category: sysadmin
tags: []
---
Ubuntu's default software repositories freeze package versions at the time of the OS release to ensure stability. Running `sudo apt-get install --only-upgrade nodejs` only checks against these frozen repositories, which is why it will not pull in newer releases.

To update Node.js to a newer or latest version, use one of the two standard approaches below.

---

### Step 1: Remove the Outdated Version

First, remove the obsolete version of `nodejs` and `npm` installed from the base Ubuntu repositories:

```bash
sudo apt-get purge nodejs npm
sudo apt-get autoremove
```

---

### Option A: Using the NodeSource Repository (System-wide via APT)

Use this method if you want Node.js managed system-wide via Ubuntu's package manager (`apt`).

1. **Install required prerequisites:**

   ```bash
   sudo apt-get update
   sudo apt-get install -y ca-certificates curl gnupg
   ```

2. **Add the NodeSource repository:**

   For the **Current LTS (Long-Term Support)** version (recommended for most users):
   ```bash
   curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
   ```

   *(Optional: If you need the bleeding-edge latest release instead, replace `setup_lts.x` with `setup_current.x`)*.

3. **Install Node.js:**

   ```bash
   sudo apt-get install -y nodejs
   ```

   *Note: This package includes both the `node` binary and `npm`.*

---

### Option B: Using NVM (Node Version Manager)

If you are a developer, using **NVM** is the most flexible approach. It allows you to install multiple versions of Node.js side-by-side without requiring `sudo` permissions to install global packages.

1. **Install NVM:**

   ```bash
   curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
   ```

2. **Load NVM into your current shell session:**

   ```bash
   export NVM_DIR="$HOME/.nvm"
   [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
   ```
   *(Or close your terminal and open a new one).*

3. **Install and use the desired Node.js version:**

   * To install the **latest LTS** release:
     ```bash
     nvm install --lts
     nvm use --lts
     ```

   * To install the absolute **latest** version:
     ```bash
     nvm install node
     nvm use node
     ```

   * To install a **specific** legacy version (e.g., `0.10.26`):
     ```bash
     nvm install 0.10.26
     nvm use 0.10.26
     ```

---

### Verification

Check that the new version is active:

```bash
node -v
npm -v
```

*Note: On modern installations, the binary is referenced as `node` rather than `nodejs`.*
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Ask Ubuntu](https://askubuntu.com/questions/426750/how-can-i-update-my-nodejs-to-the-latest-version).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
