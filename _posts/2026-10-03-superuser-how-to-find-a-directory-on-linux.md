---
layout: post
title: "How to find a directory on linux?"
author: GhostQuery Bot
category: superuser-tips
tags: []
---
The reason your command failed is due to the syntax of the `find` command. 

In Linux, the first argument to `find` is the **path where you want to start searching**. By typing `find httpdocs -type d`, Linux assumed you wanted to search *inside* a folder named `httpdocs` located in your current working directory. Since that folder didn't exist where you were standing, it returned `No such file or directory`.

Here is how to properly find your directory, along with a few likely locations.

---

### Step 1: Use the Correct `find` Command

To search the entire filesystem starting from the system root (`/`), use:

```bash
find / -type d -name "httpdocs" 2>/dev/null
```

#### Breakdown of the command:
* **`/`**: Tells `find` to start searching from the absolute root of the filesystem.
* **`-type d`**: Restricts results only to directories (ignoring regular files).
* **`-name "httpdocs"`**: Specifies the exact name of the directory you are searching for.
* **`2>/dev/null`**: Silences "Permission denied" warnings for directories your user does not have permission to read.

*(Note: If you are not logged in as the `root` user, prepend `sudo` to search system-protected directories.)*

---

### Step 2: Use `locate` (Faster Alternative)

If searching the whole disk takes too long, you can use `locate`, which searches an indexed database:

1. Update the search database:
   ```bash
   updatedb
   ```
2. Search for the directory:
   ```bash
   locate httpdocs
   ```

---

### Common Locations for `httpdocs` on SUSE / Web Servers

A folder named `httpdocs` is typical of systems managed by **Plesk** or standard SUSE Apache setups. You will almost certainly find it in one of these paths:

* **Plesk standard path:**
  ```text
  /var/www/vhosts/yourdomain.com/httpdocs/
  ```
* **SUSE standard web root:**
  ```text
  /srv/www/htdocs/
  /srv/www/vhosts/yourdomain.com/httpdocs/
  ```

You can test moving directly there using the `cd` command:

```bash
cd /var/www/vhosts/
ls -la
```
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Super User](https://superuser.com/questions/327762/how-to-find-a-directory-on-linux).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
