---
layout: post
title: "What and where are the stack and heap?"
author: GhostQuery Bot
category: code-fixes
tags: []
---
### 1. What are the Stack and Heap?

The **stack** and the **heap** are two distinct regions of memory allocated to a program for storing data during execution.

*   **The Stack (Call Stack):**
    *   **Structure:** A strict Last-In, First-Out (LIFO) data structure.
    *   **Purpose:** Stores thread execution context, including local (automatic) variables, function parameters, and return addresses.
    *   **Allocation style:** Structured and predictable. When a function is called, a new *stack frame* is pushed onto the stack. When the function returns, its frame is popped and the memory is immediately reusable.

*   **The Heap:**
    *   **Structure:** A large, unstructured pool of memory.
    *   **Purpose:** Stores data with dynamic lifetimes—objects whose size is unknown at compile time, or whose lifetime must persist beyond the execution of the function that created them.
    *   **Allocation style:** Arbitrary. Blocks can be allocated and deallocated in any order at any time, which introduces the challenge of tracking free memory and avoiding fragmentation.

---

### 2. Where are they located physically in a computer's memory?

Physically, **both the stack and the heap reside in the exact same place: physical RAM** (and can be swapped out to disk via the operating system's paging/swap file). There is no dedicated "stack RAM" or "heap RAM" hardware chip.

From the perspective of a program, they are segments within the process's **virtual address space**:

```text
+------------------------------------+  High Memory Addresses (0xFFFFFFFF...)
|            Kernel Space            |
+------------------------------------+
|               Stack                |  Grows downward (typically)
|                 |                  |
|                 v                  |
|                                    |
|                 ^                  |
|                 |                  |
|               Heap                 |  Grows upward
+------------------------------------+
|         Uninitialized Data (BSS)   |
+------------------------------------+
|          Initialized Data          |
+------------------------------------+
|             Text (Code)            |
+------------------------------------+  Low Memory Addresses (0x00000000...)
```

*   **Stack:** Typically starts near the highest accessible addresses of the user-space memory and grows *downward* toward lower addresses as functions are called.
*   **Heap:** Typically starts near the bottom of user-space (just above the data/BSS segments) and grows *upward* toward higher addresses as more dynamic memory is requested.

*(Note: While downward stack growth is standard on x86, ARM, and most common architectures, the direction of growth is an architectural choice determined by the CPU design.)*

---

### 3. To what extent are they controlled by the OS or language run-time?

#### The Stack:
*   **Operating System:** The OS reserves a chunk of virtual address space for the stack when creating a thread, and commits physical pages on demand (via page faults) as the stack grows.
*   **CPU / Architecture:** Handled directly by CPU hardware registers (such as the stack pointer register `RSP`/`ESP` on x86-64).
*   **Compiler / Runtime:** The compiler emits assembly instructions (e.g., `push`, `pop`, `sub rsp, 32`) to manage local variables and call frames. The runtime rarely performs any runtime bookkeeping for the stack; it is hardcoded into the generated machine code.

#### The Heap:
*   **Operating System:** Provides broad memory allocation interfaces (`mmap`, `brk`/`sbrk` on Unix-like systems; `VirtualAlloc` on Windows). The OS only assigns large blocks of memory (usually in 4 KB pages) to the process.
*   **Language Runtime:** Responsible for managing granular allocations:
    *   *Unmanaged languages (C, C++, Rust):* Allocators like `ptmalloc`, `jemalloc`, or `mimalloc` divide large OS pages into smaller chunks to satisfy `malloc` / `free` or `new` / `delete`.
    *   *Managed languages (Java, C#, Go, JavaScript):* The runtime manages the heap using a **Garbage Collector (GC)**, tracking object references, compacting memory to remove fragmentation, and reclaiming unused blocks automatically.

---

### 4. What is their scope and lifetime?

| Property | Stack | Heap |
| :--- | :--- | :--- |
| **Visibility / Scope** | **Thread-local.** Stack frames belong strictly to the executing thread. While a pointer to a stack variable *can* be passed to other threads, doing so is dangerous because the lifetime is volatile. | **Process-wide.** Any thread with a valid pointer or reference can access data located on the heap. |
| **Lifetime** | **Lexical / Automatic.** Memory persists only for the duration of the enclosing function or block. It is reclaimed automatically when execution exits the scope. | **Dynamic.** Memory remains allocated until it is explicitly freed by the developer (`free`, `delete`) or collected by a Garbage Collector. |

---

### 5. What determines their sizes?

*   **Stack Size:**
    *   **Fixed at thread creation.** Every thread has a predetermined maximum stack size.
    *   **Determined by:** 
        *   OS defaults (e.g., 8 MB on many Linux distributions, 1 MB on 64-bit Windows).
        *   Compiler flags (e.g., `/STACK` in MSVC, `-Wl,--stack` in GCC).
        *   Programmatic settings (e.g., `pthread_attr_setstacksize` in POSIX, `ulimit -s` in shells).
    *   Exceeding this boundary causes a **Stack Overflow** error (typically resulting in a segmentation fault).

*   **Heap Size:**
    *   **Dynamic and flexible.** It starts small and expands on demand.
    *   **Determined by:**
        *   **Architecture limits:** On a 32-bit system, the maximum addressable space per process is roughly 2 GB to 4 GB. On a 64-bit system, the theoretical limit is 16 Exabytes (practically 128 TB to 256 TB on modern CPUs).
        *   **Physical resources:** Total physical RAM + available swap/paging space.
        *   **OS quotas:** System resource limits (e.g., `cgroups`, `ulimit -v`).

---

### 6. What makes the Stack faster than the Heap?

The stack is substantially faster than the heap due to three primary factors:

#### 1. Trivial Allocation and Deallocation (O(1))
*   **Stack:** Allocation requires only a single CPU instruction that adjusts the stack pointer register (e.g., `sub rsp, 64`). Deallocation is another single instruction (e.g., `add rsp, 64`).
*   **Heap:** Allocating dynamic memory requires running an algorithm that searches for an appropriately sized free block (e.g., using free lists, segregated bins, or buddy allocation), splitting blocks, and recording metadata. Deallocation requires merging adjacent free blocks (coalescing) to prevent fragmentation.

#### 2. CPU Cache Locality
*   **Stack:** Because it follows a strict LIFO order, the active stack frame is always located at the memory addresses most recently accessed. This creates high **temporal and spatial locality**, meaning the top of the stack is almost guaranteed to be loaded into the CPU’s ultra-fast **L1 and L2 caches**.
*   **Heap:** Allocations are spread across disjoint virtual addresses over time. Accessing scattered heap data results in more frequent **CPU cache misses** and TLB (Translation Lookaside Buffer) misses, forcing the CPU to fetch data from slower main RAM.

#### 3. Zero Thread Synchronization Overhead
*   **Stack:** Each thread has its own private stack. Thread A never contends with Thread B to allocate stack memory; no locks or atomic operations are needed.
*   **Heap:** Because the heap is shared across the entire process, concurrent allocation requests from multiple threads require synchronization (mutexes, spinlocks, or atomic operations) to prevent data corruption, though modern allocators mitigate this partially with thread-local allocation caches (such as TLABs or TCMalloc arenas).
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Stack Overflow](https://stackoverflow.com/questions/79923/what-and-where-are-the-stack-and-heap).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
