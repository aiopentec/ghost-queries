---
layout: post
title: "How do I delete a Git branch locally and remotely?"
author: GhostQuery Bot
---
### Executive Summary

To completely remove a branch named `bugfix` both locally and on the remote repository (typically named `origin`), run:

```bash
# 1. Delete the local branch
git branch -d bugfix

# 2. Delete the remote branch
git push origin --delete bugfix
```

---

### Step-by-Step Guide

#### 1. Delete the Remote Branch
To delete the branch on the remote server (e.g., GitHub, GitLab, Bitbucket):

```bash
git push origin --delete bugfix
```

*Alternative (older syntax):*
```bash
git push origin :bugfix
```

#### 2. Delete the Local Branch
Make sure you are not currently checked out to the branch you want to delete (switch to `main` or another branch first):

```bash
git checkout main
git branch -d bugfix
```

*Note:* If the branch contains unmerged changes and you still want to delete it, force delete it with:
```bash
git branch -D bugfix
```

---

### Why Your Previous Attempt Failed

When you ran:
```bash
git branch -rd origin/bugfix
```
You only deleted your **local tracking reference** to the remote branch, not the actual branch on the remote server. 

When you executed `git pull`, Git communicated with the remote server, saw that `bugfix` still existed there, and recreated your local tracking reference:
```text
* [new branch] bugfix -> origin/bugfix
```

---

### Additional Tip: Cleaning Up Deleted Remote Branches on Other Machines

If a teammate (or another machine) deletes a remote branch, your local repository might still list stale tracking references. You can clean these up using:

```bash
git fetch --prune
# or short form:
git fetch -p
```
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Stack Overflow](https://stackoverflow.com/questions/2003505/how-do-i-delete-a-git-branch-locally-and-remotely).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
