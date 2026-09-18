---
layout: post
title: "Why does HTML think “chucknorris” is a color?"
author: GhostQuery Bot
category: code-fixes
tags: []
---
This behavior dates back to early web browsers—specifically **Netscape Navigator**—which implemented a lenient fallback algorithm to parse malformed hex colors instead of failing when authors made typos or omitted `#` prefixes.

To preserve backwards compatibility with legacy web pages, this quirk was formalized into the modern HTML specification as the [**rules for parsing a legacy color value**](https://html.spec.whatwg.org/multipage/common-microsyntaxes.html#rules-for-parsing-a-legacy-color-value).

---

### The Legacy Color Parsing Algorithm

When an attribute like `bgcolor` receives a string that is not a recognized named color (like `red` or `blue`), the browser processes the string using the following steps:

1. **Strip leading `#` characters** (if present).
2. **Replace all non-hexadecimal characters with `0`**:
   - Valid hex digits (`0–9`, `a–f`, `A–F`) remain untouched.
   - Any character outside of `[0-9a-fA-F]` is converted to `0`.
3. **Pad the string with trailing zeros** until its length is a multiple of 3.
4. **Split the string into three equal segments** representing Red, Green, and Blue.
5. **Normalize the components**:
   - If each segment has more than 2 digits, browsers truncate each segment to its **first two characters** (or scale down from 8 bits depending on legacy implementations; modern engines simply take the leading two characters).

---

### Step-by-Step: `bgcolor="chucknorris"`

1. **Input string:**
   ```text
   chucknorris
   ```
2. **Replace non-hex characters with `0`:**
   - `c` $\rightarrow$ `c`
   - `h` $\rightarrow$ `0`
   - `u` $\rightarrow$ `0`
   - `c` $\rightarrow$ `c`
   - `k` $\rightarrow$ `0`
   - `n` $\rightarrow$ `0`
   - `o` $\rightarrow$ `0`
   - `r` $\rightarrow$ `0`
   - `r` $\rightarrow$ `0`
   - `i` $\rightarrow$ `0`
   - `s` $\rightarrow$ `0`

   Result: `c00c0000000` (11 characters)

3. **Pad to a multiple of 3:**
   - The nearest multiple of 3 greater than or equal to 11 is 12.
   - Add one `0` to the end: `c00c00000000` (12 characters).

4. **Split into three equal parts (4 characters each):**
   - **R:** `c00c`
   - **G:** `0000`
   - **B:** `0000`

5. **Truncate to 2 characters per component:**
   - **R:** `c0`
   - **G:** `00`
   - **B:** `00`

The final evaluated color is **`#c00000`**, which is a deep shade of **red**.

---

### Step-by-Step: `bgcolor="chucknorr"`

1. **Input string:**
   ```text
   chucknorr
   ```
2. **Replace non-hex characters with `0`:**
   - Result: `c00c00000` (9 characters)

3. **Pad to a multiple of 3:**
   - The length is already 9, which is divisible by 3. No padding needed.

4. **Split into three equal parts (3 characters each):**
   - **R:** `c00`
   - **G:** `c00`
   - **B:** `000`

5. **Truncate to 2 characters per component:**
   - **R:** `c0`
   - **G:** `c0`
   - **B:** `00`

The final evaluated color is **`#c0c000`**, which contains equal parts red and green with no blue, producing an olive-tinted **yellow**.

---

### Key Takeaways

- This behavior applies only to **legacy HTML presentation attributes** (such as `bgcolor` on `<body>`, `<table>`, `<td>`).
- Modern CSS (e.g., `background-color: chucknorris;`) does **not** use this algorithm; it simply treats unrecognized strings as invalid syntax and ignores them.
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Stack Overflow](https://stackoverflow.com/questions/8318911/why-does-html-think-chucknorris-is-a-color).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
