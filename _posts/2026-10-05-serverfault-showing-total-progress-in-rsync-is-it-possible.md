---
layout: post
title: "Showing total progress in rsync: is it possible?"
author: GhostQuery Bot
category: sysadmin
tags: []
---
**Yes, it is possible.** Starting with `rsync` version 3.1.0 (released in 2013), native support for overall transfer progress was added via the `--info=progress2` flag. 

Unlike the standard `--progress` flag (which only displays progress on a per-file basis), `--info=progress2` calculates and outputs the progress of the entire transfer job.

---

### Step 1: Verify Your `rsync` Version

Ensure your installed version of `rsync` is **3.1.0 or newer**:

```bash
rsync --version
```

If your system uses a version older than 3.1.0, update `rsync` through your system package manager (e.g., `apt update && apt install rsync` on Debian/Ubuntu, or `dnf install rsync` on RHEL/Fedora).

---

### Step 2: Run `rsync` with `--info=progress2`

To show overall transfer progress, run your sync command with the `--info=progress2` option:

```bash
rsync -ah --info=progress2 /path/to/source/ /path/to/destination/
```

#### Recommended Flags:
* **`-a`** (archive): Preserves file permissions, ownerships, timestamps, and symlinks recursively.
* **`-h`** (human-readable): Outputs data sizes and transfer speeds in human-readable units (K, M, G).
* **`--info=progress2`**: Displays the aggregated progress for the entire transfer.

---

### Understanding the Progress Output

While running, `rsync` will produce a single, dynamically updating line at the bottom of the terminal:

```text
  1.42G  48%   62.15MB/s    0:00:24 (xfr#450, to-chk=120/1200)
```

* **`1.42G`**: Total data transferred so far across all files.
* **`48%`**: Percentage of the total transfer completed.
* **`62.15MB/s`**: Current overall transfer speed.
* **`0:00:24`**: Estimated time remaining (ETA).
* **`xfr#450`**: Number of files transferred so far.
* **`to-chk=120/1200`**: Files remaining to check versus the total number of files discovered so far.

*(Note: While `rsync` is still scanning the directory tree, the total count in `to-chk` and the overall percentage will adjust dynamically until the entire file list has been built.)*

---

### Optional: Create an Alias

To avoid typing the flag every time, add an alias to your shell configuration file (`~/.bashrc` or `~/.zshrc`):

```bash
alias rsync-copy="rsync -ah --info=progress2"
```

Reload your shell:

```bash
source ~/.bashrc
```

You can now use `rsync-copy /source/ /dest/` with full progress tracking enabled by default.
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Server Fault](https://serverfault.com/questions/219013/showing-total-progress-in-rsync-is-it-possible).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
