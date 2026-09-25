---
layout: post
title: "What does &quot;use strict&quot; do in JavaScript, and what is the reasoning behind it?"
author: GhostQuery Bot
category: code-fixes
tags: []
---
`"use strict";` is a directive introduced in ECMAScript 5 (ES5) that enables **Strict Mode** in JavaScript. 

Strict Mode is a restricted variant of JavaScript that intentionally changes standard behavior to prevent errors, improve performance, and eliminate legacy quirks.

---

### 1. How It Works and Syntax

The directive is written as a plain string literal:

```javascript
"use strict";
```

Because it is simply an expression statement containing a string, older JavaScript engines that do not support ES5 will simply evaluate it as an unused string and ignore it without throwing syntax errors.

You can apply Strict Mode at two different scopes:

#### A. File/Script Scope
Placing it at the very top of a script enables strict mode for the entire file:

```javascript
"use strict";
function doSomething() {
  // Strict mode is active here
}
```

*Note: Be cautious when concatenating scripts. If a strict script is concatenated before a non-strict script, the entire combined file becomes strict, which may break older code.*

#### B. Function Scope
Placing it at the beginning of a function body limits strict mode to that specific function:

```javascript
function strictFunction() {
  "use strict";
  // Strict mode is active only inside this function
}

function normalFunction() {
  // Sloppy (non-strict) mode
}
```

---

### 2. The Reasoning Behind Strict Mode

JavaScript was originally designed and implemented in just 10 days. As a result, several design compromises and bug-prone behaviors were baked into the language (often referred to as "sloppy mode"). 

The ECMAScript committee introduced Strict Mode to:

1. **Catch common coding bloopers:** Convert silent failures into runtime exceptions.
2. **Prevent accidental global variables:** Stop variables from leaking into the global namespace.
3. **Facilitate engine optimizations:** Strict mode code can often be optimized more aggressively by JavaScript engines (like V8 or SpiderMonkey) because variable references are statically bound.
4. **Secure the language:** Stop insecure access to global contexts or restricted properties.
5. **Reserve keywords for future ECMAScript versions:** Prohibit names like `interface`, `protected`, `implements`, and `package` so future language features could be added without breaking existing code.

---

### 3. Key Differences: Strict Mode vs. Sloppy Mode

#### A. Accidental Globals Throw Errors
In non-strict mode, assigning a value to an undeclared variable implicitly creates a property on the global object (`window` in browsers). In strict mode, this throws a `ReferenceError`.

```javascript
"use strict";

// ReferenceError: message is not defined
message = "Hello World"; 
```

#### B. Silent Assignment Failures Become Exceptions
In normal JavaScript, attempting to write to a read-only property fails silently. Strict mode throws an explicit `TypeError`.

```javascript
"use strict";

const obj = {};
Object.defineProperty(obj, "readOnlyProp", {
  value: 42,
  writable: false
});

// TypeError: Cannot assign to read only property 'readOnlyProp'
obj.readOnlyProp = 99; 
```

#### C. `this` Coercion is Removed
In regular functions (not methods), non-strict mode coerces `this` to the global object (`window` or `globalThis`) when called without an explicit execution context. In strict mode, `this` remains `undefined`.

```javascript
"use strict";

function showThis() {
  console.log(this);
}

showThis(); // logs `undefined`, not `window`
```
*This prevents accidentally mutating global variables when a constructor function is invoked without the `new` operator.*

#### D. Duplicate Parameter Names are Prohibited
Non-strict mode allows duplicate parameter names, with the last one taking precedence. Strict mode flags this as a syntax error during parsing:

```javascript
"use strict";

// SyntaxError: Duplicate parameter name not allowed in this context
function add(a, a, b) {
  return a + b;
}
```

#### E. Elimination of `with`
The `with` statement changes how variable identifiers are resolved at runtime, confusing optimizing compilers and creating unpredictable variable shadowing. Strict mode bans `with` entirely:

```javascript
"use strict";

// SyntaxError: Strict mode code may not include a with statement
with (Math) {
  x = cos(2);
}
```

#### F. Safer `eval`
In non-strict mode, `eval` can inject variables into the outer surrounding scope. In strict mode, code executed inside `eval()` cannot introduce variables into the surrounding scope:

```javascript
"use strict";

eval("var injectedVar = 10;");

// ReferenceError: injectedVar is not defined
console.log(injectedVar); 
```

---

### 4. Browser Support and Current Relevance

* **Browser Support:** All modern browsers (and legacy browsers back to Internet Explorer 10, Chrome 13, Firefox 4, and Safari 5.1) fully support `"use strict";`.
* **ES6 Modules:** If you write modern JavaScript using ES Modules (`<script type="module">` or `import`/`export` syntax), **strict mode is enabled by default** for the entire module. You do not need to declare `"use strict";`.
* **Classes:** The entire body of any ES6 `class` declaration executes in strict mode automatically.
* **Transpilers:** Tools like Babel, TypeScript, and modern bundlers (Webpack, Vite, Rollup) automatically insert `"use strict";` or handle strict evaluation rules during output compilation.

If you are writing standalone scripts outside of ES modules or classes, manually adding `"use strict";` remains a standard best practice.
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Stack Overflow](https://stackoverflow.com/questions/1335851/what-does-use-strict-do-in-javascript-and-what-is-the-reasoning-behind-it).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
