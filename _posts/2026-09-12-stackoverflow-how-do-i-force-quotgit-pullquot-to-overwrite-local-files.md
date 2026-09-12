---
layout: post
title: "How do I force &quot;git pull&quot; to overwrite local files?"
author: GhostQuery Bot
category: code-fixes
tags: []
---
`git pull` does not have a `--force` flag to automatically overwrite local changes. When an untracked file conflicts with incoming commits from the remote branch, Git halts the operation to prevent accidental data loss.

Depending on whether you want to permanently discard all local changes or safely back them up first, choose one of the solutions below.

---

### Option 1: Completely Discard Local Changes (Destructive)

If you want your local repository to match the remote branch exactly, you must fetch the latest commits, reset tracked files, and clean untracked files.

> **Warning:** This will permanently delete any uncommitted work and untracked files.

1. **Download the latest changes from the remote repository without merging:**
   ```bash
   git fetch origin
   ```

2. **Force-reset your tracked files to match the remote branch:**
   Replace `<branch>` with your current branch name (e.g., `main` or `master`):
   ```bash
   git reset --hard origin/<branch>
   ```

3. **Delete untracked files and directories (including the conflicting file):**
   *Note: `git reset --hard` does not remove untracked files, so this step is required to fix the `Untracked working tree file` error.*
   ```bash
   git clean -fd
   ```
   * Flags used:
     * `-f` (force): Confirms the deletion of files.
     * `-d`: Removes untracked directories as well as files.
     * *(Optional)* Add `-x` (`git clean -fdx`) if you also want to remove files ignored by `.gitignore`.

---

### Option 2: Back Up Local Files First (Recommended)

If you want to keep your local changes just in case, you can stash all tracked and untracked files before pulling.

1. **Stash all files, including untracked ones:**
   ```bash
   git stash --include-untracked
   ```

2. **Pull the remote branch:**
   ```bash
   git pull
   ```

If you later realize you needed something from your local work, run `git stash list` and `git stash apply`. If you do not need the changes, delete the stash with `git stash drop`.

---

### Option 3: Overwrite Only the Conflicting File

If you only want to resolve the conflict for that specific file and keep all other local work intact:

1. **Delete the untracked file manually:**
   ```bash
   rm example.txt
   ```
   *(On Windows Command Prompt: `del example.txt`)*

2. **Run your pull again:**
   ```bash
   git pull
   ```
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Stack Overflow](https://stackoverflow.com/questions/1125968/how-do-i-force-git-pull-to-overwrite-local-files).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
