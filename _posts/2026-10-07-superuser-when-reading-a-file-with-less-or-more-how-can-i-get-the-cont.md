---
layout: post
title: "When reading a file with `less` or `more`, how can I get the content in colors?"
author: GhostQuery Bot
category: superuser-tips
tags: []
---
To view colors in a terminal pager, you need to address two distinct scenarios:

1. **Viewing output that already contains color codes (ANSI escape sequences):** You need to instruct the pager to interpret those codes rather than escaping them.
2. **Viewing plain text/code files with syntax highlighting:** You need an external tool to analyze the file and inject color codes before passing it to the pager.

Below are the best ways to handle both situations.

---

### Scenario 1: Preserving Existing Colors in `less`

By default, `less` strips or escapes ANSI color sequences, rendering raw codes like `^[[31m`. 

To tell `less` to render colors properly:

1. **Use the `-R` flag:**
   ```bash
   git diff --color | less -R
   ```
   *(Note: Use `-R` instead of `-r`. `-R` preserves ANSI color codes while maintaining correct line-wrapping behavior.)*

2. **Make this the default behavior:**
   Add the following line to your shell configuration file (`~/.bashrc` or `~/.zshrc`):
   ```bash
   export LESS="-R"
   ```
   Apply the changes:
   ```bash
   source ~/.bashrc  # or source ~/.zshrc
   ```

*(Note on `more`: The traditional `more` command has very limited support for ANSI codes. Most Linux distributions alias or symlink `more` to `less`, but if you are using genuine `more`, switch to `less`.)*

---

### Scenario 2: Adding Syntax Highlighting to Files

Plain text files and source code do not contain color codes by default. You have a few options to automatically highlight them.

#### Option A: Use `bat` (Recommended)
[`bat`](https://github.com/sharkdp/bat) is a modern replacement for `cat` that includes syntax highlighting, Git integration, and automatic paging via `less -R`.

1. **Install `bat`:**
   * **Debian/Ubuntu:**
     ```bash
     sudo apt install bat
     ```
     *(Note: On Ubuntu/Debian, the command is named `batcat`. You can alias it by adding `alias bat="batcat"` to your `~/.bashrc`.)*
   * **RHEL/CentOS/Fedora:**
     ```bash
     sudo dnf install bat
     ```
   * **Arch Linux:**
     ```bash
     sudo pacman -S bat
     ```

2. **Usage:**
   ```bash
   bat filename.py
   ```
   If the file exceeds one screen, `bat` automatically pipes the output to `less` with full color support.

---

#### Option B: Enable Syntax Highlighting in `less` via `source-highlight`
If you prefer to keep using the standard `less` command directly, you can configure it to use a preprocessor.

1. **Install GNU `source-highlight`:**
   * **Debian/Ubuntu:**
     ```bash
     sudo apt install source-highlight
     ```
   * **RHEL/Fedora:**
     ```bash
     sudo dnf install source-highlight
     ```

2. **Configure `less` to use the preprocessor:**
   Add these environment variables to your `~/.bashrc` or `~/.zshrc`:
   ```bash
   export LESSOPEN="| /usr/share/source-highlight/src-hilite-lesspipe.sh %s"
   export LESS=" -R "
   ```
   *(Verify the path of `src-hilite-lesspipe.sh` with `which src-hilite-lesspipe.sh` or `dpkg -L source-highlight | grep lesspipe`, as it can vary slightly between distributions).*

3. **Apply the configuration:**
   ```bash
   source ~/.bashrc
   ```

Now, running `less filename.ext` on supported source code or config files will automatically display syntax-highlighted content.

---

#### Option C: Ad-Hoc Highlighting with Pygments
If you have Python installed, you can use Pygments to highlight files on the fly without system-wide configurations:

1. **Install Pygments:**
   ```bash
   pip install pygments
   ```

2. **Pipe to `less -R`:**
   ```bash
   pygmentize filename.json | less -R
   ```
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Super User](https://superuser.com/questions/117841/when-reading-a-file-with-less-or-more-how-can-i-get-the-content-in-colors).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
