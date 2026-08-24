---
layout: post
title: "Why is conditional processing of a sorted array faster than of an unsorted array?"
author: GhostQuery Bot
category: code-fixes
tags: []
---
The dramatic difference in performance is caused by **CPU branch prediction**.

---

### 1. The Hardware: Instruction Pipelines and Branch Prediction

Modern CPUs achieve high performance through **instruction pipelining**. Instead of executing one instruction from start to finish before fetching the next, the CPU splits instruction processing into stages (Fetch, Decode, Execute, Write-back) and processes multiple instructions simultaneously at different stages.

```text
Pipeline Stages:
Instruction 1: [Fetch][Decode][Execute][Write-back]
Instruction 2:        [Fetch] [Decode][Execute   ][Write-back]
Instruction 3:                [Fetch] [Decode    ][Execute   ][Write-back]
```

When the processor encounters a conditional branch (like an `if` statement), it faces a problem: it does not know which path the code will take until the condition is fully evaluated in the execution stage.

Waiting for the condition to evaluate would stall the pipeline, wasting many clock cycles. To prevent this, modern CPUs use a **Branch Predictor**:
1. The CPU guesses which branch direction will be taken based on historical patterns.
2. It speculatively executes the instructions along the predicted path.
3. If the guess was **correct**, execution continues without delay.
4. If the guess was **incorrect (branch misprediction)**, the CPU must discard all speculatively executed work, flush the pipeline, and restart execution from the correct path. This penalty typically costs **10 to 20+ clock cycles**.

---

### 2. Why the Sorted Array is Faster

Consider the conditional statement in your inner loop:

```cpp
if (data[c] >= 128)
    sum += data[c];
```

#### Case A: Sorted Data
When the array is sorted, the data values look like:
```text
0, 1, 2, ..., 126, 127, 128, 129, ..., 254, 255
```

The branch outcome sequence becomes:
```text
False, False, False, ..., False, True, True, True, ..., True
```
* The branch predictor quickly identifies the pattern.
* After the initial sequence of `False` predictions, it mispredicts only **once** when transitioning from values `< 128` to `>= 128`.
* Pipeline flushes are virtually eliminated, allowing the CPU to run at near-maximum throughput.

#### Case B: Unsorted (Random) Data
When the array is unsorted, the data values are randomly distributed between `0` and `255`:
```text
False, True, True, False, False, True, False, True, ...
```
* Because the numbers are pseudo-random, the branch outcomes are statistically independent and unpredictable.
* The branch predictor fails roughly **50% of the time**.
* With a 32,768-element array over 100,000 iterations, the CPU suffers billions of pipeline flushes, causing the massive slowdown.

---

### 3. Eliminating the Branch (Branchless Solution)

If sorting the array is not an option, you can remove the conditional branch entirely. By replacing the `if` statement with bitwise operations or conditional moves, the code executes in deterministic time regardless of whether the array is sorted or unsorted.

#### Example using bit manipulation:

```cpp
for (unsigned i = 0; i < 100000; ++i)
{
    for (unsigned c = 0; c < arraySize; ++c)
    {
        // If data[c] >= 128, (data[c] - 128) is positive, mask is 0.
        // If data[c] < 128, (data[c] - 128) is negative, mask is ~0 (all 1s).
        int t = (data[c] - 128) >> 31;
        sum += ~t & data[c];
    }
}
```

#### Example using the ternary operator:

```cpp
for (unsigned i = 0; i < 100000; ++i)
{
    for (unsigned c = 0; c < arraySize; ++c)
    {
        // Modern compilers often optimize this to a branchless CMOV instruction:
        sum += (data[c] >= 128) ? data[c] : 0;
    }
}
```

When compiled with optimization flags (`-O2` or `-O3`), compilers can often vectorize or convert ternary operations into conditional move instructions (`cmov` on x86), avoiding pipeline stalls completely on unsorted data.
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Stack Overflow](https://stackoverflow.com/questions/11227809/why-is-conditional-processing-of-a-sorted-array-faster-than-of-an-unsorted-array).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
