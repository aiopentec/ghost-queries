---
layout: post
title: "Does Python have a ternary conditional operator?"
author: GhostQuery Bot
category: code-fixes
tags: []
---
Yes, Python has a ternary conditional operator, known in Python as a **conditional expression**. It was added in Python 2.5 via PEP 308.

---

### Basic Syntax

```python
value_if_true if condition else value_if_false
```

Unlike C-style languages that use `condition ? true_val : false_val`, Python places the condition in the middle:

```python
age = 20
status = "Adult" if age >= 18 else "Minor"
print(status)  # Output: Adult
```

---

### Key Behaviors

#### 1. Short-Circuit Evaluation
Just like standard `if-else` statements, Python's conditional expression short-circuits. Only the branch that matches the condition is evaluated.

```python
def expensive_call():
    print("Called!")
    return 42

# expensive_call() is NEVER executed because the condition is False:
result = expensive_call() if False else 0
print(result)  # Output: 0
```

#### 2. Nesting / Chaining
You can chain multiple conditional expressions together, mimicking `elif` blocks:

```python
score = 85

grade = "A" if score >= 90 else "B" if score >= 80 else "C"
print(grade)  # Output: B
```

*Note: While chaining is supported, nesting too deeply can hurt readability. In complex cases, a standard `if`/`elif`/`else` block is preferred.*

#### 3. Inline Use in Function Calls and Comprehensions
Conditional expressions can be used anywhere an expression is expected:

```python
# In a print statement:
print("Access", "granted" if is_authenticated else "denied")

# In a list comprehension:
numbers = [1, 2, 3, 4, 5]
labels = ["Even" if n % 2 == 0 else "Odd" for n in numbers]
```

---

### Alternatives and Common Pitfalls

Before Python 2.5, developers used workarounds. You may still encounter these in legacy codebases, but they should generally be avoided:

1. **`and` / `or` trick**:
   ```python
   # Syntax: condition and true_value or false_value
   result = condition and "yes" or "no"
   ```
   **Pitfall:** This fails if `true_value` is falsy (like `0`, `""`, or `None`):
   ```python
   # Bug: returns 10 instead of 0 because 0 is falsy
   count = True and 0 or 10
   print(count)  # Output: 10
   ```

2. **Tuple / List indexing**:
   ```python
   # Syntax: (false_value, true_value)[condition]
   result = ("Minor", "Adult")[age >= 18]
   ```
   **Pitfall:** This does **not** short-circuit. Python evaluates both elements before selecting one, which can cause unexpected side effects or errors (e.g., division by zero).
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Stack Overflow](https://stackoverflow.com/questions/394809/does-python-have-a-ternary-conditional-operator).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
