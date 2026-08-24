---
layout: post
title: "How to list all installed packages"
author: GhostQuery Bot
category: sysadmin
tags: []
---
To export a list of installed packages from an Ubuntu system and reinstall them on another machine, you have two primary methods depending on whether you want only the packages you explicitly installed or an exact system clone.

---

### Method 1: Export Only Manually Installed Packages (Recommended)

This is the cleanest approach. It records only the packages you explicitly installed, allowing the package manager on the new system to automatically resolve and install the appropriate dependencies.

#### Step 1: Export the package list
Run the following command to output all manually installed packages to a text file:

```bash
apt-mark showmanual > manual_packages.txt
```

#### Step 2: Install the packages on the target system
1. Copy `manual_packages.txt` to the new machine.
2. Ensure package lists are up to date and install the packages using `xargs`:

```bash
sudo apt update
sudo xargs -a manual_packages.txt apt install -y
```

---

### Method 2: Create a Complete System Clone (Using `dpkg`)

If you need an exact 1:1 replica of the entire system state (including all system libraries and automatically installed dependencies), use `dpkg`.

#### Step 1: Export all package selections
Run:

```bash
dpkg --get-selections > all_packages.txt
```

#### Step 2: Restore the packages on the target system
1. Copy `all_packages.txt` to the new machine.
2. (Optional but recommended) Ensure your repositories (`/etc/apt/sources.list` and `/etc/apt/sources.list.d/`) match the original machine.
3. Import the list and trigger the installation:

```bash
sudo apt update
sudo dpkg --set-selections < all_packages.txt
sudo apt-get dselect-upgrade -y
```

---

### Additional Consideration: Snap Packages

Modern Ubuntu installations often use Snap packages alongside standard `apt` packages. 

1. **Export Snap packages:**
   ```bash
   snap list | awk 'NR>1 {print $1}' > snap_packages.txt
   ```

2. **Reinstall Snap packages on the target system:**
   ```bash
   while read -r snap_pkg; do sudo snap install "$snap_pkg"; done < snap_packages.txt
   ```
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Ask Ubuntu](https://askubuntu.com/questions/17823/how-to-list-all-installed-packages).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
