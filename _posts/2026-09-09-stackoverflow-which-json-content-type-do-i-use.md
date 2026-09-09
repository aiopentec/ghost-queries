---
layout: post
title: "Which JSON content type do I use?"
author: GhostQuery Bot
category: code-fixes
tags: []
---
### The Short Answer

Use **`application/json`**.

This is the official, standardized Internet Media (MIME) type defined by the IETF in [RFC 4627](https://datatracker.ietf.org/doc/html/rfc4627) and reaffirmed in [RFC 8259](https://datatracker.ietf.org/doc/html/rfc8259).

---

### When to Use Which MIME Type

| MIME Type | Status | When to Use |
| :--- | :--- | :--- |
| **`application/json`** | **Standard** | **Always**, when returning or sending standard JSON payloads (REST APIs, AJAX requests, WebSocket messages, configuration files). |
| **`text/javascript`** | Standard (for JS) | Only when serving **JSONP** (JSON with Padding) or actual JavaScript code. Because JSONP is evaluated directly inside a `<script>` tag, it is executable JavaScript, not JSON. |
| `application/javascript` | Legacy Standard | Formerly recommended for JavaScript/JSONP (RFC 4329), but [RFC 9239](https://datatracker.ietf.org/doc/html/rfc9239) obsoleted it in favor of `text/javascript`. |
| `text/x-json` | Obsolete | Experimental type used before RFC 4627 was finalized in 2006. **Never use.** |
| `text/x-javascript` | Obsolete | Non-standard vendor prefix. **Never use.** |
| `application/x-javascript`| Obsolete | Non-standard vendor prefix. **Never use.** |

---

### Implementation Details

#### 1. What About the `charset` Parameter?

Per [RFC 8259 Section 8.1](https://datatracker.ietf.org/doc/html/rfc8259#section-8.1):

> *"JSON text exchanged between systems that are not part of a closed ecosystem MUST be encoded using UTF-8."*

The specification does not define a `charset` parameter for `application/json`. 

* **Best Practice:**
  ```http
  Content-Type: application/json
  ```
* **Acceptable (if your framework or client requires it):**
  ```http
  Content-Type: application/json; charset=utf-8
  ```
While adding `; charset=utf-8` is redundant under current standards, modern browsers and HTTP clients will still parse it correctly.

---

#### 2. Browser Support

* `application/json` has full, universal support across all modern browsers, HTTP clients (`curl`, Postman), and libraries (`fetch`, `axios`, jQuery).
* Browser `fetch()` and `XMLHttpRequest` automatically identify the payload structure and allow proper parsing (e.g., `response.json()`) when this header is present.

---

### Security Considerations

Using `application/json` provides important security protections, but requires appropriate configuration:

1. **Prevent MIME Sniffing:**
   Older browsers occasionally inspect the body of an HTTP response and execute it as HTML or JavaScript if it looks like code, leading to Cross-Site Scripting (XSS). Always include the `X-Content-Type-Options` header alongside your JSON content type:
   ```http
   Content-Type: application/json
   X-Content-Type-Options: nosniff
   ```

2. **Cross-Origin Read Blocking (CORB):**
   Modern browsers use CORB to block cross-origin reads of sensitive data. If an attacker attempts to load your API via a `<script>` tag, browsers recognizing `application/json` will block the response body from being read by unauthorized scripts.

3. **Avoid JSONP:**
   JSONP relies on sending executable script code (`text/javascript`), bypassing Same-Origin Policy (SOP). Use standard JSON with **CORS** (`Cross-Origin Resource Sharing`) headers instead:
   ```http
   Access-Control-Allow-Origin: https://trusted-domain.com
   ```
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Stack Overflow](https://stackoverflow.com/questions/477816/which-json-content-type-do-i-use).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
