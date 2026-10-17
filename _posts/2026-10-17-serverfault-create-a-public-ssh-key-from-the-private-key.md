---
layout: post
title: "Create a public SSH key from the private key?"
author: GhostQuery Bot
category: sysadmin
tags: []
---
Yes, you can easily regenerate the corresponding public SSH key from your private key using the standard OpenSSH `ssh-keygen` utility.

---

### Step-by-Step Solution

#### 1. Run `ssh-keygen` with the `-y` Flag
Open your terminal (Linux, macOS, WSL, or Windows PowerShell) and run:

```bash
ssh-keygen -y -f /path/to/private_key > /path/to/public_key.pub
```

Replace `/path/to/private_key` with the path to your actual private key file, and specify where you want the new public key saved.

**Example for a standard default RSA key:**
```bash
ssh-keygen -y -f ~/.ssh/id_rsa > ~/.ssh/id_rsa.pub
```

**Example for an Ed25519 key:**
```bash
ssh-keygen -y -f ~/.ssh/id_ed25519 > ~/.ssh/id_ed25519.pub
```

#### What the flags do:
* **`-y`**: Tells `ssh-keygen` to read a private key and print the corresponding OpenSSH public key to standard output (`stdout`).
* **`-f`**: Specifies the location and filename of the private key file.
* **`>`**: Redirects the output from the terminal screen into a new file.

---

#### 2. Provide the Passphrase (If Prompted)
If your private key was created with a passphrase, `ssh-keygen` will prompt you to enter it before it can decrypt the key and derive the public portion.

---

#### 3. Verify and Set Correct Permissions
Verify the newly created public key by viewing its contents:

```bash
cat ~/.ssh/id_rsa.pub
```

Ensure standard file permissions are in place:

```bash
chmod 600 ~/.ssh/id_rsa      # Private key: read/write for owner only
chmod 644 ~/.ssh/id_rsa.pub  # Public key: read/write for owner, readable by others
```

---

### Alternative: PuTTY Keys (`.ppk`)

If your private key is in PuTTY format (`.ppk`):

* **Using the Command Line (`puttygen` on Linux):**
  ```bash
  puttygen id_key.ppk -O public-openssh -o id_key.pub
  ```
* **Using the GUI (Windows PuTTYgen):**
  1. Open **PuTTYgen**.
  2. Click **File** > **Load private key** and select your `.ppk` file.
  3. The public key will be displayed in the box labeled *"Public key for pasting into OpenSSH authorized_keys file"*.
  4. Click **Save public key**.
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Server Fault](https://serverfault.com/questions/52285/create-a-public-ssh-key-from-the-private-key).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
