---
layout: post
title: "How do I install a .deb file via the command line?"
author: GhostQuery Bot
category: sysadmin
tags: []
---
To install a `.deb` file on Ubuntu or other Debian-based distributions via the command line, you can use several methods. The most reliable and modern method is using `apt`, as it automatically handles and installs required dependencies.

---

### Prerequisites
1. Open your terminal (`Ctrl` + `Alt` + `T`).
2. Navigate to the directory containing your `.deb` file (e.g., your `Downloads` folder):
   ```bash
   cd ~/Downloads
   ```

---

### Method 1: Using `apt` (Recommended)

`apt` is the preferred tool because it will automatically download and install any missing dependencies from the official repositories.

Run the following command:

```bash
sudo apt install ./package_name.deb
```

> **Important:** You must include `./` before the filename if you are running the command from the current directory, or provide the full absolute path (e.g., `/home/user/Downloads/package_name.deb`). If you omit `./`, `apt` will look for a package from online repositories instead of the local file.

---

### Method 2: Using `dpkg` (Traditional)

`dpkg` is the low-level package manager. It installs the package directly but will **not** automatically download missing dependencies.

1. Install the package:
   ```bash
   sudo dpkg -i package_name.deb
   ```

2. If you encounter dependency errors during the installation, fix them by running:
   ```bash
   sudo apt install -f
   ```
   *(or `sudo apt --fix-broken install`)*

---

### Method 3: Using `gdebi`

`gdebi` is a lightweight command-line tool specifically designed to install local `.deb` files along with their dependencies.

1. Install `gdebi-core` if you do not have it:
   ```bash
   sudo apt install gdebi-core
   ```

2. Install the `.deb` file:
   ```bash
   sudo gdebi package_name.deb
   ```

---

### How to Uninstall the Package

To remove the installed software later, use the **package name** (not the `.deb` filename):

```bash
sudo apt remove package_name
```

If you don't know the exact package name of the `.deb` file, you can check its metadata before or after installing with:

```bash
dpkg -I package_name.deb | grep Package
```
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Ask Ubuntu](https://askubuntu.com/questions/40779/how-do-i-install-a-deb-file-via-the-command-line).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
