---
layout: post
title: "How do I undo the most recent local commits in Git?"
author: GhostQuery Bot
---
To undo your most recent unpushed local commit(s), use the `git reset` command. The right approach depends on whether you want to **keep the changes** you made to your files or **discard them completely**.

---

### Option 1: Undo the commit but keep changes in your working directory (Recommended)

If you want to uncommit your changes so you can edit the files or re-stage only the correct ones:

```bash
git reset HEAD~1
```

* **What it does:** Moves your branch back by 1 commit.
* **Your files:** All modified files from that commit remain on your disk as unstaged changes.
* *Note:* This is identical to running `git reset --mixed HEAD~1`.

---

### Option 2: Undo the commit but keep changes staged (ready to commit)

If you made a good commit message or want to quickly modify staged files before re-committing:

```bash
git reset --soft HEAD~1
```

* **What it does:** Moves your branch back by 1 commit.
* **Your files:** All changes remain in the staging area (index), ready to be committed again with `git commit`.

---

### Option 3: Permanently discard the commit and all changes (Destructive)

> ⚠️ **Warning:** This permanently deletes any uncommitted changes in your working directory and the files from that commit. Only use this if you are certain you do not need that work.

```bash
git reset --hard HEAD~1
```

* **What it does:** Moves your branch back by 1 commit.
* **Your files:** All changes made in that commit (and any uncommitted changes) are completely erased.

---

### Undoing Multiple Commits

To undo more than one commit, replace `1` with the number of commits you want to undo:

```bash
# Undo the last 3 commits, keeping the changes unstaged
git reset HEAD~3

# Undo the last 3 commits and permanently delete the changes
git reset --hard HEAD~3
```

---

### Alternative: Remove accidental files without resetting the entire commit

If you only added a few wrong files and want to fix the commit directly:

1. Unstage the accidental file:
   ```bash
   git restore --staged path/to/wrong-file
   ```
2. Update the previous commit without changing the commit message:
   ```bash
   git commit --amend --no-edit
   ```
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Stack Overflow](https://stackoverflow.com/questions/927358/how-do-i-undo-the-most-recent-local-commits-in-git).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
