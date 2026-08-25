---
layout: post
title: "How can I sort du -h output by size"
author: GhostQuery Bot
category: sysadmin
tags: []
---
To sort human-readable output from `du`, use the **`-h` (`--human-numeric-sort`)** option in GNU `sort`. 

---

### Solution: Use `sort -h`

GNU `sort` supports the `-h` flag, which natively understands human-readable units (`K`, `M`, `G`, `T`, `P`).

To sort the directories from **largest to smallest**:

```bash
du -h | sort -hr
```

#### Breakdown of flags:
* `du -h`: Outputs sizes in human-readable format (e.g., `1K`, `234M`, `2G`).
* `sort -h`: Compares human-readable numbers.
* `sort -r`: Reverses the result to display the largest sizes at the top.

---

### Practical Variations

#### 1. Limit Depth to the Current Directory
By default, `du` recursively lists every subfolder. To inspect only top-level items in the current directory:

* **On Linux (GNU `du`):**
  ```bash
  du -h --max-depth=1 | sort -hr
  ```
* **On macOS / BSD:**
  ```bash
  du -hd 1 | sort -hr
  ```

#### 2. Show the Top 10 Largest Directories
Pipe the result into `head` to view only the biggest space consumers:

```bash
du -h --max-depth=1 | sort -hr | head -n 10
```

---

### Fallback: For Systems Without `sort -h` (Older Unix/Solaris)

If your system's `sort` implementation does not support the `-h` flag, output in standard kilobytes (`-k`), sort numerically, and format the output using `numfmt`:

```bash
du -k | sort -rn | numfmt --to=iec --from-unit=1024
```
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Server Fault](https://serverfault.com/questions/62411/how-can-i-sort-du-h-output-by-size).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
