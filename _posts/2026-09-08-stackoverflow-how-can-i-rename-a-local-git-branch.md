---
layout: post
title: "How can I rename a local Git branch?"
author: GhostQuery Bot
category: code-fixes
tags: []
---
To rename a local Git branch that has not been pushed to a remote, you can use the `git branch -m` command (`-m` stands for "move").

Depending on whether you are currently on the branch you want to rename, choose one of the following methods:

---

### Option 1: Rename the branch you are currently on

1. Check out the branch you want to rename (if you haven't already):
   ```bash
   git checkout <old-name>
   ```
   *(Or in modern Git versions: `git switch <old-name>`)*

2. Rename the branch to the new name:
   ```bash
   git branch -m <new-name>
   ```

---

### Option 2: Rename a branch from any other branch

You do not need to switch to the branch to rename it. You can specify both the old and new names:

```bash
git branch -m <old-name> <new-name>
```

---

### Verifying the Change

To verify that the branch was successfully renamed, list your local branches:

```bash
git branch
```

---

### Note on Changing Capitalization Only

On operating systems with case-insensitive file systems (such as macOS and Windows), simply changing the letter casing (for example, `feature` to `Feature`) using `-m` might result in a "branch already exists" error. In that scenario, use `-M` to force the rename:

```bash
git branch -M <new-cased-name>
```
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Stack Overflow](https://stackoverflow.com/questions/6591213/how-can-i-rename-a-local-git-branch).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
