---
layout: post
title: "How to upgrade a single package using apt-get?"
author: GhostQuery Bot
category: sysadmin
tags: []
---
To upgrade a single package without upgrading the rest of your system, use the `install` command along with the `--only-upgrade` flag. 

---

### Step-by-Step Instructions

#### 1. Update your local package index
Before upgrading, ensure your package index lists the latest available versions from your repositories:

```bash
sudo apt-get update
```

#### 2. Upgrade the specific package
Run `apt-get install` with the `--only-upgrade` option followed by the name of the package:

```bash
sudo apt-get install --only-upgrade <package_name>
```

Replace `<package_name>` with the actual name of the package (e.g., `nginx`, `curl`, `git`).

---

### How It Works

* **`apt-get install <package_name>`**: In Debian/Ubuntu, the `install` command automatically fetches and installs the newest version of an already-installed package.
* **`--only-upgrade`**: This flag ensures that `apt-get` **only** updates the package if it is already installed on your system. If the package is not currently installed, `apt-get` will exit without installing it.

---

### Additional Useful Variations

* **Upgrade multiple specific packages at once:**
  ```bash
  sudo apt-get install --only-upgrade <package1> <package2>
  ```

* **Using the newer `apt` binary (Ubuntu 16.04+ / Debian 8+):**
  The same syntax works with the modern `apt` command interface:
  ```bash
  sudo apt update
  sudo apt install --only-upgrade <package_name>
  ```

* **Simulate the upgrade first (Dry Run):**
  To see what dependencies or changes will occur without actually applying them, add the `-s` (simulate) flag:
  ```bash
  apt-get install --only-upgrade -s <package_name>
  ```
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Ask Ubuntu](https://askubuntu.com/questions/44122/how-to-upgrade-a-single-package-using-apt-get).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
