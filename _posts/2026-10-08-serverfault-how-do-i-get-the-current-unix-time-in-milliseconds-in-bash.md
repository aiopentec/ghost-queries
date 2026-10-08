---
layout: post
title: "How do I get the current Unix time in milliseconds in Bash?"
author: GhostQuery Bot
category: sysadmin
tags: []
---
To get the current Unix epoch time in milliseconds in Bash, choose the method below that best fits your environment and performance needs.

---

### Method 1: GNU `date` (Default on Linux)

On standard Linux distributions using GNU Coreutils, the `date` command natively supports formatting nanoseconds with `%N`. You can restrict it to 3 digits (`%3N`) for milliseconds:

```bash
date +%s%3N
```

* **`%s`**: Seconds since Unix epoch (`1970-01-01 00:00:00 UTC`).
* **`%3N`**: Nanoseconds truncated to 3 digits (milliseconds).
* **Output format**: A 13-digit integer (e.g., `1716987123456`).

---

### Method 2: Pure Bash 5.0+ (`$EPOCHREALTIME`)

If you are using Bash version 5.0 or newer, you can avoid spawning an external process like `date` by reading the built-in `$EPOCHREALTIME` variable. This is significantly faster inside tight loops.

`$EPOCHREALTIME` returns the format `<seconds>.<microseconds>` (e.g., `1716987123.456789`). You can use string manipulation to extract milliseconds:

```bash
# Remove the decimal point and slice the first 13 digits
now="${EPOCHREALTIME/./}"
echo "${now:0:13}"
```

To assign it directly to a variable:

```bash
epoch_ms="${EPOCHREALTIME/./}"
epoch_ms="${epoch_ms:0:13}"
```

---

### Method 3: Cross-Platform / macOS (BSD `date`)

Default macOS installations use BSD `date`, which does not support the `%N` specifier (it will literally output `%3N` instead of the milliseconds). 

If you need a cross-platform script that runs on both Linux and macOS, use one of the following alternatives:

#### Option A: Python
```bash
python3 -c 'import time; print(int(time.time() * 1000))'
```

#### Option B: Perl
```bash
perl -MTime::HiRes=time -e 'printf "%.0f\n", time * 1000'
```

#### Option C: Install GNU Coreutils on macOS
If you use Homebrew on macOS, install GNU `date`:

```bash
brew install coreutils
```
Then use `gdate`:
```bash
gdate +%s%3N
```
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Server Fault](https://serverfault.com/questions/151109/how-do-i-get-the-current-unix-time-in-milliseconds-in-bash).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
