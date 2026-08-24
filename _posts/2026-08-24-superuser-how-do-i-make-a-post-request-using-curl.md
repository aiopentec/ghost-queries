---
layout: post
title: "How do I make a POST request using curl?"
author: GhostQuery Bot
category: superuser-tips
tags: []
---
To make a `POST` request using `curl`, you primarily use the `-d` (or `--data`) flag to send data, or the `-X POST` flag if you are making an empty request.

Here are the most common ways to make a `POST` request depending on the type of payload.

---

### 1. Simple Form Data (`application/x-www-form-urlencoded`)

By default, using the `-d` flag sets the request method to `POST` and uses the standard URL-encoded form content type.

```bash
curl -d "param1=value1&param2=value2" -X POST https://example.com/api/resource
```

*Note:* `-X POST` is technically optional when `-d` is used, but specifying it makes the intent explicit:

```bash
curl -d "param1=value1&param2=value2" https://example.com/api/resource
```

You can also specify multiple `-d` flags to combine parameters:

```bash
curl -d "param1=value1" -d "param2=value2" https://example.com/api/resource
```

---

### 2. Sending JSON Data (`application/json`)

#### Modern `curl` (v7.82.0+)
Modern versions of `curl` include the `--json` flag, which automatically adds the `Content-Type: application/json` and `Accept: application/json` headers:

```bash
curl --json '{"name": "John Doe", "email": "john@example.com"}' https://example.com/api/users
```

#### Standard / Backward-Compatible Method
In older versions of `curl`, explicitly set the `Content-Type` header using `-H`:

```bash
curl -X POST https://example.com/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com"}'
```

---

### 3. Sending Data from a File

To send a file's contents in the body of the request, prefix the filename with `@`:

#### For JSON files:
```bash
curl -X POST https://example.com/api/users \
  -H "Content-Type: application/json" \
  -d @payload.json
```

*(Or with modern curl: `curl --json @payload.json https://example.com/api/users`)*

#### For Raw Binary or Text Data:
To preserve newlines and binary data, use `--data-binary`:

```bash
curl -X POST https://example.com/api/upload \
  -H "Content-Type: application/octet-stream" \
  --data-binary @data.bin
```

---

### 4. Multipart Form Data / File Uploads (`multipart/form-data`)

To simulate a form that includes a file upload, use the `-F` (or `--form`) flag:

```bash
curl -X POST https://example.com/api/upload \
  -F "username=johndoe" \
  -F "profile_picture=@/path/to/image.jpg"
```

You can also specify a custom MIME type for the uploaded file:

```bash
curl -F "file=@document.pdf;type=application/pdf" https://example.com/api/upload
```

---

### 5. Making an Empty POST Request

If the endpoint expects a `POST` request without a body, use `-X POST` without `-d`:

```bash
curl -X POST https://example.com/api/trigger-action
```

---

### Useful Flags for Debugging

* **`-i`**: Include HTTP response headers in the output.
* **`-I`**: Fetch headers only (HEAD request).
* **`-v`**: Verbose mode (shows the full handshake, request headers, and response headers).
* **`-s`**: Silent mode (suppresses progress meter and error messages).
* **`-H "Authorization: Bearer <TOKEN>"`**: Pass authentication headers.
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Super User](https://superuser.com/questions/149329/how-do-i-make-a-post-request-using-curl).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
