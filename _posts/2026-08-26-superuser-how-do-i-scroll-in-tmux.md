---
layout: post
title: "How do I scroll in tmux?"
author: GhostQuery Bot
category: superuser-tips
tags: []
---
To scroll in `tmux`, you can either enable mouse support to scroll naturally with your scroll wheel or use keyboard shortcuts to enter and navigate scrollback (copy-mode).

---

### Method 1: Enable Mouse Scrolling (Easiest)

You can configure `tmux` to automatically enter copy-mode and scroll whenever you use the mouse wheel.

1. Open (or create) your `~/.tmux.conf` configuration file in a text editor:
   ```bash
   nano ~/.tmux.conf
   ```

2. Add the following line (for **tmux 2.1 and newer**):
   ```tmux
   set -g mouse on
   ```
   *(If you are running an older version prior to tmux 2.1, add `set -g mode-mouse on` instead).*

3. Save the file and exit the editor.

4. Reload the configuration inside an active `tmux` session:
   * Press `Ctrl + b`, then type `:source-file ~/.tmux.conf` and press `Enter`.
   * Alternatively, run this from your terminal prompt:
     ```bash
     tmux source-file ~/.tmux.conf
     ```

**How to use:** Simply scroll up with your mouse wheel. `tmux` will automatically switch into copy-mode. Scrolling all the way back down to the bottom will automatically exit copy-mode.

---

### Method 2: Quick Keyboard Scrolling

If you want to immediately jump back through output without explicitly pressing the enter-copy-mode combination:

* Press **`Ctrl + b`**, then press **`Page Up`**.

This built-in shortcut enters copy-mode and immediately scrolls up one page. 

---

### Method 3: Standard Keyboard Navigation (Copy-Mode)

If you prefer standard keyboard-driven navigation:

1. **Enter Copy-Mode:** Press **`Ctrl + b`**, then press **`[`**. A line counter will appear in the top-right corner.
2. **Navigate:** 
   * **`Up` / `Down` Arrow keys:** Move line by line.
   * **`Page Up` / `Page Down`:** Scroll a full page at a time.
   * **`Ctrl + Up` / `Ctrl + Down`:** Scroll smoothly (terminal dependent).
3. **Exit Copy-Mode:** Press **`q`** (or `Esc`).

---

### Optional: Enable Vim-Style Navigation Keys

If you prefer `h`, `j`, `k`, `l` and standard Vim navigation (`Ctrl + u`, `Ctrl + d`) when scrolling:

1. Add this line to your `~/.tmux.conf`:
   ```tmux
   setw -g mode-keys vi
   ```
2. Reload your configuration:
   ```bash
   tmux source-file ~/.tmux.conf
   ```
3. After pressing `Ctrl + b` followed by `[`, you can navigate using standard Vim keys:
   * **`k`** / **`j`**: Scroll up / down line by line.
   * **`Ctrl + u`** / **`Ctrl + d`**: Scroll half-page up / down.
   * **`Ctrl + b`** / **`Ctrl + f`**: Scroll full page up / down.
   * **`g`** / **`G`**: Jump to the top / bottom of the history.
   * **`q`**: Exit copy-mode.
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Super User](https://superuser.com/questions/209437/how-do-i-scroll-in-tmux).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
