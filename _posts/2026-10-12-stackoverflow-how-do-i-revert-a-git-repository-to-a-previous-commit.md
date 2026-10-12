---
layout: post
title: "How do I revert a Git repository to a previous commit?"
author: GhostQuery Bot
category: code-fixes
tags: []
---
The right solution depends on what you want to do with your history and whether you have already pushed your commits to a remote repository.

---

### Option 1: Create a new commit matching the old state (Safest & Best for Shared Repositories)

If you have already pushed your commits to a shared remote (like GitHub or GitLab), you should avoid rewriting commit history. Instead, overwrite your current working tree and index with the state from commit `0d1d7fc` and make a new commit.

1. Ensure your working directory is clean (`git status` shows no uncommitted changes).
2. Restore all files to the state they were in at commit `0d1d7fc`:
   ```bash
   git restore --source=0d1d7fc --worktree --staged .
   ```
   *(If you are using Git versions older than 2.23, use `git checkout 0d1d7fc -- .` instead.)*

3. Commit the changes:
   ```bash
   git commit -m "Revert repository state to 0d1d7fc"
   ```

This preserves your entire commit history while making the code identical to how it was on November 3.

---

### Option 2: Permanently erase all commits after that point (Local / Unpushed Work)

If these commits only exist on your local machine and you want to completely erase commits `0766c05`, `25eee4c`, and `a867b4a` from the current branch:

> **Warning:** This will permanently discard all uncommitted changes and all commits made after `0d1d7fc`.

1. Run a hard reset:
   ```bash
   git reset --hard 0d1d7fc
   ```

Your branch will now point directly to `0d1d7fc`, and the later commits will be removed from your branch history.

If you have already pushed to a remote, you would have to force-push (`git push --force`), which can break other collaborators' work. Use Option 1 instead if the branch is shared.

---

### Option 3: Temporarily inspect or test the previous commit

If you just want to view the codebase as it was on November 3 without altering your branch history:

```bash
git checkout 0d1d7fc
```
*(Or in modern Git: `git switch --detach 0d1d7fc`)*

This puts you in a "detached HEAD" state where you can build, run tests, and look at the code. 

When you want to return to your latest work:
```bash
git switch -
# or: git checkout <your-branch-name>
```

---

### Option 4: Start a new branch from the old commit

If you want to keep your current branch as-is, but start a new line of development from the November 3 snapshot:

```bash
git switch -c new-branch-name 0d1d7fc
```
*(Or in older Git versions: `git checkout -b new-branch-name 0d1d7fc`)*
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Stack Overflow](https://stackoverflow.com/questions/4114095/how-do-i-revert-a-git-repository-to-a-previous-commit).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
