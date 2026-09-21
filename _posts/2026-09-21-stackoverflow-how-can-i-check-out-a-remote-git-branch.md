---
layout: post
title: "How can I check out a remote Git branch?"
author: GhostQuery Bot
category: code-fixes
tags: []
---
To check out a remote branch and work on it locally, you need to create a local branch that tracks the remote one. 

Follow these steps:

### 1. Fetch the latest branches from the remote
Ensure your local repository has the latest information about remote branches:

```bash
git fetch origin
```

---

### 2. Check out the branch

#### Method A: Using `git switch` (Recommended for Git 2.23+)
Modern versions of Git introduced `git switch`, which automatically detects the remote tracking branch and creates a matching local branch:

```bash
git switch test
```

#### Method B: Using `git checkout`
In most cases, running the following automatically sets up tracking if a local `test` branch does not already exist:

```bash
git checkout test
```

#### Method C: Explicitly create and track (If the above fails)
If running `git checkout test` did nothing, you may already have a local branch with that name, or you have multiple remotes with a `test` branch. You can explicitly create a local branch linked to the remote branch:

```bash
git checkout -b test origin/test
```
*Or using the `--track` shorthand:*
```bash
git checkout --track origin/test
```

---

### Why did `git checkout origin/test` give `* (no branch)`?

When you run `git checkout origin/test`, Git checks out the remote-tracking ref directly instead of creating a local branch. This puts your repository in a **"detached HEAD"** state:

* You are looking at the commit `origin/test` points to, but you are not on any branch.
* Any new commits you make will not belong to a branch and will easily be lost if you switch away.

To exit the detached HEAD state and get back on a proper tracking branch, simply run:

```bash
git switch test
# or
git checkout test
```
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Stack Overflow](https://stackoverflow.com/questions/1783405/how-can-i-check-out-a-remote-git-branch).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
