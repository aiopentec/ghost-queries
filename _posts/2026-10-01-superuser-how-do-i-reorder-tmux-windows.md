---
layout: post
title: "How do I reorder tmux windows?"
author: GhostQuery Bot
category: superuser-tips
tags: []
---
In `tmux`, window reordering is handled via either the `move-window` or `swap-window` commands, depending on whether you want to shift into an empty index or swap places with an existing window.

Here are the ways to reorder your windows:

---

### Method 1: Swap with Another Window Index (`swap-window`)

If you want to swap the current window with another index (e.g., swapping your current window with window `0`):

1. Press your prefix key (default: `Ctrl`+`b`), then type `:` to enter the command prompt.
2. Run:
   ```tmux
   swap-window -t 0
   ```

* **To keep your cursor/focus on the window you just moved**, add the `-d` flag:
  ```tmux
  swap-window -d -t 0
  ```

* **To shift one position left or right**, use relative offsets:
  ```tmux
  swap-window -d -t -1   # Move one position to the left
  swap-window -d -t +1   # Move one position to the right
  ```

---

### Method 2: Move into an Unoccupied Index (`move-window`)

If index `0` is currently empty, you can move the current window directly into it:

1. Press `Ctrl`+`b`, then `:`.
2. Run:
   ```tmux
   move-window -t 0
   ```
   *(Shorthand: `movew -t 0`)*

If the target index is already occupied, this command will return an error stating that the index is in use.

---

### Method 3: Automatically Keep Windows Contiguous

In GNU `screen`, moving a window pushes other window numbers down. To achieve contiguous window numbering automatically in `tmux` (so you never have gaps like `0`, `1`, `4`, `5`), add this setting to your configuration:

1. Open `~/.tmux.conf` in your editor.
2. Add the following line:
   ```tmux
   set-option -g renumber-windows on
   ```
3. Reload your config inside tmux: `Ctrl`+`b` `:` followed by `source-file ~/.tmux.conf`.

Now, closing or moving windows will automatically re-index the rest in numerical order. You can also manually trigger a re-index across all windows at any time by running:
```tmux
move-window -r
```

---

### Recommended: Add Keyboard Shortcuts for Reordering

If you reorder windows frequently, you can bind shortcuts in `~/.tmux.conf` to shift windows left and right using keyboard combinations (e.g., `Ctrl`+`Shift`+`Left/Right`):

```tmux
# Move current window one position to the left
bind-key -n C-S-Left swap-window -d -t -1

# Move current window one position to the right
bind-key -n C-S-Right swap-window -d -t +1
```

*(Note: The `-n` flag allows the shortcut to run without pressing your prefix key first.)*
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Super User](https://superuser.com/questions/343572/how-do-i-reorder-tmux-windows).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
