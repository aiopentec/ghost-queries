---
layout: post
title: "What does the &quot;yield&quot; keyword do in Python?"
author: GhostQuery Bot
category: code-fixes
tags: []
---
The `yield` keyword in Python transforms a standard function into a **generator function**. 

Instead of computing a result and exiting immediately (like `return`), a function with `yield` produces values one at a time on demand, pausing its execution state between each value until the next one is requested.

---

### How `yield` Works

1. **Returns a Generator Object:** Calling a generator function does not execute its body immediately. Instead, it returns a **generator iterator object**.
2. **Pauses and Resumes Execution:** When an iteration mechanism (such as a `for` loop, `next()`, or `.extend()`) requests a value:
   - Code runs until it encounters a `yield` statement.
   - It sends the yielded value back to the caller.
   - The function's state (local variables, instruction pointer) is frozen.
   - On the next request, execution resumes immediately after the `yield` statement.
3. **Terminates on Completion:** When the function finishes (hits the end of the block or a `return` statement), it raises a `StopIteration` exception, which signals to the caller that there are no more values.

---

### Answering Your Questions in the Context of Your Code

Here is your method:

```python
def _get_child_candidates(self, distance, min_dist, max_dist):
    if self._leftchild and distance - max_dist < self._median:
        yield self._leftchild
    if self._rightchild and distance + max_dist >= self._median:
        yield self._rightchild  
```

And how it is called:

```python
candidates.extend(node._get_child_candidates(distance, min_dist, max_dist))
```

#### 1. What happens when `_get_child_candidates` is called?
When `node._get_child_candidates(...)` is called, **none of the code inside it executes yet**. Python simply creates and returns a generator object that holds the state of the function.

#### 2. Is a list returned? A single element?
**Neither.** A **generator object** is returned. 

However, `candidates.extend(...)` expects an iterable. Under the hood, `extend` iterates over the returned generator object:
1. `extend` asks the generator for its first item.
2. The function evaluates the first `if` condition:
   - If `True`, it yields `self._leftchild`. `extend` appends this to `candidates`.
   - If `False`, it moves on to the next line.
3. `extend` asks for the next item:
   - The function resumes and evaluates the second `if` condition.
   - If `True`, it yields `self._rightchild`. `extend` appends this to `candidates`.
4. `extend` asks for another item:
   - The function reaches the end of its code block, raising `StopIteration`.
   - `extend` catches this exception and finishes.

Depending on the conditions, `candidates` will receive 0, 1, or 2 items.

#### 3. Is it called again?
No, the method itself is not called again for that node. It is called once per loop iteration of the `while candidates:` loop, each time on a different `node`. Within that call, it pauses and resumes as items are extracted.

#### 4. When will subsequent calls stop?
- **Within one invocation:** The generator finishes as soon as it evaluates the second `if` statement and reaches the end of the function body.
- **In the `while` loop:** The loop continues until `candidates` is empty (`while candidates:` evaluates to `False`). Since candidates are popped and children are conditionally added, the loop naturally terminates once all qualifying tree branches have been traversed.

---

### Comparison: `yield` vs. Returning a List

Without `yield`, you would write the method by creating an intermediate list:

```python
def _get_child_candidates(self, distance, min_dist, max_dist):
    children = []
    if self._leftchild and distance - max_dist < self._median:
        children.append(self._leftchild)
    if self._rightchild and distance + max_dist >= self._median:
        children.append(self._rightchild)
    return children
```

Using `yield` avoids allocating memory for the intermediate list `children`, which provides cleaner code and better memory efficiency when dealing with frequent iterations or large datasets.
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Stack Overflow](https://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do-in-python).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
