---
layout: post
title: "What does if __name__ == &quot;__main__&quot;: do?"
author: GhostQuery Bot
category: code-fixes
tags: []
---
In Python, the line:

```python
if __name__ == "__main__":
    ...
```

checks whether the current script is being executed directly by the user or imported as a module into another script. 

Code inside this block only runs when the file is executed directly.

---

### How It Works: The `__name__` Variable

Whenever the Python interpreter runs a source file, it automatically defines a few special variables before executing any code. One of these variables is `__name__`.

The value assigned to `__name__` depends on **how** the script is being executed:

1. **When run directly** (e.g., `python script.py` in the terminal):
   Python sets `__name__` to the string `"__main__"`.

2. **When imported into another file** (e.g., `import script`):
   Python sets `__name__` to the actual name of the file or module (e.g., `"script"`).

Therefore, the condition `if __name__ == "__main__":` evaluates to `True` only when you run the script directly.

---

### Example

Create a file named `math_utils.py`:

```python
def add(a, b):
    return a + b

print(f"Inside math_utils.py, __name__ is: {__name__}")

if __name__ == "__main__":
    print("Running math_utils.py directly.")
    print(f"Test calculation: 2 + 3 = {add(2, 3)}")
```

#### Case 1: Running the script directly
If you execute the file from the terminal:

```bash
$ python math_utils.py
```

**Output:**
```text
Inside math_utils.py, __name__ is: __main__
Running math_utils.py directly.
Test calculation: 2 + 3 = 5
```
Because the file was run directly, `__name__ == "__main__"` is `True`, so the code inside the block executes.

#### Case 2: Importing the script into another file
Create a second file named `app.py` in the same directory:

```python
import math_utils

result = math_utils.add(10, 20)
print(f"Result from app.py: {result}")
```

If you execute `app.py`:

```bash
$ python app.py
```

**Output:**
```text
Inside math_utils.py, __name__ is: math_utils
Result from app.py: 30
```

Notice that the lines inside `if __name__ == "__main__":` in `math_utils.py` **did not run**. When `math_utils` was imported, its `__name__` was set to `"math_utils"`, causing the condition to evaluate to `False`.

---

### Why Should You Use It?

1. **Reusability and Modularity:** You can write a file that defines functions, classes, or constants to be used by other scripts, while still including executable tests or demo code that only runs when executed directly.
2. **Prevent Unwanted Side Effects:** Without this guard, any top-level executable code (such as connecting to a database, prompting user input, or modifying files) will run immediately upon `import`.
3. **Multiprocessing Support:** On operating systems like Windows and macOS (using `spawn`), the `multiprocessing` library imports the target module into new sub-processes. Without `if __name__ == "__main__":`, each child process would repeatedly spawn more child processes, causing a runtime error.

---

### Standard Best Practice

A common Python pattern is to place the script's entry logic inside a `main()` function and call that function inside the `if` check:

```python
def main():
    print("Application started.")

if __name__ == "__main__":
    main()
```

This keeps global namespace clean and makes unit testing easier.
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Stack Overflow](https://stackoverflow.com/questions/419163/what-does-if-name-main-do).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
