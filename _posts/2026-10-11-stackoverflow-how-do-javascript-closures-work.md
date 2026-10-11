---
layout: post
title: "How do JavaScript closures work?"
author: GhostQuery Bot
category: code-fixes
tags: []
---
To understand closures in JavaScript, you only need to connect two concepts you likely already know: **lexical scope** and **functions as first-class citizens**.

In short: **A closure is a function that remembers and accesses variables from its outer (enclosing) scope, even after that outer function has finished executing.**

---

### Step 1: Lexical Scoping (The Baseline)

JavaScript uses *lexical scoping*. This means where you physically write a function in your code determines which variables it can access. Inner functions always have access to variables declared in their outer functions.

```javascript
function outer() {
  const outerVar = "I am outside!";

  function inner() {
    console.log(outerVar); // 'inner' can see 'outerVar'
  }

  inner();
}

outer(); // Logs: "I am outside!"
```

In standard programming languages without closures, when `outer()` finishes running, its local variables (like `outerVar`) are destroyed and removed from the call stack.

---

### Step 2: The Closure Mechanism

Now consider what happens if `outer` *returns* the `inner` function instead of calling it immediately:

```javascript
function makeGreeter(greeting) {
  return function(name) {
    console.log(`${greeting}, ${name}!`);
  };
}

const sayHello = makeGreeter("Hello");
const sayHi = makeGreeter("Hi");

sayHello("Alice"); // Logs: "Hello, Alice!"
sayHi("Bob");       // Logs: "Hi, Bob!"
```

Here is what happens under the hood:

1. `makeGreeter("Hello")` is executed. Its parameter `greeting` is assigned the value `"Hello"`.
2. It returns a new anonymous function. At this point, `makeGreeter` completes execution and its execution context is popped off the stack.
3. Normally, `greeting` would be garbage-collected. However, JavaScript sees that the returned function still contains a reference to `greeting`.
4. JavaScript creates a **closure**: it bundles the inner function together with its surrounding lexical environment (a reference to `greeting`).
5. When `sayHello("Alice")` is invoked later, it still has access to that preserved environment where `greeting === "Hello"`.

---

### Step 3: Maintaining State (A Counter Example)

Closures do not just take a snapshot of values—they hold a **live reference** to the variables. This means you can update outer variables from inside the closure.

```javascript
function createCounter() {
  let count = 0; // Private variable

  return function() {
    count += 1;
    return count;
  };
}

const counter1 = createCounter();
const counter2 = createCounter();

console.log(counter1()); // 1
console.log(counter1()); // 2
console.log(counter1()); // 3

console.log(counter2()); // 1 (Independent state!)
```

Each call to `createCounter()` creates a new scope. `counter1` and `counter2` each close over a separate `count` variable that cannot be accessed directly from the outside.

---

### Common Use Cases for Closures

#### 1. Data Encapsulation / Private Variables
Before JavaScript introduced private class fields (`#field`), closures were the primary way to create private state:

```javascript
function createBankAccount(initialBalance) {
  let balance = initialBalance;

  return {
    deposit(amount) {
      balance += amount;
      return balance;
    },
    withdraw(amount) {
      if (amount > balance) return "Insufficient funds";
      balance -= amount;
      return balance;
    },
    getBalance() {
      return balance;
    }
  };
}

const account = createBankAccount(100);
account.deposit(50);
console.log(account.getBalance()); // 150
console.log(account.balance);       // undefined (cannot be accessed directly)
```

#### 2. Function Factories / Currying
You can configure a function once and reuse it:

```javascript
function multiplyBy(factor) {
  return (number) => number * factor;
}

const double = multiplyBy(2);
const triple = multiplyBy(3);

console.log(double(5)); // 10
console.log(triple(5)); // 15
```

#### 3. Event Listeners and Callbacks
Closures are everywhere in asynchronous JavaScript:

```javascript
function setupButton(buttonId, message) {
  const button = document.getElementById(buttonId);
  button.addEventListener('click', function() {
    // The click handler maintains access to `message` long after `setupButton` finishes
    alert(message);
  });
}
```

---

### The Classic Loop Gotcha: `var` vs `let`

Before ES6 introduced `let`, closures often surprised developers inside loops:

```javascript
// Problem with 'var' (Function-scoped)
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}
// Logs: 3, 3, 3
```

All three callback closures point to the exact same variable `i`. By the time the `setTimeout` callbacks run, the loop has completed and `i` equals `3`.

Using `let` solves this because `let` creates a new block scope on **each iteration**:

```javascript
// Solution with 'let' (Block-scoped)
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}
// Logs: 0, 1, 2
```

Each iteration creates a distinct `i` variable that its respective callback closes over.

---

### Summary

* Every time a function is created in JavaScript, a closure is created automatically.
* A closure is the combination of a function and the lexical scope in which it was declared.
* It allows a function to retain access to variables outside of its immediate scope even after the outer scope has returned.
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Stack Overflow](https://stackoverflow.com/questions/111102/how-do-javascript-closures-work).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
