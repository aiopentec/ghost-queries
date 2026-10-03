---
layout: post
title: "How can I recursively delete all files of a specific extension in the current directory?"
author: GhostQuery Bot
category: sysadmin
tags: []
---
The safest and most standard way to recursively delete files matching a specific pattern in Linux is using the `find` command. 

To prevent accidental data loss, always follow a **two-step workflow**: first, preview the files that will be affected; second, execute the deletion.

---

### Step 1: Preview the files (Dry Run)

Before deleting anything, verify your current directory and list all matching files to ensure you are targeting the right files:

1. Confirm your current directory:
   ```bash
   pwd
   ```

2. List all files ending with `.bak` in the current directory and all subdirectories:
   ```bash
   find . -type f -name "*.bak"
   ```

**Breakdown of the command:**
* `.` specifies the current directory as the starting search path.
* `-type f` ensures that only regular files are matched (directories named `.bak` will not be selected).
* `-name "*.bak"` searches for filenames ending in `.bak`. **Always enclose the pattern in quotes** to prevent the shell from expanding the wildcard before `find` processes it.

---

### Step 2: Delete the files

Once you have verified that the output from Step 1 lists only the files you want to delete, you can safely remove them using one of the following methods.

#### Method A: Direct deletion (Recommended)
Add the `-delete` flag to the end of the verified command:

```bash
find . -type f -name "*.bak" -delete
```

> **Important:** Always place the `-delete` flag at the very end of the command. The `find` command evaluates arguments in order; placing `-delete` earlier can delete files before the `-name` filter is evaluated.

---

#### Method B: Interactive confirmation (Extra Cautious)
If you want Linux to prompt you for confirmation before deleting each individual file, use the `-ok` action instead of `-delete`:

```bash
find . -type f -name "*.bak" -ok rm {} \;
```

For every matching file, you will be prompted:
```text
< rm ... ./path/to/file.bak > ?
```
Press `y` to confirm or `n` to skip.

---

### Alternative: Using Bash `globstar`

If you are using Bash (version 4.0 or newer) and prefer not to use `find`, you can enable recursive globbing:

1. Enable the `globstar` shell option:
   ```bash
   shopt -s globstar
   ```

2. Preview the matches:
   ```bash
   ls **/*.bak
   ```

3. Delete with an interactive prompt for safety:
   ```bash
   rm -i **/*.bak
   ```
   *(Remove the `-i` flag if you do not want to be prompted for each file.)*
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Ask Ubuntu](https://askubuntu.com/questions/377438/how-can-i-recursively-delete-all-files-of-a-specific-extension-in-the-current-di).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
