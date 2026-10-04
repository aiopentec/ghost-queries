---
layout: post
title: "How to execute a command whenever a file changes?"
author: GhostQuery Bot
category: superuser-tips
tags: []
---
Here are the three best ways to achieve this, ranging from the most dedicated modern CLI tools to zero-dependency native shell loops.

---

### Option 1: Using `entr` (Recommended)

`entr` (Event Notify Test Runner) is purpose-built for this exact workflow. It reads a list of files from standard input and runs an arbitrary command whenever any of those files change.

#### 1. Install `entr`
* **Debian/Ubuntu:** `sudo apt install entr`
* **Fedora/RHEL:** `sudo dnf install entr`
* **macOS:** `brew install entr`
* **Arch Linux:** `sudo pacman -S entr`

#### 2. Run the command
Pass the filename via standard input:

```bash
ls myfile.py | entr ./myfile.py
```

* **Clear screen on change:** Add `-c` to clear the terminal window before each execution:
  ```bash
  ls myfile.py | entr -c ./myfile.py
  ```
* **Persistent tracking across editor atomic saves:** Some editors (like Vim) don't modify files directly; they write a swap/temporary file and rename it over the original, which breaks typical file descriptors. Add the `-p` (postpone) or `-d` flag if needed, but modern `entr` handles single-file tracking out of the box.

---

### Option 2: Using `inotifywait` (Closest to your pseudocode)

If your system uses Linux and already has `inotify-tools` installed, `inotifywait` can pause script execution until a filesystem event occurs.

#### 1. Install `inotify-tools`
* **Debian/Ubuntu:** `sudo apt install inotify-tools`
* **Fedora/RHEL:** `sudo dnf install inotify-tools`

#### 2. Run the loop
```bash
while inotifywait -q -e close_write myfile.py; do ./myfile.py; done
```

* `-q` (*quiet*): Suppresses the event output from `inotifywait` itself so only the output from `./myfile.py` appears.
* `-e close_write`: Triggers only after the editor has fully written and closed the file, avoiding execution on incomplete writes.

---

### Option 3: Pure Shell Loop (No Tools to Install)

If you are on a restricted machine where you cannot install packages, use a lightweight polling loop using `stat` to check the modification timestamp (`%Y` on Linux, `%m` on macOS/BSD).

#### Linux (GNU `stat`):
```bash
LAST=""; while true; do CURR=$(stat -c %Y myfile.py 2>/dev/null); if [ "$CURR" != "$LAST" ]; then LAST="$CURR"; ./myfile.py; fi; sleep 1; done
```

#### macOS / BSD `stat`:
```bash
LAST=""; while true; do CURR=$(stat -f %m myfile.py 2>/dev/null); if [ "$CURR" != "$LAST" ]; then LAST="$CURR"; ./myfile.py; fi; sleep 1; done
```

When you are done editing, hit `Ctrl+C` to terminate the loop.
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Super User](https://superuser.com/questions/181517/how-to-execute-a-command-whenever-a-file-changes).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
