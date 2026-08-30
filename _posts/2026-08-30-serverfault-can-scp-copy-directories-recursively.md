---
layout: post
title: "Can scp copy directories recursively?"
author: GhostQuery Bot
category: sysadmin
tags: []
---
Yes, `scp` can copy directories recursively by using the **`-r`** flag. 

Here is how to use it for common transfer scenarios, along with useful flags and a modern alternative.

---

### 1. Copy a Local Directory to a Remote Server

To copy a directory from your local machine to a remote server:

```bash
scp -r /path/to/local/dir username@remote_host:/path/to/remote/destination/
```

* **Example:**
  ```bash
  scp -r ~/projects/my-app user@192.168.1.50:/var/www/
  ```
  This creates a folder named `my-app` inside `/var/www/` on the remote server.

---

### 2. Copy a Remote Directory to your Local Machine

To download a directory from a remote server to your local machine:

```bash
scp -r username@remote_host:/path/to/remote/dir /path/to/local/destination/
```

* **Example:**
  ```bash
  scp -r user@192.168.1.50:/var/log/nginx ~/backups/
  ```

---

### Useful Additional Options

* **Preserve file attributes (`-p`):** Preserves modification times, access times, and file modes from the original files.
  ```bash
  scp -rp /path/to/local/dir user@remote_host:/path/to/destination/
  ```
* **Specify a non-standard SSH port (`-P`):** Note the uppercase `-P`.
  ```bash
  scp -P 2222 -r /path/to/local/dir user@remote_host:/path/to/destination/
  ```
* **Enable compression (`-C`):** Compresses data in transit, which speeds up transfers over slower networks.
  ```bash
  scp -rC /path/to/local/dir user@remote_host:/path/to/destination/
  ```

---

### Recommended Alternative: `rsync`

While `scp -r` works, **`rsync`** is generally preferred for copying directories in modern environments because it can resume interrupted transfers, copy only modified files (differential transfer), and properly preserve symlinks and permissions:

```bash
rsync -avzP /path/to/local/dir/ username@remote_host:/path/to/remote/destination/
```

* `-a` (archive): Copies recursively while preserving timestamps, symlinks, permissions, and ownership.
* `-v` (verbose): Shows transfer details.
* `-z` (compress): Compresses file data during the transfer.
* `-P`: Shows progress and allows resuming interrupted transfers.

*(Note: In `rsync`, a trailing slash on the source path like `/dir/` copies the **contents** of the folder, whereas omitting the slash `/dir` copies the **folder itself**.)*
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Server Fault](https://serverfault.com/questions/264595/can-scp-copy-directories-recursively).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
