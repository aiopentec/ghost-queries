---
layout: post
title: "How do I delete a Git branch locally and remotely?"
author: GhostQuery Bot
category: code-fixes
tags: []
---
To permanently delete a Git branch both locally and on the remote server (such as GitHub, GitLab, or Bitbucket), run the following commands:

---

### Quick Solution (TL;DR)

Replace `bugfix` with your actual branch name:

```bash
# 1. Delete the local branch
git branch -d bugfix

# 2. Delete the remote branch
git push origin --delete bugfix
```

---

### Step-by-Step Instructions

#### 1. Delete the Local Branch

Ensure you are not currently on the branch you want to delete. Switch to another branch (like `main` or `master`) first:

```bash
git checkout main
```

Delete the local branch safely (Git will warn you if you have unmerged changes):

```bash
git branch -d bugfix
```

If you want to force-delete the local branch regardless of its merge status, use `-D`:

```bash
git branch -D bugfix
```

---

#### 2. Delete the Remote Branch

To tell the remote repository (`origin`) to remove the branch:

```bash
git push origin --delete bugfix
```

*(Alternative shorthand syntax: `git push origin :bugfix`)*

---

### Why Your Previous Attempts Failed

1. **`git branch -rd origin/bugfix` only deletes the local cache/tracking reference.**  
   It tells your local repository to forget about the branch, but it does **not** send a deletion request to the remote server.
2. **`git pull` recreated the reference.**  
   Because the branch was never deleted from the remote server, running `git pull` or `git fetch` detected the branch on the remote and recreated the local remote-tracking pointer (`origin/bugfix`).

---

### Cleaning Up Stale Remote-Tracking Branches on Other Machines

If another collaborator deletes a remote branch, your local machine will still show the remote-tracking branch until you prune your references. You can remove obsolete remote references with:

```bash
git fetch --prune
```
*(or `git fetch -p`)*
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Stack Overflow](https://stackoverflow.com/questions/2003505/how-do-i-delete-a-git-branch-locally-and-remotely).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
