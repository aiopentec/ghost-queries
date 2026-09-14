---
layout: post
title: "What&#39;s the default superuser username/password for postgres after a new install?"
author: GhostQuery Bot
category: sysadmin
tags: []
---
The default superuser name in PostgreSQL is **`postgres`**, and by default, it has **no password set**. 

On Debian and Ubuntu systems, PostgreSQL is configured to use **peer authentication** for local connections. This means PostgreSQL matches your Linux system username to the PostgreSQL username. During installation, an operating system user named `postgres` is automatically created, and only this system user can access the database superuser without a password.

Here is how to access the database, set a password, and create a new superuser.

---

### Step 1: Log in as the `postgres` superuser

To log in, run `psql` as the local `postgres` system user using `sudo`:

```bash
sudo -u postgres psql
```

You will immediately enter the PostgreSQL interactive terminal:

```text
psql (version)
Type "help" for help.

postgres=#
```

---

### Step 2: (Optional) Set a password for the `postgres` user

If you plan to connect using third-party GUI tools (like pgAdmin or DBeaver) or connect over the network, you must assign a password to the `postgres` user.

Run the following command inside the `psql` prompt:

```sql
ALTER USER postgres WITH PASSWORD 'your_secure_password';
```

Or run the interactive command:

```sql
\password postgres
```

Type `\q` and press Enter to exit `psql`.

---

### Step 3: Create a new superuser

You have two options for creating a new superuser:

#### Option A: Using the command line (Easiest)

From your Linux shell, run PostgreSQL's built-in `createuser` wrapper:

```bash
sudo -u postgres createuser --superuser --pwprompt <new_username>
```

You will be prompted to enter and confirm a password for the new user.

#### Option B: Using SQL commands

1. Log into the `psql` console:
   ```bash
   sudo -u postgres psql
   ```
2. Run the `CREATE ROLE` statement:
   ```sql
   CREATE ROLE new_username WITH SUPERUSER LOGIN PASSWORD 'your_secure_password';
   ```
3. Type `\q` to exit.

---

### Step 4: Connecting with the new user

To log in with your newly created user locally via the command line:

```bash
psql -U new_username -d postgres -h localhost -W
```

* `-U`: Specifies the database user.
* `-d`: Specifies the database to connect to (by default, `postgres` exists).
* `-h localhost`: Forces a TCP/IP connection rather than a Unix domain socket, allowing you to use password authentication.
* `-W`: Forces `psql` to prompt for a password.
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Server Fault](https://serverfault.com/questions/110154/whats-the-default-superuser-username-password-for-postgres-after-a-new-install).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
