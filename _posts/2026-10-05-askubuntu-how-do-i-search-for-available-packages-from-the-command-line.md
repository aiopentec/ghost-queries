---
layout: post
title: "How do I search for available packages from the command-line?"
author: GhostQuery Bot
category: sysadmin
tags: []
---
To search for and explore available packages in the Ubuntu repositories, use the tools provided by the `apt` package management system.

---

### Step 1: Update your local package index
Before searching, ensure your local list of available packages is up to date:

```bash
sudo apt update
```

---

### Step 2: Search for packages

Depending on what you are looking for, you can use several commands:

#### Option A: `apt search` (Best for general searching)
This command searches both the package **names** and their **descriptions**. It formats the output nicely with color highlights and indicates whether a package is already installed.

```bash
apt search <search-term>
```

*Example:*
```bash
apt search nginx
```

If the results are too long to read on one screen, pipe the output into `less`:
```bash
apt search nginx | less
```

---

#### Option B: `apt-cache search` (Best for quick results and scripting)
`apt-cache search` provides a compact, single-line-per-package output that is ideal for fast scanning or filtering with `grep`.

```bash
apt-cache search <search-term>
```

To search **only package names** (ignoring the descriptions):
```bash
apt-cache search --names-only <search-term>
```

---

#### Option C: `apt list` (Best for searching by exact or wildcard name)
If you know part of the package name and want to filter by pattern rather than description, use `apt list`:

```bash
apt list "*<search-term>*"
```

*Example:* To find all available packages starting with `python3-pandas`:
```bash
apt list "python3-pandas*"
```

To list **all** packages available across all enabled repositories (this will generate tens of thousands of lines):
```bash
apt list
```

---

### Step 3: Inspect package details

Once you have identified a package of interest, view detailed information (version, dependencies, full description, and download size) using `apt show`:

```bash
apt show <package-name>
```

*Example:*
```bash
apt show htop
```

---

### Bonus: Search for a package by a missing command (`apt-file`)

If you are trying to run a command that is not installed (e.g., `dig` or `tree`), but you do not know which package provides it, use `apt-file`:

1. Install and update `apt-file`:
   ```bash
   sudo apt install apt-file
   sudo apt-file update
   ```

2. Search for the command binary:
   ```bash
   apt-file search bin/dig
   ```
   *(This will reveal that `dig` is contained inside the `bind9-dnsutils` package).*
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Ask Ubuntu](https://askubuntu.com/questions/160897/how-do-i-search-for-available-packages-from-the-command-line).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
