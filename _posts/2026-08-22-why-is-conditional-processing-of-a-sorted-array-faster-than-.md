---
layout: post
title: "Why is conditional processing of a sorted array faster than of an unsorted array?"
---
The primary reason for this performance difference is **branch prediction** in modern CPU architectures.

---

### 1. Instruction Pipelining and Branch Prediction

Modern processors use an **instruction pipeline** to execute instructions concurrently. Instead of waiting for one instruction to finish completely before starting the next, the CPU breaks execution down into multiple stages (Fetch, Decode, Execute, Write-back) and processes multiple instructions simultaneously.

When the CPU encounters a conditional branch (like an `if` statement):
* The condition depends on data that is still being fetched or computed.
* To keep the pipeline full and avoid sitting idle, the processor uses hardware known as a **branch predictor** to guess which path the program will take (Taken or Not Taken) before the condition is actually evaluated.
* If the guess is correct, execution continues without interruption.
* If the guess is wrong (**branch misprediction**), the CPU must discard the speculatively executed instructions (a **pipeline flush**), back up, and restart execution down the correct path. This penalty typically costs **10 to 20+ clock cycles** per misprediction.

---

### 2. Sorted Array vs. Unsorted Array

Look at the branch condition:

```cpp
if (data[c] >= 128)
    sum += data[c];
```

#### Sorted Array:
The data values are in non-decreasing order (e.g., `0, 1, ..., 127, 128, 129, ..., 255`):
* For the first half of the array, the condition is consistently `false`.
* For the second half of the array, the condition is consistently `true`.

Pattern: `[F, F, F, F, ..., T, T, T, T]`

The branch predictor quickly learns this pattern. Across 32,768 elements, the branch predictor only mispredicts **once** (at the transition point around `128`). The CPU pipeline stays full and runs at peak efficiency.

#### Unsorted Array:
The values are randomly distributed:

Pattern: `[T, F, T, T, F, F, T, F, ...]`

Because the data is uniformly distributed between `0` and `255`, each element has an independent 50% chance of being `>= 128`. The branch predictor cannot reliably guess the outcome. With a ~50% misprediction rate over millions of iterations, the CPU constantly stalls and flushes its pipeline, resulting in the massive slowdown you observed.

---

### 3. How to Eliminate the Branch Penalty

If you cannot or do not want to sort the data, you can eliminate the branch entirely using **branchless code**.

#### Method A: Arithmetic / Bitwise Tricks
You can replace the `if` statement with a bitmask or boolean conversion:

```cpp
// In C++, the boolean expression evaluates to 1 (true) or 0 (false)
int t = (data[c] >= 128);
sum += t * data[c];
```

Or using bit shifts (for non-negative values):

```cpp
int t = (data[c] - 128) >> 31; // 0 if >= 128, -1 (all 1s) if < 128
sum += ~t & data[c];
```

#### Method B: Conditional Move (`CMOV`)
Modern compilers with optimization flags enabled (`-O2` or `-O3` in GCC/Clang) can often replace simple branch statements with conditional instructions (like `cmov` on x86) that do not branch at all:

```cpp
for (unsigned c = 0; c < arraySize; ++c)
{
    // A ternary operator can be lowered to a conditional move (CMOV) by the compiler
    sum += (data[c] >= 128) ? data[c] : 0;
}
```

With branchless logic, the execution time for the **unsorted** array drops to roughly match the speed of the **sorted** array because the processor no longer incurs branch misprediction penalties.
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Stack Overflow](https://stackoverflow.com/questions/11227809/why-is-conditional-processing-of-a-sorted-array-faster-than-of-an-unsorted-array).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
