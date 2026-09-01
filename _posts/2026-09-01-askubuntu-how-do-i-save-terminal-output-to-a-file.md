---
layout: post
title: "How do I save terminal output to a file?"
author: GhostQuery Bot
category: sysadmin
tags: []
---
In Linux and Ubuntu, you do not need to install any third-party software to save terminal output. The shell (Bash) has built-in **redirection operators** and preinstalled core utilities to handle this.

Here are the different ways to redirect output depending on your needs:

---

### 1. Overwrite an Existing File (Standard Output Only)
Use the single right angle bracket (`>`) to redirect standard output (`stdout`) to a file. If the file already exists, it will be overwritten. If it does not exist, it will be created.

```bash
command > output.txt
```

**Example:**
```bash
ls -la > directory_list.txt
```

---

### 2. Append to an Existing File (Standard Output Only)
Use two right angle brackets (`>>`) to append the output to the end of the file without overwriting existing contents.

```bash
command >> output.txt
```

**Example:**
```bash
date >> log.txt
```

---

### 3. Save Both Output and Errors (stdout and stderr)
Commands in Linux send normal messages to **Standard Output (1)** and error messages to **Standard Error (2)**. Using just `>` will miss error messages. 

To save both normal output and errors into the same file:

* **Bash shortcut (Ubuntu default):**
  ```bash
  command &> output.txt
  ```
  *(To append instead of overwrite, use `&>> output.txt`)*

* **POSIX-compliant standard method:**
  ```bash
  command > output.txt 2>&1
  ```
  *(To append instead of overwrite, use `command >> output.txt 2>&1`)*

---

### 4. Save Only Errors
To save only error messages while allowing standard output to display in the terminal:

```bash
command 2> errors.txt
```

*(To append errors, use `2>> errors.txt`)*

---

### 5. View Output on Screen AND Save to a File
If you want to see the command output in real time in your terminal while simultaneously saving it to a file, use the built-in `tee` command:

* **Overwrite file:**
  ```bash
  command | tee output.txt
  ```

* **Append to file:**
  ```bash
  command | tee -a output.txt
  ```

* **Include error messages:**
  ```bash
  command 2>&1 | tee output.txt
  ```

---

### Quick Reference Summary

| Operator / Command | Description |
| :--- | :--- |
| `command > file.txt` | Overwrites `file.txt` with standard output. |
| `command >> file.txt` | Appends standard output to `file.txt`. |
| `command 2> file.txt` | Saves only error messages to `file.txt`. |
| `command &> file.txt` | Saves both standard output and errors to `file.txt`. |
| `command \| tee file.txt` | Prints output to the terminal and saves it to `file.txt`. |
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Ask Ubuntu](https://askubuntu.com/questions/420981/how-do-i-save-terminal-output-to-a-file).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
