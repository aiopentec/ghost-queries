---
layout: post
title: "What is the difference between double and single square brackets in bash?"
author: GhostQuery Bot
category: sysadmin
tags: []
---
While both `[` and `[[` are used for conditional testing in Bash, they operate under fundamentally different mechanisms within the shell. 

Here is a technical breakdown of the differences between the two.

---

### 1. Underlying Implementation: Command vs. Keyword

* **`[` (Test Command):** `[` is an alias for the standard `test` utility. It is implemented as a shell built-in in Bash, but also exists as an external binary executable (typically `/usr/bin/[`). Because it behaves like a regular command, Bash processes all arguments passed to `[` using standard shell expansion rules before `[` executes.
* **`[[` (Compound Command / Keyword):** `[[` is a shell keyword (a reserved word). Because it is part of Bash's native syntax, the shell parses everything between `[[` and `]]` as an expression, disabling certain standard shell expansions like word splitting and pathname expansion.

---

### 2. Word Splitting and Quoting Safety

Because `[` is treated as a normal command, unquoted variables that evaluate to empty strings or contain whitespace will cause syntax errors.

#### With `[`:
```bash
STRING=""
[ $STRING != foo ]
# Expands to: [ != foo ]
# Error: bash: [: !=: unary operator expected

STRING="hello world"
[ $STRING != foo ]
# Expands to: [ hello world != foo ]
# Error: bash: [: too many arguments
```
To use `[` safely, you must quote every variable:
```bash
[ "$STRING" != foo ]
```

#### With `[[`:
Word splitting is disabled inside `[[`. It handles empty strings and whitespace safely without quoting:
```bash
STRING=""
[[ $STRING != foo ]]       # Evaluates cleanly to true

STRING="hello world"
[[ $STRING != foo ]]       # Evaluates cleanly to true
```

---

### 3. Pattern Matching and Regular Expressions

`[[` provides advanced string inspection capabilities that do not exist in `[`:

* **Glob Pattern Matching:** You can match against shell globs using `==` or `!=`.
  ```bash
  FILE="backup_2023.tar.gz"
  
  [[ $FILE == *.tar.gz ]]    # Returns 0 (true)
  [ "$FILE" = *.tar.gz ]     # Compares literal string "*.tar.gz" (unless expanded by globbing)
  ```
  *(Note: Quoting the right-hand side in `[[` forces a literal string comparison instead of a pattern match: `[[ $FILE == "*.tar.gz" ]]`)*

* **Regular Expression Matching:** `[[` supports regex evaluation via the `=~` operator, capturing sub-expressions into the `BASH_REMATCH` array:
  ```bash
  IP="192.168.1.50"
  
  if [[ $IP =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
      echo "Valid IP format"
  fi
  ```

---

### 4. Logical Operators and Grouping

* **`[` uses `-a` (AND) and `-o` (OR):**
  These operators are defined by the `test` command, but their behavior is notoriously ambiguous when combined with multiple arguments and is marked obsolescent in POSIX.
  ```bash
  # Inside `[`, use -a / -o, or chain separate tests:
  [ "$A" = "1" -a "$B" = "2" ]
  [ "$A" = "1" ] && [ "$B" = "2" ]
  ```

* **`[[` uses native `&&` and `||`:**
  Within `[[`, standard boolean operators work directly, and parentheses can be used for logical grouping without needing backslash escapes:
  ```bash
  [[ ($A == 1 || $A == 2) && $B == 3 ]]
  ```

---

### 5. Pathname Expansion (Globbing)

* **`[` performs file globbing:**
  If an unquoted parameter expands to a wildcard that matches multiple files in the working directory, `[` fails.
  ```bash
  VAR="*"
  [ $VAR = foo ]
  # Expands to: [ file1 file2 file3 = foo ]
  # Error: [: too many arguments
  ```

* **`[[` disables filename expansion:**
  ```bash
  VAR="*"
  [[ $VAR == foo ]]   # Compares the literal character "*" to "foo" safely.
  ```

---

### Comparison Summary

| Feature | `[` (POSIX / `test`) | `[[` (Bash Extension) |
| :--- | :--- | :--- |
| **Type** | Built-in command / Binary | Shell keyword |
| **Portability** | Universal (POSIX `sh`, `dash`, etc.) | Bash, Zsh, Ksh |
| **Unquoted empty/spaced vars** | Syntax errors | Handled safely |
| **Glob pattern matching** | No | Yes (`==`, `!=`) |
| **Regex matching (`=~`)** | No | Yes |
| **Logical operators** | `-a`, `-o` | `&&`, `||` |
| **Parentheses grouping** | Requires escaping (`\(`, `\)`) | Unescaped (`(`, `)`) |

### When to use which:
* Use **`[`** only if your script is targeting strict POSIX compliance (e.g., using `#!/bin/sh` or running on resource-constrained environments like Alpine Linux `busybox`).
* Use **`[[`** whenever you are writing scripts specifically for Bash (using `#!/bin/bash`), as it prevents common whitespace bugs and simplifies syntax.
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Server Fault](https://serverfault.com/questions/52034/what-is-the-difference-between-double-and-single-square-brackets-in-bash).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
