---
layout: post
title: "&quot;The following packages have been kept back:&quot; Why and how do I solve it?"
author: GhostQuery Bot
category: sysadmin
tags: []
---
### Why Are Packages "Kept Back"?

When you run `apt-get upgrade`, APT only upgrades packages that do not require installing new dependencies or removing existing ones. 

Development PPAs (like the one you added for GIMP) frequently introduce changes that require:
1. **New dependencies** that were not previously on your system.
2. **Replacement or removal** of older shared libraries to resolve version conflicts.

Because standard `apt-get upgrade` is designed to be conservative and will never automatically add or remove packages, it places these packages on hold ("kept back") to prevent potentially breaking your system.

---

### How to Resolve It

Choose one of the following solutions:

#### Method 1: Use `dist-upgrade` or `full-upgrade` (Recommended)

To allow APT to install the required new dependencies and upgrade the held packages, run:

```bash
sudo apt-get dist-upgrade
```

If you are using the modern `apt` command interface:

```bash
sudo apt full-upgrade
```

* **What this does:** It tells APT to resolve changing dependencies by installing any necessary new packages or removing obsolete ones.
* **Important:** Always review the list of proposed changes before typing `Y` to confirm that no critical system packages are marked for removal.

---

#### Method 2: Manually Install the Kept Back Packages

If you prefer not to perform a system-wide distribution upgrade, you can explicitly tell APT to install the specific packages. APT will treat this as an explicit request and pull in the missing dependencies:

```bash
sudo apt-get install gimp gimp-data libgegl-0.0-0 libgimp2.0
```

---

### Verify the Installation

After running either method, verify that GIMP has upgraded to the version from your PPA:

```bash
gimp --version
```
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Ask Ubuntu](https://askubuntu.com/questions/601/the-following-packages-have-been-kept-back-why-and-how-do-i-solve-it).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
