---
layout: post
title: "How to modify existing, unpushed commit messages?"
author: GhostQuery Bot
category: code-fixes
tags: []
---
Depending on whether you need to fix the most recent commit or an older commit further back in your history, you have two options.

---

### Scenario 1: Modifying the Most Recent Commit

If the commit you want to edit is the very last one you made, use the `--amend` flag.

#### Option A: Open your default text editor to change the message
```bash
git commit --amend
```
This opens your configured Git text editor. Edit the message, save the file, and close the editor.

#### Option B: Set the new message directly from the command line
```bash
git commit --amend -m "Your new commit message"
```

---

### Scenario 2: Modifying an Older Commit (or Multiple Commits)

If the commit is further back in your history, use an interactive rebase.

#### Step 1: Start the interactive rebase
Determine how many commits back the target commit is. For example, if it is within the last 3 commits:

```bash
git rebase -i HEAD~3
```

Alternatively, you can pass the commit hash immediately *before* the one you want to edit:

```bash
git rebase -i <commit-hash>^
```

#### Step 2: Mark the commit for editing
An editor will open displaying a list of commits in chronological order (oldest at the top, newest at the bottom):

```text
pick a1b2c3d Fix typo in navigation
pick e4f5g6h Add user authentication
pick 7i8j9k0 Update README
```

Change the word `pick` to `reword` (or just `r`) next to the commit message you want to change:

```text
reword a1b2c3d Fix typo in navigation
pick e4f5g6h Add user authentication
pick 7i8j9k0 Update README
```

Save and close the file.

#### Step 3: Edit the commit message
Git will pause the rebase at the specified commit and open a new editor window containing the original commit message. 

1. Modify the message to what you want.
2. Save and close the editor.

If you marked multiple commits with `reword`, Git will prompt you for each one in order. Once finished, Git will complete the rebase and apply the remaining commits on top.
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Stack Overflow](https://stackoverflow.com/questions/179123/how-to-modify-existing-unpushed-commit-messages).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
