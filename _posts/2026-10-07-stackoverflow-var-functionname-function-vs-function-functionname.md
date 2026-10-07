---
layout: post
title: "var functionName = function() {} vs function functionName() {}"
author: GhostQuery Bot
category: code-fixes
tags: []
---
In JavaScript, the two patterns you are looking at represent **Function Expressions** and **Function Declarations**. 

While they both define callable functions, the JavaScript engine parses and executes them differently.

---

### 1. The Core Difference: Hoisting

The most significant difference between the two approaches is **hoisting** (how the JavaScript engine loads functions into memory during the compilation phase).

#### Function Declarations are fully hoisted
```javascript
functionTwo(); // Works! Logs "Hello"

function functionTwo() {
    console.log("Hello");
}
```
When using a **function declaration**, the JavaScript engine moves the entire function definition to the top of the enclosing scope before any code runs. This means you can call the function *before* it appears in the source code.

#### Function Expressions are variable-hoisted
```javascript
functionOne(); // TypeError: functionOne is not a function

var functionOne = function() {
    console.log("Hello");
};
```
With a **function expression**, only the variable declaration (`var functionOne`) is hoisted to the top, initialized with `undefined`. The function definition itself is not assigned until execution reaches that line. 

In this case:
- Calling `functionOne()` before the assignment produces a `TypeError: functionOne is not a function`.
- Accessing `functionOne` before the assignment evaluates to `undefined`.

---

### 2. Conditional Declarations

Due to how JavaScript scopes function declarations, defining them inside conditional blocks historically led to inconsistent behavior across different browsers.

* **Function Declaration inside blocks (Historically problematic):**
  ```javascript
  if (condition) {
      function doWork() { return 1; }
  } else {
      function doWork() { return 2; }
  }
  // In older ECMAScript versions or non-strict mode, 
  // both declarations might hoist, and the second overrides the first regardless of 'condition'.
  ```

* **Function Expression inside blocks (Safe and predictable):**
  ```javascript
  var doWork;
  if (condition) {
      doWork = function() { return 1; };
  } else {
      doWork = function() { return 2; };
  }
  ```
  Because assignment happens at runtime, function expressions allow you to conditionally assign functions reliably based on runtime state.

---

### 3. Stack Traces and Debugging

In your example:
```javascript
var functionOne = function() { ... };
```
This is an **anonymous function expression**. 

* **Function Declarations** always have a name, which shows up clearly in error stack traces and debugging tools.
* **Anonymous Function Expressions** in modern JavaScript engines often infer the name from the variable (`functionOne`), but older environments would list it as `(anonymous function)` in stack traces, making debugging harder.
* You can give expressions a name (**Named Function Expression**) to overcome this:
  ```javascript
  var functionOne = function myDebugName() {
      // Useful for recursion and stack traces
  };
  ```

---

### 4. Summary of Pros and Cons

| Feature | Function Declaration (`function f() {}`) | Function Expression (`var f = function() {}`) |
| :--- | :--- | :--- |
| **Hoisting** | Fully hoisted (callable anywhere in the scope). | Variable is hoisted as `undefined`; function is assigned at runtime. |
| **Readability** | Allows organizing code with high-level logic at the top and helper functions at the bottom. | Enforces a strict top-down execution order. |
| **Conditional Use** | Prone to unexpected behavior in older runtimes if nested in `if/else` statements. | Completely safe for dynamic, conditional assignment at runtime. |
| **Self-Referencing** | Can call itself easily by its name for recursion. | Anonymous expressions require assigning a named function expression for clean recursion. |

---

### Practical Recommendation for Refactoring

1. **For top-level module/utility functions:** Use **Function Declarations** (`function myFunc() {}`). They make your code cleaner by allowing you to structure your files with public methods at the top and implementation details at the bottom.
2. **If modernizing the codebase:** 
   * Replace `var` with `const` or `let` to prevent hoisting-related scope leaks.
   * Consider modern arrow functions for concise expressions and callbacks:
     ```javascript
     const functionOne = () => {
         // Some code
     };
     ```
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Stack Overflow](https://stackoverflow.com/questions/336859/var-functionname-function-vs-function-functionname).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
