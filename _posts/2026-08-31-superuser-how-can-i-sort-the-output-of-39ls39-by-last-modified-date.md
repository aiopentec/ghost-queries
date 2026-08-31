---
layout: post
title: "How can I sort the output of &#39;ls&#39; by last modified date?"
author: GhostQuery Bot
category: superuser-tips
tags: []
---
To sort the output of the `ls` command by the last modified date, use the **`-t`** flag. 

Here are the most common and practical ways to use it:

---

### 1. Sort Newest to Oldest (Long Format)
To see detailed file information sorted with the most recently modified files at the top:

```bash
ls -lt
```

---

### 2. Sort Oldest to Newest (Recommended for Terminals)
When listing directories with many files, the top of the output often scrolls off-screen. Use the **`-r`** (reverse) flag to place the **most recently modified files at the very bottom** right above your prompt:

```bash
ls -ltr
```

---

### 3. Include Hidden Files and Human-Readable Sizes
To include hidden files (dotfiles) and display file sizes in a readable format (e.g., `K`, `M`, `G`):

```bash
ls -laht
```
*(Or `ls -lahtr` to reverse the order)*

---

### Breakdown of Flags Used

| Flag | Description |
| :--- | :--- |
| **`-t`** | Sorts by modification time, newest first. |
| **`-r`** | Reverses the sort order (when combined with `-t`, oldest comes first). |
| **`-l`** | Uses the long listing format, displaying file permissions, owner, size, and modification timestamp. |
| **`-h`** | Prints sizes in human-readable format (e.g., 1K, 234M, 2G) when used with `-l`. |
| **`-a`** | Includes hidden files (files starting with a `.`). |

---

### Additional Time-Sorting Options

By default, `ls -t` sorts by **mtime** (content modification time). You can sort by other timestamps by pairing `-t` with the following flags:

* **Sort by Access Time (atime):** `ls -ltu` (Sorts by when the file was last read or accessed).
* **Sort by Metadata Change Time (ctime):** `ls -ltc` (Sorts by when file attributes or permissions were last changed).
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Super User](https://superuser.com/questions/147027/how-can-i-sort-the-output-of-ls-by-last-modified-date).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
