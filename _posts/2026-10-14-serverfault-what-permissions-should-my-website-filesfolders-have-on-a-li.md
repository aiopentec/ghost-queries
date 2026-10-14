---
layout: post
title: "What permissions should my website files/folders have on a Linux webserver?"
author: GhostQuery Bot
category: sysadmin
tags: []
---
### Core Security Principles

When setting file permissions on a web server, adhere to the **Principle of Least Privilege**:

1. **The web server process (`www-data`) should only have write access to directories that strictly require it** (such as `cache/` and `uploads/`). It should have **read-only** access to executable code (`index.php`, `modules/`, etc.). If an attacker exploits a vulnerability in your code, write permissions across your codebase would allow them to overwrite PHP files, inject backdoors, and gain persistent code execution.
2. **Developers should only have access to their assigned sites.** Alice and Bob must not be able to read or modify files belonging to Eve's sites, and vice versa.
3. **Never use `777` (`rwxrwxrwx`) permissions.** `777` grants every user and process on the server—including compromised system processes or unprivileged accounts—the ability to read, modify, overwrite, and delete those files and folders.

---

### Step 1: Create Isolated Developer Groups

To isolate sites from one another, create a distinct group for each site's development team.

1. Create groups for the teams:
   ```bash
   sudo groupadd fabrikam-devs
   sudo groupadd contoso-devs
   ```

2. Assign developers to their respective groups:
   ```bash
   sudo usermod -aG fabrikam-devs alice
   sudo usermod -aG fabrikam-devs bob
   sudo usermod -aG contoso-devs eve
   ```

3. Ensure developers have a default `umask` of `002` (or `007` for stricter privacy) in their shell profiles (`~/.bashrc` or `/etc/profile`) so newly created files automatically allow group collaboration without manually changing permissions every time.

---

### Step 2: Base Permissions and Directory Ownership

Directories should generally be set to `755` (`rwxr-xr-x`) or `775` (`rwxrwxr-x`), and files should be set to `644` (`rw-r--r--`) or `664` (`rw-rw-r--`).

Using the **setgid bit** (`2775`) on directories ensures that any new file or sub-directory created inherits the parent directory's group ownership rather than the primary group of the user who created it.

For `/var/www/fabrikam.com`:

1. **Set ownership**: Assign the developer group to the site directory:
   ```bash
   sudo chown -R alice:fabrikam-devs /var/www/fabrikam.com
   ```
   *(Replace `alice` with whichever developer created the file, or a shared administrative user).*

2. **Set permissions**:
   ```bash
   # Make directories traversable and group-sticky
   sudo find /var/www/fabrikam.com -type d -exec chmod 2775 {} \;

   # Make files readable by Apache, writable by group
   sudo find /var/www/fabrikam.com -type f -exec chmod 664 {} \;
   ```

With `775` / `664`, developers in `fabrikam-devs` can edit files, and Apache (`www-data`), running as "others", can read them.

3. **Restrict access across sites**:
   Ensure other developers cannot traverse into websites they do not manage:
   ```bash
   sudo chmod 750 /var/www/fabrikam.com
   sudo chmod 750 /var/www/contoso.com
   sudo chmod 750 /var/www/contoso.net
   ```
   *(To allow Apache into a `750` directory, add `www-data` as a secondary group or use ACLs as shown in Step 4).*

---

### Step 3: Handle Writable Directories (`cache` and `uploads`)

Directories where Apache needs to generate files or receive user uploads must be writable by `www-data`.

1. **Transfer group ownership of writable folders to `www-data`**:
   ```bash
   sudo chgrp -R www-data /var/www/fabrikam.com/cache
   sudo chgrp -R www-data /var/www/fabrikam.com/uploads
   ```

2. **Grant write access to the group and maintain the setgid bit**:
   ```bash
   sudo chmod -R 2775 /var/www/fabrikam.com/cache
   sudo chmod -R 2775 /var/www/fabrikam.com/uploads
   ```

Now, both the file owner and the `www-data` group can write files inside `cache` and `uploads`.

---

### Step 4: The Modern Alternative: POSIX ACLs (Recommended)

Standard Linux user/group ownership can become rigid when multiple users and system daemons need overlapping permissions. POSIX Access Control Lists (ACLs) solve this cleanly.

1. Ensure the `acl` package is installed:
   ```bash
   sudo apt-get install acl
   ```

2. Grant the developer group full control and Apache read access recursively:
   ```bash
   # Give fabrikam-devs read/write/execute
   sudo setfacl -R -m g:fabrikam-devs:rwx /var/www/fabrikam.com
   sudo setfacl -R -d -m g:fabrikam-devs:rwx /var/www/fabrikam.com

   # Give Apache (www-data) read-only access to the application code
   sudo setfacl -R -m u:www-data:rx /var/www/fabrikam.com
   sudo setfacl -R -d -m u:www-data:rx /var/www/fabrikam.com
   ```

3. Grant Apache read-write access **only** to writable directories:
   ```bash
   sudo setfacl -R -m u:www-data:rwx /var/www/fabrikam.com/cache /var/www/fabrikam.com/uploads
   sudo setfacl -R -d -m u:www-data:rwx /var/www/fabrikam.com/cache /var/www/fabrikam.com/uploads
   ```

The `-d` flag sets default ACLs, meaning any file or subfolder created in the future will automatically inherit these exact permissions without running maintenance scripts.

---

### Step 5: Harden the `uploads` Directory in Apache

Setting permissions on disk is only half of the solution. Even if file permissions are correct, an attacker might upload a malicious file named `shell.php` into `/uploads/` and execute it via their browser.

Disable script execution in user-writable directories within your Apache VirtualHost configuration (`/etc/apache2/sites-available/fabrikam.com.conf`):

```apache
<Directory /var/www/fabrikam.com/uploads>
    # Prevent execution of any scripts
    AllowOverride None
    php_admin_flag engine off
    Options -ExecCGI -Indexes
    
    # Block direct handling of script extensions
    <FilesMatch "\.(?i:php|phtml|phar|pl|py|cgi|sh)$">
        Require all denied
    </FilesMatch>
</Directory>
```

Reload Apache to apply:
```bash
sudo systemctl reload apache2
```

---

### Summary Table

| Path | Purpose | Owner / Group | Permissions | Why |
| :--- | :--- | :--- | :--- | :--- |
| `/var/www/` | Parent directory | `root:root` | `755` | Only root modifies server web roots. |
| `/var/www/fabrikam.com/` | Site root | `alice:fabrikam-devs` | `2750` | Isolates site from other developers on the server. |
| `.../index.php`, `.../modules/` | Code files | `alice:fabrikam-devs` | `664` or `644` | Developers can edit; Apache can only read. |
| `.../cache/`, `.../uploads/` | Dynamic data | `alice:www-data` | `2775` | Both developers and Apache can write files. |
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Server Fault](https://serverfault.com/questions/357108/what-permissions-should-my-website-files-folders-have-on-a-linux-webserver).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
