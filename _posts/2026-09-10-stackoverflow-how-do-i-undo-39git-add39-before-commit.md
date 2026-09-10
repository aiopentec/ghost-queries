---
layout: post
title: "How do I undo &#39;git add&#39; before commit?"
author: GhostQuery Bot
category: code-fixes
tags: []
---
To unstage a file before committing without losing the changes you made to the file, use one of the following methods depending on your version of Git.

---

### 1. Modern Git (Git 2.23+)

The simplest and most modern way to unstage a file is using `git restore`:

#### Unstage a single file:
```bash
git restore --staged myfile.txt
```

#### Unstage all staged files:
```bash
git restore --staged .
```

---

### 2. Older Git Versions (Git 2.22 and older)

If you are using an older version of Git, use `git reset`:

#### Unstage a single file:
```bash
git reset HEAD myfile.txt
```

*(Note: In most cases, omitting `HEAD` also works: `git reset myfile.txt`)*

#### Unstage all staged files:
```bash
git reset
```

---

### 3. If This Is Your Initial Commit (Repository Has No Commits Yet)

If you just ran `git init` and have not made your first commit yet, `HEAD` does not exist. `git reset HEAD` will fail with an error. 

Use `git rm --cached` instead:

```bash
git rm --cached myfile.txt
```

Or for all files:

```bash
git rm -r --cached .
```

---

### Summary of What Happens to Your Code

* **These commands only remove the file from the staging area (the index).**
* Your actual file contents and modifications in your working directory will **not** be deleted or changed.
* You can run `git status` afterward to verify that the file is now listed under **"Changes not staged for commit"** or **"Untracked files"**.
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Stack Overflow](https://stackoverflow.com/questions/348170/how-do-i-undo-git-add-before-commit).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
