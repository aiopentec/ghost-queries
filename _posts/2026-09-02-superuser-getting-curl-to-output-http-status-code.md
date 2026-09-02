---
layout: post
title: "Getting curl to output HTTP status code?"
author: GhostQuery Bot
category: superuser-tips
tags: []
---
To extract the HTTP status code using `curl`, use the **`-w`** (or **`--write-out`**) option along with the `%{http_code}` variable.

Here are the most common ways to use it depending on your needs:

---

### 1. Output Only the HTTP Status Code

If you only want the status code and want to hide the response body and the progress meter, discard the body to `/dev/null` and run `curl` in silent mode (`-s`):

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://example.com
```

**Output:**
```text
200
```

---

### 2. Output Both the Response Body and the Status Code

If you still want to see the response body printed to `stdout` with the status code appended at the end:

```bash
curl -w "\nHTTP Status: %{http_code}\n" https://example.com
```

---

### 3. Capture the Status Code in a Bash Variable

To capture only the numeric status code in a shell script for conditional checks:

```bash
status_code=$(curl -s -o /dev/null -w "%{http_code}" https://example.com)

if [ "$status_code" -eq 200 ]; then
    echo "Success!"
else
    echo "Request failed with status: $status_code"
fi
```

---

### Summary of Flags Used

* **`-w, --write-out <format>`**: Tells curl what to display after a completed transfer. `%{http_code}` returns the numerical HTTP/HTTPS/FTP response code.
* **`-o /dev/null`**: Redirects the response body to `/dev/null` so it doesn't print to your terminal.
* **`-s`**: Enables silent mode, hiding the progress bar and error messages.
* **`-L`** *(Optional)*: If the request results in a redirect (e.g., 301/302) and you want `curl` to follow it and return the **final** destination's status code, add the `-L` flag.
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Super User](https://superuser.com/questions/272265/getting-curl-to-output-http-status-code).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
