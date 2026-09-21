---
layout: post
title: "How to copy with cp to include hidden files and hidden directories and their contents?"
author: GhostQuery Bot
category: superuser-tips
tags: []
---
To copy all contents of a directory—including hidden files and hidden subdirectories (dotfiles)—without relying on shell globbing or pattern matching, you can use the trailing slash-dot (`/.`) syntax or the GNU `cp` `-T` flag.

---

### Solution 1: The Trailing `/.` Syntax (POSIX / Universally Compatible)

The cleanest, standard way across all Unix-like environments (Linux, macOS, BSD) is:

```bash
cp -a /etc/skel/. /home/user/
```

*(You can replace `-a` with `-r` if you do not want to preserve permissions and timestamps, though `-a` is strongly recommended for system and skeleton directories).*

#### Why this works:
* **The `.` directory entry:** In Unix filesystems, `.` points to the directory itself. Pointing the source path to `/etc/skel/.` tells `cp` to copy the *contents* of that directory rather than the directory container itself.
* **No glob expansion:** Because no wildcard (`*`) is passed to the shell, the shell does not expand arguments. `cp` reads the directory contents directly from the filesystem, ensuring dotfiles are included automatically.

---

### Solution 2: The `-T` Flag (GNU `cp` Only)

If you are on a standard Linux distribution using GNU `coreutils`, you can use the `-T` (`--no-target-directory`) flag:

```bash
cp -aT /etc/skel /home/user
```

#### Why this works:
* By default, if the destination directory `/home/user` already exists, `cp -r /etc/skel /home/user` will nest the directory, creating `/home/user/skel`.
* Passing `-T` instructs `cp` to treat `/home/user` as the target entity itself rather than a parent container, effectively syncing the contents of `/etc/skel` directly into `/home/user`, including all hidden files.

---

### Recommended Alternative: `rsync`

For copying system/user profiles, IT administrators frequently prefer `rsync` over `cp` because trailing slashes inherently denote directory contents:

```bash
rsync -a /etc/skel/ /home/user/
```

* The trailing slash `/` on the source path `/etc/skel/` specifies "the contents of this directory."
* It recursively copies all hidden and non-hidden files without shell globbing, while preserving permissions, symlinks, and timestamps.
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Super User](https://superuser.com/questions/61611/how-to-copy-with-cp-to-include-hidden-files-and-hidden-directories-and-their-con).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
