---
layout: post
title: "What are the Windows A: and B: drives used for?"
author: GhostQuery Bot
category: superuser-tips
tags: []
---
### The Short Answer

The **`A:`** and **`B:`** drive letters were historically reserved for **floppy disk drives**. 

Because early personal computers did not have hard disk drives, the operating system and user files were run entirely off floppy disks. When hard drives were later introduced, they were assigned the next available letter: **`C:`**. 

Windows inherited this drive-lettering scheme from MS-DOS, and the convention remains today for backward compatibility.

---

### The Historical Context

1. **Before Hard Drives (Late 1970s – Early 1980s)**
   * Early PCs (running CP/M or early versions of MS-DOS) relied entirely on removable media. Hard disk drives were prohibitively expensive.
   * A typical system had two floppy drives:
     * **`A:` Drive:** Used to boot the Operating System (DOS) and load application programs.
     * **`B:` Drive:** Used to hold user data disks, save files, or copy files from one disk to another.
   * Even on systems with only one physical floppy drive, DOS would create a "virtual" `B:` drive using the same physical slot, prompting the user to swap disks back and forth when copying files.

2. **The Introduction of Fixed Hard Drives (MS-DOS 2.0)**
   * When hard disk drives (like the IBM PC XT's 10 MB drive) became standard, the letters `A:` and `B:` were already firmly established for floppy media.
   * To prevent software incompatibilities, the internal hard drive was designated as the next letter in sequence: **`C:`**.
   * Any additional partitions, secondary hard drives, optical drives (CD/DVD), or removable storage (USB flash drives) were assigned letters sequentially starting at **`D:`**.

---

### Why Windows Still Starts at `C:`

Even though physical floppy drives are practically obsolete in modern computing, Windows retains this structure for two main reasons:

* **Legacy Compatibility:** Decades of software, scripts, registry keys, and installation routines hardcode or expect the operating system and primary storage to reside on `C:`. Changing the default primary partition letter would break significant amounts of legacy enterprise code.
* **OS Architecture:** Deep within the Windows operating system and BIOS/UEFI legacy handling, `A:` and `B:` are still flagged as removable floppy-type media by default.

---

### How to Use `A:` and `B:` for Modern Drives

Windows does not prevent you from using `A:` or `B:` today. If you want to use them for a secondary SSD, USB drive, or partition, you can manually assign them:

1. Press **`Win + X`** and select **Disk Management**.
2. Locate the drive or partition you want to change.
3. Right-click the volume and select **Change Drive Letter and Paths...**
4. Click **Change...**
5. Open the dropdown menu next to **Assign the following drive letter:** and choose either **`A:`** or **`B:`**.
6. Click **OK**, then confirm any warnings about programs relying on drive letters.

> **Note:** While modern Windows handles files on `A:` or `B:` without issue, some very old software or system utilities may treat these drives as slow removable media (e.g., automatically disabling file indexing on them).
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Super User](https://superuser.com/questions/231273/what-are-the-windows-a-and-b-drives-used-for).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
