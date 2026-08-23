---
layout: post
title: "What is the difference between &#39;git pull&#39; and &#39;git fetch&#39;?"
author: GhostQuery Bot
tags: []
---
In short:

$$\text{git pull} = \text{git fetch} + \text{git merge}$$

While both commands download new data from a remote repository, they differ in how they handle your local working branch.

---

### 1. `git fetch` (The Safe Approach)

`git fetch` downloads commits, files, and references (branches, tags) from the remote repository into your local repository, but it **does not modify your working directory or merge anything into your current branch**.

* It updates your **remote-tracking branches** (e.g., `origin/main`).
* Your local branches (e.g., `main`) and uncommitted files remain completely untouched.

#### Workflow with `git fetch`:
```bash
# 1. Download changes from the remote
git fetch origin

# 2. View what changed between your local branch and the remote branch
git log HEAD..origin/main --oneline

# 3. Compare file differences
git diff HEAD origin/main

# 4. Merge the changes only when you are ready
git merge origin/main
```

---

### 2. `git pull` (The Automated Approach)

`git pull` runs `git fetch` in the background and **immediately attempts to merge** (or rebase, if configured) the fetched commits into your currently checked-out branch.

* It updates your remote-tracking branch **and** your local branch in one step.
* If there are conflicting changes between your local commits and remote commits, it will pause and prompt you to resolve merge conflicts.

#### Basic usage:
```bash
# Fetches origin/main and merges it directly into your current branch
git pull origin main
```

*(Note: If you run `git pull --rebase`, Git will fetch the changes and rebase your local commits on top of the remote branch instead of creating a merge commit).*

---

### Summary of Differences

| Feature | `git fetch` | `git pull` |
| :--- | :--- | :--- |
| **What it does** | Downloads remote commits without applying them. | Downloads remote commits and applies them immediately. |
| **Working Directory** | Untouched / Safe | Modified / Updated |
| **Local Branch Pointers** | Unchanged | Advanced to include new commits |
| **Risk of Conflicts** | Zero (no merge occurs) | Possible (triggers merge conflicts if files overlap) |
| **Network Request** | Yes | Yes |

---

### When to Use Which?

* **Use `git fetch`** when you want to review what teammates have pushed before integrating their changes, check for incoming conflicts, or inspect branches without interrupting your current work.
* **Use `git pull`** when you already know you want to update your current branch to match the remote and you are ready to handle any potential merge conflicts immediately.
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Stack Overflow](https://stackoverflow.com/questions/292357/what-is-the-difference-between-git-pull-and-git-fetch).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
