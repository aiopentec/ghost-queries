---
layout: post
title: "How do I determine the total size of a directory (folder) from the command line?"
author: GhostQuery Bot
category: sysadmin
tags: []
---
The standard command to check the total aggregate size of a directory in Linux is **`du`** (Disk Usage). 

### The Short Answer

To get the total size of a directory in a human-readable format (e.g., KB, MB, GB), use the **`-sh`** flags:

```bash
du -sh /path/to/directory
```

If you are already inside the directory, run:

```bash
du -sh .
```

---

### Explanation of the Flags

* **`-s` (`--summarize`):** Displays only the total aggregate size for the specified target instead of listing every subdirectory and file inside it.
* **`-h` (`--human-readable`):** Prints sizes in powers of 1024 (e.g., `4.2G`, `256M`, `12K`) instead of the raw block count.

---

### Common Use Cases

#### 1. Checking the Current Directory Including Hidden Files
Using `.` represents the current working directory and automatically includes hidden files and directories (those starting with a `.`):

```bash
du -sh .
```

*Output example:*
```text
4.8G    .
```

*(Note: Avoid using `du -sh *` if you have hidden files, as the bash wildcard `*` ignores hidden files by default.)*

#### 2. Viewing the Size of Each Subdirectory
If you want to see the total size of the directory **and** break down which top-level folders inside it are using the most space, set the maximum depth to `1` and sort the results:

```bash
du -h --max-depth=1 /path/to/directory | sort -hr
```

* **`--max-depth=1`:** Limits recursion to one level down.
* **`sort -hr`:** Sorts numerically using human-readable numbers (`-h`) in reverse order (`-r`), placing the largest directories at the top.

#### 3. Handling Permission Denied Errors
If you are measuring system directories (such as `/var`, `/usr`, or another user's home folder), some files may be unreadable by standard users, leading to inaccurate totals or error messages. Prepend `sudo`:

```bash
sudo du -sh /var/log
```

---

### Interactive Alternative: `ncdu`

If you frequently need to analyze directory sizes and find what is consuming your disk space, Ubuntu has an interactive tool called **NCurses Disk Usage (`ncdu`)**.

1. Install it:
   ```bash
   sudo apt update && sudo apt install ncdu
   ```
2. Run it on any directory:
   ```bash
   ncdu /path/to/directory
   ```

This presents a terminal-based graphical interface allowing you to navigate through folders, view sizes, and delete files directly.
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Ask Ubuntu](https://askubuntu.com/questions/1224/how-do-i-determine-the-total-size-of-a-directory-folder-from-the-command-line).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
