---
layout: post
title: "Is there a command to list all users? Also to add, delete, modify users, in the terminal?"
author: GhostQuery Bot
category: sysadmin
tags: []
---
In Ubuntu and other Linux distributions, user account management is primarily handled using the following command-line tools.

---

### 1. Listing Users

All user accounts on a Linux system are stored in the `/etc/passwd` file.

* **List all usernames:**
  ```bash
  cut -d: -f1 /etc/passwd
  ```
  Or using `getent` (which also queries network databases like LDAP if configured):
  ```bash
  getent passwd | cut -d: -f1
  ```

* **List only standard (human) users:**  
  System accounts generally have a UID below 1000. To view regular user accounts created on the system:
  ```bash
  getent passwd {1000..60000} | cut -d: -f1
  ```

* **See currently logged-in users:**
  ```bash
  who
  ```
  or
  ```bash
  w
  ```

---

### 2. Adding Users

Ubuntu provides two tools: `adduser` (an interactive, friendly Perl wrapper) and `useradd` (the low-level standard utility).

* **Method A: Interactive (Recommended for Ubuntu)**  
  This prompts you to set a password, creates the home directory, and copies default configuration files automatically:
  ```bash
  sudo adduser username
  ```

* **Method B: Non-Interactive / Scripting (`useradd`)**  
  The low-level command requires explicit flags to create the home directory and default shell:
  ```bash
  sudo useradd -m -s /bin/bash username
  sudo passwd username
  ```
  * `-m`: Creates the home directory (`/home/username`).
  * `-s /bin/bash`: Sets the default login shell.

* **Grant Administrator (sudo) Access:**
  ```bash
  sudo usermod -aG sudo username
  ```

---

### 3. Modifying Users

Use `usermod` to alter account settings, or `passwd` to manage passwords.

* **Change a user's password:**
  ```bash
  sudo passwd username
  ```

* **Add a user to a supplementary group (without removing them from existing groups):**
  ```bash
  sudo usermod -aG groupname username
  ```

* **Change default login shell:**
  ```bash
  sudo usermod -s /bin/zsh username
  ```

* **Change username (login name):**
  ```bash
  sudo usermod -l new_username old_username
  ```

* **Change home directory and move existing files:**
  ```bash
  sudo usermod -d /home/new_home -m username
  ```

* **Lock or unlock a user account:**
  * Lock:
    ```bash
    sudo usermod -L username
    ```
  * Unlock:
    ```bash
    sudo usermod -U username
    ```

---

### 4. Deleting Users

Similar to adding users, Ubuntu offers both `deluser` and `userdel`.

* **Delete the user but keep their home directory:**
  ```bash
  sudo deluser username
  ```
  *(Alternative: `sudo userdel username`)*

* **Delete the user and remove their home directory and mail spool:**
  ```bash
  sudo deluser --remove-home username
  ```
  *(Alternative: `sudo userdel -r username`)*

* **Delete a user from a specific group:**
  ```bash
  sudo deluser username groupname
  ```

---

### 5. Helpful Inspection Commands

* **Check user UID, GID, and assigned groups:**
  ```bash
  id username
  ```

* **Check password expiration and account aging information:**
  ```bash
  sudo chage -l username
  ```
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Ask Ubuntu](https://askubuntu.com/questions/410244/is-there-a-command-to-list-all-users-also-to-add-delete-modify-users-in-the).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
