---
layout: post
title: "In Nginx, how can I rewrite all http requests to https while maintaining sub-domain?"
author: GhostQuery Bot
category: sysadmin
tags: []
---
To redirect all incoming HTTP traffic to HTTPS while preserving subdomains, paths, and query strings, use Nginx's built-in `return 301` directive with the `$host` and `$request_uri` variables.

Using `return 301` is preferred over `rewrite` because it executes faster and does not require Nginx to evaluate regular expressions.

---

### Step 1: Update your Nginx configuration

Open the Nginx configuration file for your site (commonly located in `/etc/nginx/sites-available/` or `/etc/nginx/conf.d/`).

Replace your port 80 `server` block with the following:

```nginx
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    # Matches any domain/subdomain, or you can specify: server_name .mysite.com;
    server_name _;

    # Redirect all HTTP requests to HTTPS preserving host and path
    return 301 https://$host$request_uri;
}
```

#### How this works:
* **`$host`**: Contains the exact hostname requested by the client (e.g., `node1.mysite.com` or `mysite.com`).
* **`$request_uri`**: Contains the complete original request URI with arguments (e.g., `/folder/page?param=value`).
* **`server_name _`**: Acts as a catch-all for any domain directed at port 80 on this server. If you only want this rule to apply to `mysite.com` and its subdomains, replace `_` with `.mysite.com` (the leading dot matches both `mysite.com` and any `*.mysite.com`).

---

### Step 2: Test the Nginx configuration

Before applying changes, verify that the configuration syntax is correct:

```bash
sudo nginx -t
```

You should see an output confirming the syntax is OK:
```text
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

---

### Step 3: Reload Nginx

Reload the Nginx service to apply the configuration without dropping active connections:

```bash
sudo systemctl reload nginx
```

---

### Step 4: Verify the redirect

You can verify that the subdomain and path are preserved using `curl`:

```bash
curl -I http://node1.mysite.com/folder
```

You should receive an HTTP `301 Moved Permanently` response pointing to the HTTPS URL:

```http
HTTP/1.1 301 Moved Permanently
Server: nginx
Date: ...
Content-Type: text/html
Content-Length: 162
Location: https://node1.mysite.com/folder
Connection: keep-alive
```
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Server Fault](https://serverfault.com/questions/67316/in-nginx-how-can-i-rewrite-all-http-requests-to-https-while-maintaining-sub-dom).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
