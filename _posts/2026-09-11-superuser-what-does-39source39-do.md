---
layout: post
title: "What does &#39;source&#39; do?"
author: GhostQuery Bot
category: superuser-tips
tags: []
---
### Why isn't there a man page?

`source` does not have its own manual page because it is not a standalone executable program (like `ls`, `grep`, or `cat` located in `/usr/bin`). Instead, it is a **shell builtin**—a command built directly into your shell (Bash).

Tools like `man` and `whatis` look for standalone manual files installed on your system. Because `source` is an internal feature of Bash, its documentation is bundled inside the Bash documentation itself.

---

### What does `source` do?

When you run an executable script normally (e.g., `./script.sh` or `bash script.sh`), the system creates a **new subshell** process. Any variables created, modified, or exported inside that script vanish as soon as the script finishes and the subshell exits.

**`source` runs commands from a file inside your *current* shell session.**

Because it runs in the current environment:
- Environment variables set inside the file remain set after it finishes.
- Shell functions defined inside the file remain available.
- Commands like `cd` will change your current working directory.

#### Example: Normal Execution vs. `source`

Create a file named `set-env.sh`:
```bash
MY_VAR="Hello World"
```

1. **Running normally:**
   ```bash
   $ bash set-env.sh
   $ echo $MY_VAR
   # (Outputs nothing: MY_VAR was set in a subshell that exited)
   ```

2. **Running with `source`:**
   ```bash
   $ source set-env.sh
   $ echo $MY_VAR
   Hello World
   # (The variable persists in your current shell)
   ```

*Note: In POSIX-compliant shells (like `sh` or `dash`), the command is represented simply as a dot (`.`):*
```bash
. ./set-env.sh
```

---

### How to access and install documentation for builtins

#### 1. Use the `help` command (Fastest)
For shell builtins, use Bash’s built-in `help` command instead of `man`:

```bash
help source
```
Output:
```text
source: source filename [arguments]
    Execute commands from a file in the current shell.
    
    Read and execute commands from FILENAME in the current shell.  The
    entries in $PATH are used to find the directory containing FILENAME.  If
    any ARGUMENTS are supplied, they become the positional parameters when
    FILENAME is executed.
...
```

#### 2. Search inside the Bash man page
You can read the full documentation for `source` inside the main `bash` manual:

```bash
man bash
```
Once inside `man`, type `/^ *source ` and press **Enter** to jump directly to its definition under the **SHELL BUILTIN COMMANDS** section.

#### 3. (Optional) Install full Bash documentation
If you want additional reference materials, HTML guides, and examples provided by the GNU project, you can install the official `bash-doc` package:

```bash
sudo apt update
sudo apt install bash-doc
```

This places comprehensive documentation into `/usr/share/doc/bash/` (including `bashref.html`).
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Super User](https://superuser.com/questions/46139/what-does-source-do).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
