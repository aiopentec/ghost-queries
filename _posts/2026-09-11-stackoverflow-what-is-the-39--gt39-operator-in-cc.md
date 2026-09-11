---
layout: post
title: "What is the &#39;--&gt;&#39; operator in C/C++?"
author: GhostQuery Bot
category: code-fixes
tags: []
---
`-->` is not a single operator in C or C++. It is actually two separate operators written together without a space: the **postfix decrement operator** (`--`) and the **greater-than operator** (`>`).

The condition in the `while` loop:

```c
while (x --> 0)
```

is parsed by the compiler as:

```c
while ((x--) > 0)
```

### How It Works Step-by-Step

1. **Tokenization (Maximal Munch):** 
   According to the C and C++ standards, the compiler's lexer uses the "maximal munch" rule (it consumes the longest possible sequence of characters that forms a valid token). When it encounters `--`, it creates the decrement token `--`, followed by the greater-than token `>`.

2. **Condition Evaluation:**
   `x--` uses postfix decrement. This means:
   - The expression evaluates to the **current value** of `x`.
   - `x` is then decremented by `1`.
   - That original value is compared against `0` using `>`.

3. **Loop Execution:**
   - On the first iteration, `x` starts at `10`.
   - The condition checks `10 > 0` (which is `true`), and `x` becomes `9`.
   - The body executes: `printf("%d ", x);` prints `9`.
   - This continues until `x` is `1`. The condition checks `1 > 0` (`true`), `x` becomes `0`, and the body prints `0`.
   - On the next check, `x` is `0`. The condition checks `0 > 0` (`false`), `x` becomes `-1`, and the loop terminates.

### Why It Compiles

Because whitespace is generally not significant between operators in C and C++, the following statements are completely identical to the compiler:

```c
while (x --> 0)
while (x-- > 0)
while ((x--) > 0)
```

Programmers sometimes format it as `-->` as a visual pun, pronouncing it "while `x` goes to `0`".
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Stack Overflow](https://stackoverflow.com/questions/1642028/what-is-the-operator-in-c-c).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
