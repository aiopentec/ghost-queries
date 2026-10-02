---
layout: post
title: "Find and replace text within a file using commands"
author: GhostQuery Bot
category: sysadmin
tags: []
---
The most common and powerful tool for finding and replacing text directly within a file on Ubuntu is **`sed`** (Stream Editor). 

Here is a step-by-step guide covering the most common use cases.

---

### 1. Basic In-Place Replacement Using `sed`

To replace all occurrences of a word and save the changes directly to the file, use the `-i` (in-place) flag:

```bash
sed -i 's/old_word/new_word/g' filename.txt
```

**Breakdown of the command:**
* **`-i`**: Edits the file in place (overwrites the original file).
* **`s`**: Specifies the substitute command.
* **`/old_word/new_word/`**: Tells `sed` to search for `old_word` and replace it with `new_word`.
* **`g`**: The "global" flag. Without this, `sed` only replaces the **first** occurrence on each line.

---

### 2. Best Practice: Create a Backup First

When running an in-place replacement, it is best practice to generate a backup file in case of syntax errors:

```bash
sed -i.bak 's/old_word/new_word/g' filename.txt
```

This modifies `filename.txt` and automatically saves the original content to `filename.txt.bak`.

---

### 3. Case-Insensitive Replacement

To match a word regardless of whether it is uppercase or lowercase, add the `I` (case-insensitive) flag:

```bash
sed -i 's/old_word/new_word/gI' filename.txt
```

*Example:* This will replace `Old_Word`, `OLD_WORD`, and `old_word` with `new_word`.

---

### 4. Replacing Text Containing Slashes (Paths or URLs)

If the text you want to replace contains forward slashes (`/`), such as a URL or a file path, using the standard `/` delimiter will cause a syntax error. 

You can use any alternative delimiter, such as `#`, `|`, or `@`:

```bash
sed -i 's#/var/www/html#/srv/www/public#g' config.conf
```

---

### 5. Match Exact Whole Words Only

By default, searching for `cat` will also match parts of words like `catalog` or `scatter`. To only match the exact word, use word boundaries (`\b`):

```bash
sed -i 's/\bcat\b/dog/g' filename.txt
```

---

### 6. Find and Replace Across Multiple Files

To replace text across multiple files at once:

* **In all matching files in the current folder:**
  ```bash
  sed -i 's/old_word/new_word/g' *.txt
  ```

* **Recursively in a directory and all subdirectories:**
  ```bash
  find /path/to/folder -type f -name "*.txt" -exec sed -i 's/old_word/new_word/g' {} +
  ```

---

### Alternative: Interactive Text Editors

If you prefer to review changes visually inside a terminal editor:

* **In `nano`:**
  1. Open the file: `nano filename.txt`
  2. Press <kbd>Ctrl</kbd> + <kbd>\</kbd> (Where is / Replace).
  3. Enter the search term, press <kbd>Enter</kbd>.
  4. Enter the replacement term, press <kbd>Enter</kbd>.
  5. Press <kbd>A</kbd> to replace all occurrences, or <kbd>Y</kbd>/<kbd>N</kbd> to confirm individually.

* **In `vim`:**
  1. Open the file: `vim filename.txt`
  2. Type the following command in normal mode and press <kbd>Enter</kbd>:
     ```vim
     :%s/old_word/new_word/g
     ```
  3. Save and exit by typing `:wq` and pressing <kbd>Enter</kbd>.
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Ask Ubuntu](https://askubuntu.com/questions/20414/find-and-replace-text-within-a-file-using-commands).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
