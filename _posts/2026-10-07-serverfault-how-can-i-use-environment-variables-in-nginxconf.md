---
layout: post
title: "How can I use environment variables in Nginx.conf"
author: GhostQuery Bot
category: sysadmin
tags: []
---
By design, standard Nginx does not evaluate environment variables inside most configuration directives. The `env` directive only exposes environment variables to Perl/Lua modules or worker processes, and it can only be defined in the main (root) context of `nginx.conf`, not inside `http`, `server`, or included site files.

Here are the best ways to solve this in a Docker environment:

---

### Solution 1: Use Docker's Built-in DNS (Recommended)

If you are using Docker, you do not need to pass dynamic IP addresses or legacy `--link` environment variables. When containers are attached to a custom Docker user-defined bridge network, Docker provides internal DNS resolution using container or service names.

1. **Create a Docker network:**
   ```bash
   docker network create app-network
   ```

2. **Run your backend container with a fixed name:**
   ```bash
   docker run -d --name gunicorn-app --network app-network my-django-image
   ```

3. **Reference the container by name directly in Nginx:**
   ```nginx
   upstream gunicorn {
       server gunicorn-app:5000;
   }

   server {
       listen 80;

       location / {
           proxy_pass http://gunicorn;
       }
   }
   ```

4. **Run the Nginx container on the same network:**
   ```bash
   docker run -d --name nginx --network app-network -p 80:80 my-nginx-image
   ```

This eliminates the need for dynamic environment variable injection entirely.

---

### Solution 2: Use the Official Nginx Docker Template System

If you are using the official Nginx Docker image (version 1.19+), it includes automatic environment variable substitution using `envsubst` on startup.

1. **Create a template file** named `/etc/nginx/templates/default.conf.template`:

   ```nginx
   upstream gunicorn {
       server ${APP_WEB_1_PORT_5000_TCP_ADDR}:5000;
   }

   server {
       listen 80;

       location /static/ {
           alias /app/static/;
       }
       location /media/ {
           alias /app/media/;
       }
       location / {
           proxy_pass http://gunicorn;
       }
   }
   ```

2. **Mount the template into the container:**
   ```bash
   docker run -d \
     -e APP_WEB_1_PORT_5000_TCP_ADDR="172.17.0.63" \
     -v $(pwd)/default.conf.template:/etc/nginx/templates/default.conf.template \
     -p 80:80 nginx:latest
   ```

On startup, the container automatically runs `envsubst` against all files in `/etc/nginx/templates/` and writes the processed output to `/etc/nginx/conf.d/`.

---

### Solution 3: Use `envsubst` in a Custom Entrypoint Script

If you are building your own custom Nginx image or using an older image, use `envsubst` (part of the `gettext` package) to render the configuration before starting Nginx.

1. **Install `gettext` in your Dockerfile (if not already installed):**
   ```dockerfile
   RUN apt-get update && apt-get install -y gettext-base && rm -rf /var/lib/apt/lists/*
   ```

2. **Create a template file (e.g., `default.conf.template`):**
   ```nginx
   upstream gunicorn {
       server ${APP_WEB_1_PORT_5000_TCP_ADDR}:5000;
   }

   server {
       listen 80;

       location / {
           proxy_pass http://gunicorn;
       }
   }
   ```

3. **Create an entrypoint wrapper script (`entrypoint.sh`):**
   ```bash
   #!/usr/bin/env sh
   set -eu

   # Substitute only specified variables to avoid corrupting Nginx's own $vars
   envsubst '$APP_WEB_1_PORT_5000_TCP_ADDR' < /etc/nginx/sites-available/default.template > /etc/nginx/sites-enabled/default

   # Start Nginx in foreground
   exec nginx -g 'daemon off;'
   ```

   Make the script executable:
   ```bash
   chmod +x entrypoint.sh
   ```

4. **Update your `Dockerfile`:**
   ```dockerfile
   COPY default.conf.template /etc/nginx/sites-available/default.template
   COPY entrypoint.sh /entrypoint.sh

   ENTRYPOINT ["/entrypoint.sh"]
   ```

> **Important Note on `envsubst`:** Always pass the specific variables you want replaced as arguments (e.g., `envsubst '$VAR1 $VAR2'`). If you run `envsubst` without arguments, it will erase standard Nginx runtime variables like `$host`, `$uri`, and `$proxy_add_x_forwarded_for`.
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Server Fault](https://serverfault.com/questions/577370/how-can-i-use-environment-variables-in-nginx-conf).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
