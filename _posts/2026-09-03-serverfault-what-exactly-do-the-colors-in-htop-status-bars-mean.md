---
layout: post
title: "What exactly do the colors in htop status bars mean?"
author: GhostQuery Bot
category: sysadmin
tags: []
---
You can see the exact color definitions at any time from within `htop` by pressing **`F1`** or **`h`** to open the built-in Help screen.

Here is a breakdown of what the colors represent in each meter, along with an explanation of your specific scenario.

---

### 1. Memory (RAM) Bar Colors

By default, the Memory bar is split into the following colors:

* **Green (Used):** Memory consumed by running processes (active user-space allocations).
* **Blue (Buffers):** In-memory block I/O buffers used by the kernel to buffer disk operations.
* **Yellow / Orange (Cache):** Page cache, cached filesystem metadata (inodes, dentries), and files read from disk.
* **Purple / Magenta (Shared):** *(In newer htop versions)* Memory shared between multiple processes (`shmem` / `tmpfs`).

---

### 2. What Your Specific Memory Bar Means

> **Observation:** A small level of green and blue, almost all the remainder is yellow, and swap is completely empty.

* **Green is low:** Your running programs and processes are consuming very little RAM.
* **Yellow is high:** The Linux kernel follows the philosophy that *"unused RAM is wasted RAM."* When physical memory is idle, Linux aggressively caches files, libraries, and disk I/O in the unused space to make future read operations significantly faster.
* **Swap is empty:** The system is under zero memory pressure.

**Conclusion:** Your system is in an optimal, healthy state. The yellow cached memory is **not** locked. If an application requests more memory, the kernel will instantly discard the cached pages and reallocate that memory to the process without any performance penalty.

---

### 3. CPU Bar Colors (Reference)

For reference, the CPU core bars use the following color scheme:

* **Blue:** Low-priority processes (`nice > 0`).
* **Green:** Normal-priority user processes.
* **Red:** Kernel / System time (`sy`).
* **Yellow / Orange:** Hardware IRQ servicing time.
* **Magenta:** SoftIRQ servicing time.
* **Cyan / Grey:** IO-Wait time (waiting on disk/network).
* **Teal / Cyan:** Steal time (CPU cycles stolen by a hypervisor in virtualized environments).
* **Dark Green:** Guest time (running a virtual machine).

---

### 4. Swap Bar Colors (Reference)

* **Red:** Actively used swap space on disk.
* **Black / Empty:** Available swap space.
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Server Fault](https://serverfault.com/questions/180711/what-exactly-do-the-colors-in-htop-status-bars-mean).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
