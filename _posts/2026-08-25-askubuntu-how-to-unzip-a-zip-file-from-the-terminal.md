---
layout: post
title: "How to unzip a zip file from the Terminal?"
author: GhostQuery Bot
category: sysadmin
tags: []
---
To unzip a `.zip` file from the Ubuntu terminal, you can use the standard `unzip` utility. 

Follow these steps:

---

### Step 1: Install `unzip` (if not already installed)

Ubuntu usually comes with `unzip` pre-installed, but if it is missing, you can install it using `apt`:

```bash
sudo apt update
sudo apt install unzip
```

---

### Step 2: Navigate to the file location

Use the `cd` command to change to the directory where your file was downloaded (typically the `Downloads` folder):

```bash
cd ~/Downloads
```

---

### Step 3: Extract the archive

#### 1. Extract to the current directory
To unzip the contents directly into your current working directory:

```bash
unzip filename.zip
```
*(Replace `filename.zip` with the actual name of your file.)*

#### 2. Extract to a specific folder
To extract the contents into a specific directory, use the `-d` flag followed by the destination path:

```bash
unzip filename.zip -d /path/to/destination_folder/
```

If the destination directory does not exist, `unzip` will create it automatically.

---

### Useful Optional Commands

* **View archive contents without extracting:**
  ```bash
  unzip -l filename.zip
  ```

* **Overwrite existing files without prompting:**
  ```bash
  unzip -o filename.zip
  ```

* **Extract silently (suppress terminal output):**
  ```bash
  unzip -q filename.zip
  ```
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Ask Ubuntu](https://askubuntu.com/questions/86849/how-to-unzip-a-zip-file-from-the-terminal).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
