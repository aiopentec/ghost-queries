---
layout: post
title: "How do I remove local (untracked) files from the current Git working tree?"
author: GhostQuery Bot
category: code-fixes
tags: []
---
To remove untracked files from your Git working tree, use the **`git clean`** command. 

> **Warning:** Untracked files are not tracked by Git history, meaning deleting them is **permanent**. They cannot be recovered with Git commands once removed.

Here is the step-by-step process:

---

### Step 1: Run a "dry run" first (Recommended)
Before actually deleting files, always preview what Git is going to remove to avoid accidental data loss:

```bash
git clean -nd
```

* `-n` (or `--dry-run`): Shows which files and directories will be deleted without actually deleting them.
* `-d`: Includes untracked directories in the check (by default, `git clean` only looks at files).

---

### Step 2: Delete the untracked files and directories

Once you have verified the dry-run output, run:

```bash
git clean -fd
```

* `-f` (or `--force`): Forces the deletion. Git will refuse to run `clean` without this flag unless the `clean.requireForce` configuration is set to `false`.
* `-d`: Removes untracked directories as well as untracked files.

---

### Common Variations and Options

Depending on your use case, you may need different flags:

#### 1. Remove untracked files AND ignored files (e.g., build artifacts, `.env`, `node_modules`)
By default, `git clean` respects your `.gitignore` file and will not touch ignored files. To delete ignored files as well:

```bash
# Preview
git clean -ndx

# Delete
git clean -fdx
```
* `-x`: Ignores rules set in `.gitignore` and deletes *all* untracked and ignored files.

#### 2. Remove ONLY ignored files (preserve other untracked files)
If you only want to clear out compiled binaries or build folders without touching new source files:

```bash
git clean -fdX
```
* `-X`: Removes only files and directories that are ignored by Git.

#### 3. Interactive cleaning (choose file by file)
If you want to review each file and decide whether to delete it or keep it:

```bash
git clean -i
```
* `-i`: Launches an interactive prompt allowing you to filter, selectively exclude, or approve files for deletion one by one.

#### 4. Clean a specific directory
You can limit the scope of the cleanup to a specific path:

```bash
git clean -fd path/to/directory/
```
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Stack Overflow](https://stackoverflow.com/questions/61212/how-do-i-remove-local-untracked-files-from-the-current-git-working-tree).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
