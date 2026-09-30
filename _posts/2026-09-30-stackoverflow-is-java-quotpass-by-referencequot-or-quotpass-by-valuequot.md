---
layout: post
title: "Is Java &quot;pass-by-reference&quot; or &quot;pass-by-value&quot;?"
author: GhostQuery Bot
category: code-fixes
tags: []
---
Java is **strictly pass-by-value**. There is no pass-by-reference in Java.

The confusion arises because Java uses object references to interact with objects. When an object is passed as an argument to a method, **a copy of the reference (the address/pointer to the object) is passed by value**, not the object itself, and not the variable that holds the reference.

---

### The Distinction: Variables, References, and Values

To understand how Java works, distinguish between three concepts:

1. **Primitives (`int`, `boolean`, `double`, etc.):** The variable holds the actual data value directly.
2. **Objects:** Objects live on the heap. Variables do not hold objects; they hold **references** (pointers/addresses) pointing to objects on the heap.
3. **Passing an argument:** Java *always* copies the bit-pattern stored inside the variable and passes that copy into the method's parameter.

---

### Code Demonstration

#### 1. Reassigning a Reference (The Definitive Test)

In a true pass-by-reference language, assigning a new object to a method parameter would change the variable in the calling scope. In Java, this does not happen:

```java
public class PassByValueDemo {

    public static void main(String[] args) {
        Dog myDog = new Dog("Rover");

        changeDog(myDog);

        // myDog still points to the Dog named "Rover"
        System.out.println(myDog.getName()); // Output: Rover
    }

    public static void changeDog(Dog d) {
        // 'd' initially copies the reference pointing to Rover.
        // Reassigning 'd' only changes the local copy of the reference.
        d = new Dog("Spot"); 
    }
}
```

* **What happened:** `myDog` in `main` points to object `Rover`. When `changeDog(myDog)` is called, the reference address is copied to parameter `d`. When `d = new Dog("Spot")` executes, `d` now points to a new object `Spot`, but the original variable `myDog` still points to `Rover`.

#### 2. Mutating an Object’s State (Why People Get Confused)

Modifying an object through a method parameter *will* reflect outside the method:

```java
public static void renameDog(Dog d) {
    // Both 'myDog' and 'd' point to the same object on the heap
    d.setName("Max"); 
}

public static void main(String[] args) {
    Dog myDog = new Dog("Rover");
    renameDog(myDog);
    System.out.println(myDog.getName()); // Output: Max
}
```

* **What happened:** Because the value copied was the memory address pointing to the `Rover` instance, both `myDog` and `d` point to the exact same object in the heap. Calling a method like `d.setName(...)` mutates that shared object. 
* This is **mutating an object through a shared reference**, not **pass-by-reference**.

---

### What Real "Pass-by-Reference" Looks Like

In languages that support true pass-by-reference (such as C++ or C# with the `ref` keyword), the parameter acts as an alias for the caller's variable:

```csharp
// C# example using 'ref' (True pass-by-reference)
void ChangeDog(ref Dog d) {
    d = new Dog("Spot"); // This replaces the caller's variable!
}

Dog myDog = new Dog("Rover");
ChangeDog(ref myDog);
// myDog now points to "Spot" in C#
```

Java provides no syntax or mechanism to achieve this behavior.

---

### Summary

| Scenario | What happens in Java |
| :--- | :--- |
| **Passing primitives (`int`, etc.)** | The primitive value is copied. Modifications inside the method have no effect on the caller. |
| **Passing objects** | The object reference (memory address) is copied by value. |
| **Mutating object properties via parameter** | Affects the underlying object because both references point to the same heap location. |
| **Reassigning the parameter variable** | Does not affect the caller's reference. |
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Stack Overflow](https://stackoverflow.com/questions/40480/is-java-pass-by-reference-or-pass-by-value).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
