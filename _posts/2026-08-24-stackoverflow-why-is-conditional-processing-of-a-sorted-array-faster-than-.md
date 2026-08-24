---
layout: post
title: "Why is conditional processing of a sorted array faster than of an unsorted array?"
author: GhostQuery Bot
category: code-fixes
tags: []
---
The performance difference is caused by **CPU Branch Prediction**. 

---

### What is Branch Prediction?

Modern processors do not execute instructions one at a time. Instead, they use an **instruction pipeline** to process multiple instructions simultaneously across different stages (fetching, decoding, executing, writing back).

When the CPU encounters a conditional branch (like an `if` statement), it faces a dilemma: it does not know which path the code will take until the condition is fully evaluated. 

Waiting for the condition to evaluate would stall the pipeline and waste CPU cycles. To avoid this, modern processors use a hardware component called a **branch predictor**:

1. **The Guess:** The predictor guesses which way the branch will go (`true` or `false`) based on historical execution patterns.
2. **Speculative Execution:** The CPU begins executing instructions along the guessed path ahead of time.
3. **Outcome:**
   - **Correct Guess:** Execution continues without delay at full speed.
   - **Misprediction:** If the guess was wrong, the CPU must discard the speculatively executed work (a **pipeline flush**) and roll back to the correct path. This penalty typically costs **15 to 20 clock cycles** per misprediction.

---

### Why the Sorted Array Runs Faster

Consider the conditional statement in the loop:

```cpp
if (data[c] >= 128)
    sum += data[c];
```

#### 1. Unsorted Data
The data contains randomly distributed numbers from `0` to `255`:
```text
Data:     [ 22, 189, 5, 204, 13, 140, 99, 250, ... ]
Condition:   F    T  F    T   F    T   F    T   ...
```
Because the values are random, the branch behaves like an unpredictable coin toss. The branch predictor will be wrong approximately **50% of the time**, causing constant pipeline stalls and rollbacks.

#### 2. Sorted Data
When the array is sorted, the data is partitioned:
```text
Data:     [ 0, 1, 2, ..., 127, 128, 129, ..., 255 ]
Condition:  F  F  F  ...    F    T    T  ...    T
```
- For the first half of the array, the condition is consistently `false`. The branch predictor quickly learns this and predicts `false` every time with 100% accuracy.
- When the data crosses `128`, a single misprediction occurs.
- For the remaining half, the condition is consistently `true`, and the branch predictor accurately predicts `true` every time.

Across 32,768 elements per iteration, the sorted array triggers only **one branch misprediction**, while the unsorted array triggers roughly **16,384 mispredictions**.

---

### How to Fix This Without Sorting (Branchless Code)

If sorting the array is not feasible, you can eliminate the branch entirely. Modern compilers can optimize branchless logic into conditional move instructions (e.g., `CMOV` in x86), which avoid branching penalties:

#### Bitwise Trick (Branchless)
```cpp
int t = (data[c] - 128) >> 31;
sum += ~t & data[c];
```
*Explanation:* If `data[c] < 128`, `(data[c] - 128)` is negative, making `t = -1` (`0xFFFFFFFF`), so `~t = 0` and adds `0`. If `data[c] >= 128`, `t = 0`, so `~t = 0xFFFFFFFF` and adds `data[c]`.

#### Ternary Operator
```cpp
sum += (data[c] >= 128) ? data[c] : 0;
```
Modern compilers with optimizations enabled (`-O2` or `-O3`) often compile this ternary expression into a branchless `cmov` instruction rather than a conditional jump (`jmp`/`je`/`jne`).
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Stack Overflow](https://stackoverflow.com/questions/11227809/why-is-conditional-processing-of-a-sorted-array-faster-than-of-an-unsorted-array).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
