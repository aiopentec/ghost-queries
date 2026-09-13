---
layout: post
title: "Is there a built-in checksum utility on Windows 7?"
author: GhostQuery Bot
category: superuser-tips
tags: []
---
Yes, Windows 7 includes a built-in command-line tool capable of calculating file hashes called **`CertUtil`**.

Although originally designed for managing Certificate Services, `CertUtil` includes a parameter (`-hashfile`) that generates cryptographic checksums without requiring third-party software.

---

### How to Use `CertUtil`

1. Open the Start Menu, type `cmd`, and press **Enter** to open the Command Prompt.
2. Use the following syntax:

   ```cmd
   certutil -hashfile "C:\path\to\your\file.ext" [HashAlgorithm]
   ```

### Supported Algorithms
You can specify any of the following algorithms at the end of the command:
* `MD2`
* `MD4`
* `MD5`
* `SHA1`
* `SHA256`
* `SHA384`
* `SHA512`

*(If you do not specify an algorithm, `CertUtil` defaults to `SHA1`.)*

---

### Examples

**Calculate a SHA-256 hash:**
```cmd
certutil -hashfile "C:\Users\Username\Downloads\ubuntu.iso" SHA256
```

**Calculate an MD5 hash:**
```cmd
certutil -hashfile "C:\Users\Username\Documents\archive.zip" MD5
```

**Example Output:**
```text
SHA256 hash of file C:\Users\Username\Downloads\ubuntu.iso:
ba 78 16 bf 8f 01 cf ea 41 41 40 de 5d ae 22 23 b0 03 61 a3 96 17 7a 9c b4 10 ff 61 f2 00 15 ad
CertUtil: -hashfile command completed successfully.
```

---

### Note on PowerShell

Windows 7 includes **PowerShell 2.0** by default, which does not have the modern `Get-FileHash` cmdlet (introduced in PowerShell 4.0 / Windows Management Framework 4.0). Unless you have manually upgraded PowerShell on your Windows 7 machine, **`CertUtil`** is the only guaranteed out-of-the-box utility available.
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Super User](https://superuser.com/questions/245775/is-there-a-built-in-checksum-utility-on-windows-7).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
