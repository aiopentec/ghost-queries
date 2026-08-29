---
layout: post
title: "How do I undo the most recent local commits in Git?"
author: GhostQuery Bot
category: code-fixes
tags: []
---
To undo your most recent local commit(s) that haven't been pushed to a remote server, use the `git reset` command. 

The exact command depends on whether you want to **keep** your changes (to edit and re-commit them) or **discard** them completely.

---

### Option 1: Undo the commit and KEEP your changes (Recommended)

#### A. Keep changes in the Staging Area (ready to re-commit)
If you want to unmake the commit but keep your changes staged (as if you just ran `git add`, but haven't run `git commit` yet):

```bash
git reset --soft HEAD~1
```

* **Use case:** You committed too early, forgot to add a commit message description, or want to combine multiple commits into one.

#### B. Keep changes in your Working Directory (unstaged)
If you want to unmake the commit and unstage the files, but keep the actual file modifications in your project:

```bash
git reset HEAD~1
```
*(Alternatively: `git reset --mixed HEAD~1`, as `--mixed` is the default mode)*

* **Use case:** You accidentally committed the wrong files and want to restage only specific files manually using `git add <file>`.

---

### Option 2: Permanently DESTROY the commit and all changes

If you want to completely erase the commit and throw away all file changes associated with it:

```bash
git reset --hard HEAD~1
```

> **Warning:** This permanently deletes any uncommitted changes and overwrites your files back to the state of the previous commit. This cannot be undone with standard Git undo commands.

---

### Undoing Multiple Commits

To undo more than one commit, replace `1` with the number of commits you want to roll back:

* Undo the last 3 commits and keep changes staged:
  ```bash
  git reset --soft HEAD~3
  ```
* Undo the last 3 commits and discard all changes:
  ```bash
  git reset --hard HEAD~3
  ```

Alternatively, you can reset to a specific commit hash:

```bash
git reset --soft <commit-hash>
```

---

### Alternative: Just fixing the last commit

If you only want to change the commit message or add a forgotten file to the last commit, you do not need to reset it. You can amend it:

1. Stage any additional files you forgot:
   ```bash
   git add <forgotten-file>
   ```
2. Amend the previous commit:
   ```bash
   git commit --amend -m "Your updated commit message"
   ```

---

### Safety Net: What if you accidentally used `--hard`?

If you used `git reset --hard` by mistake, you can usually recover the lost commit using `git reflog`:

1. View the commit history log:
   ```bash
   git reflog
   ```
2. Locate the commit hash right before your reset (e.g., `HEAD@{1}`).
3. Restore it:
   ```bash
   git reset --hard HEAD@{1}
   ```
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Stack Overflow](https://stackoverflow.com/questions/927358/how-do-i-undo-the-most-recent-local-commits-in-git).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
