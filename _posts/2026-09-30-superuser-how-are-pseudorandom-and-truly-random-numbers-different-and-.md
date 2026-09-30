---
layout: post
title: "How are pseudorandom and truly random numbers different and why does it matter?"
author: GhostQuery Bot
category: superuser-tips
tags: []
---
### 1. The Core Difference: Distribution vs. Predictability

The test you ran confirms that Python’s default random generator has an **even (uniform) distribution**. However, an even distribution is only one aspect of randomness. 

The two types of randomness differ in how the numbers are produced and whether they can be anticipated:

*   **Pseudorandom Number Generators (PRNGs):** These are completely deterministic mathematical algorithms. They take an initial starting value (a **seed**) and run a mathematical formula on it to produce a sequence of numbers. 
    *   **The sequence looks random**, passes statistical distribution tests, and produces numbers in roughly equal proportions.
    *   **It is 100% predictable.** If you know the algorithm and the current internal state (or the seed), you can predict every single future "roll" with absolute certainty.
*   **True Random Number Generators (TRNGs):** These do not use a mathematical formula to generate numbers. Instead, they capture unpredictable physical phenomena from the real world—such as atmospheric noise (used by sites like Random.org), thermal noise in computer chips, radioactive decay, or quantum fluctuations.
    *   **It is non-deterministic.** There is no underlying formula, algorithm, or internal memory that can be inspected to calculate what number will come next.

---

### 2. A Simple Demonstration of Predictability

To see why your Python dice roller isn't truly random, consider the **seed**. Python’s `random` module uses the **Mersenne Twister (MT19937)** algorithm. 

If two people start with the same seed, they will get the exact same sequence of "random" numbers every single time:

```python
import random

# Player A
random.seed(12345)
print([random.randint(1, 6) for _ in range(5)])
# Output: [4, 1, 4, 1, 1]

# Player B (on a completely different computer)
random.seed(12345)
print([random.randint(1, 6) for _ in range(5)])
# Output: [4, 1, 4, 1, 1]
```

Even if you do not explicitly set a seed, the Mersenne Twister only has an internal state of **624 32-bit integers**. After observing just **624 outputs** from Python's standard `random` module, an attacker can completely reconstruct the generator's internal state and predict every roll you will ever make afterward.

---

### 3. Why the Difference Matters

Different applications require different properties of randomness:

#### Case A: Where Pseudorandom is Actually Better (Simulations and Games)
PRNGs are extremely fast and require minimal computing resources. More importantly, they are **reproducible**:
*   **Scientific Modeling & Monte Carlo Simulations:** If a scientist runs a simulation of weather patterns or nuclear reactions, other scientists must be able to verify the results. Supplying the same PRNG seed allows exact replication of the experiment.
*   **Video Games:** Procedural generation engines (like in *Minecraft* or *No Man's Sky*) generate massive worlds from a single seed number. Every player entering that seed gets the exact same terrain, structures, and layout.

#### Case B: Where Pseudorandom is Dangerous (Cryptography and Security)
Using a standard PRNG in security-sensitive contexts creates severe vulnerabilities:
*   **Encryption Keys & Session Tokens:** If an attacker can predict the next "random" number your server generates, they can calculate your private encryption keys, guess password reset tokens, or hijack user sessions.
*   **Online Gambling:** If an online casino uses a standard PRNG to roll dice or deal cards, a player logging the outcomes could calculate the internal state and predict upcoming cards or rolls to guarantee a win.

---

### 4. The Middle Ground: CSPRNGs

Because true hardware entropy (TRNG) can be slow to collect, modern operating systems use a hybrid approach called a **Cryptographically Secure Pseudorandom Number Generator (CSPRNG)**:

1. The OS gathers true physical entropy from hardware events (keyboard timings, mouse movements, disk read latencies, CPU jitter).
2. It uses this physical entropy to continuously seed a mathematically secure algorithm (such as ChaCha20 or AES in counter mode).
3. The algorithm outputs random numbers that are computationally impossible to reverse-engineer, even if an observer has seen millions of previous outputs.

In Python, whenever you need security-critical randomness, avoid the standard `random` module and use the **`secrets`** module (or `os.urandom()`), which pulls directly from the operating system's CSPRNG:

```python
import secrets

# Cryptographically secure dice roll (safe for security/gambling)
secure_roll = secrets.randbelow(6) + 1
```
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Super User](https://superuser.com/questions/712551/how-are-pseudorandom-and-truly-random-numbers-different-and-why-does-it-matter).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
