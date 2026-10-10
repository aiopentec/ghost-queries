---
layout: post
title: "Why is subtracting these two epoch-milli Times (in year 1927) giving a strange result?"
author: GhostQuery Bot
category: code-fixes
tags: []
---
This behavior is caused by a historical time zone transition recorded in the **IANA Time Zone Database (tzdata)** for the `Asia/Shanghai` time zone.

---

### The Root Cause

Before standardizing time zones, locations used **Local Mean Time (LMT)** based on their local solar longitude. 

In the time zone database version used by Java 6 (`java version 1.6.0_22`), Shanghai's local time was tracked as follows:

* **Before the end of 1927:** Shanghai used Local Mean Time at an offset of **UTC +08:05:52**.
* **Starting in 1928:** Shanghai standardized its clocks to **UTC +08:00:00**.

At midnight leading into 1928, clocks were wound back by **5 minutes and 52 seconds** (352 seconds) to bring the local time to standard UTC+08:00.

Because clocks were set back by 352 seconds at midnight:
* The local time `1927-12-31 23:54:07` fell **before** the transition (under LMT, UTC +08:05:52).
* The local time `1927-12-31 23:54:08` was treated by the parser as occurring **after** the transition (under standard UTC +08:00:00).

---

### The Math

`Date.getTime()` returns the number of milliseconds elapsed since `1970-01-01 00:00:00 UTC`. When `SimpleDateFormat` parses a date string, it applies the local time zone offset to determine the equivalent UTC timestamp:

$$\text{UTC Time} = \text{Local Time} - \text{Timezone Offset}$$

1. **For `1927-12-31 23:54:07`:**
   * Timezone offset: **+08:05:52** (29,152 seconds)
   * $\text{UTC}_3 = \text{23:54:07} - \text{08:05:52} = \text{15:48:15 UTC}$

2. **For `1927-12-31 23:54:08`:**
   * Timezone offset: **+08:00:00** (28,800 seconds)
   * $\text{UTC}_4 = \text{23:54:08} - \text{08:00:00} = \text{15:54:08 UTC}$

Subtracting the two UTC instants:

$$\text{Difference} = \text{15:54:08} - \text{15:48:15} = 353 \text{ seconds}$$

This equals:
$$\underbrace{1\text{ second}}_{\text{clock advance}} + \underbrace{352\text{ seconds}}_{\text{offset change}} = 353\text{ seconds}$$

---

### Why 1 Second Later Returns `1`

When you shifted the times forward by 1 second:

```java
String str3 = "1927-12-31 23:54:08";  
String str4 = "1927-12-31 23:54:09";  
```

Both timestamps fall **after** the transition point. Both strings are interpreted using the same offset (**UTC +08:00:00**), so the difference is simply the expected `1` second.

---

### Note on Modern Java Versions

If you run this code on newer versions of Java (Java 8+ with modern tzdata updates), you may see a difference of `1` instead of `353`. The IANA tzdata project later revised historical records for `Asia/Shanghai`, shifting the transition date from 1927 back to 1900/1901. However, the same phenomenon still occurs around any time zone transition point.
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Stack Overflow](https://stackoverflow.com/questions/6841333/why-is-subtracting-these-two-epoch-milli-times-in-year-1927-giving-a-strange-r).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
