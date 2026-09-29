---
layout: post
title: "Why is my crontab not working, and how can I troubleshoot it?"
author: GhostQuery Bot
category: sysadmin
tags: []
---
When a cron job fails to run as expected, it is almost always due to differences between your interactive shell environment and the execution environment provided by the `cron` daemon.

Below is a systematic guide to diagnosing the failure, followed by the most common causes and their fixes.

---

### Step 1: Diagnose the Failure

Before changing arbitrary settings, determine if the job is running at all and inspect its output.

#### 1. Check if the Cron Service is Running
Ensure the daemon is active on your system:
* **Debian/Ubuntu:**
  ```bash
  systemctl status cron
  ```
* **RHEL/CentOS/Rocky Linux:**
  ```bash
  systemctl status crond
  ```
If it is inactive, start and enable it:
```bash
sudo systemctl enable --now cron   # or crond
```

#### 2. Check the System Logs
Cron logs every attempt to execute a scheduled task. Look for entries indicating whether the job was triggered:
* **`systemd` Journal:**
  ```bash
  journalctl -u cron -e       # Debian/Ubuntu
  journalctl -u crond -e      # RHEL/CentOS
  ```
* **Log Files:**
  * Debian/Ubuntu: `/var/log/syslog` (filter with `grep CRON`)
  * RHEL/CentOS: `/var/log/cron`

If the job appears in the logs with an execution timestamp, cron is attempting to run it, and the failure is occurring inside the command or script itself.

#### 3. Capture `stdout` and `stderr`
By default, cron sends output to the local user’s mail spool (`/var/mail/$USER`). If no Mail Transfer Agent (MTA) like Postfix or Exim is configured, output is discarded.

Force the job to log all output (both standard output and errors) to an explicit file:
```crontab
* * * * * /path/to/script.sh >> /tmp/cron_debug.log 2>&1
```
Check `/tmp/cron_debug.log` after the scheduled runtime to view the exact error message.

---

### Step 2: Identify and Fix Common Pitfalls

#### 1. The Minimal Environment and `$PATH` Issue
Cron does **not** load your shell configuration files (`~/.bashrc`, `~/.bash_profile`, `/etc/profile`). It runs in a stripped-down environment where `$PATH` usually defaults only to `/usr/bin:/bin`.

* **Symptoms:** `command not found`, utilities fail, language runtimes (like `python3`, `node`, `aws`) cannot be located.
* **Fixes:**
  * Use absolute paths for all executables inside scripts and in the crontab:
    ```crontab
    # Instead of: python3 my_script.py
    0 * * * * /usr/bin/python3 /home/user/my_script.py
    ```
  * Define `$PATH` explicitly at the top of your crontab:
    ```crontab
    PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

    0 * * * * my_script.sh
    ```

#### 2. Incorrect Working Directory
When cron executes a job, the current working directory defaults to the user's home directory (`$HOME`), not the directory where the script resides.

* **Symptoms:** `No such file or directory` when accessing relative files or local imports.
* **Fixes:**
  * `cd` to the working directory before executing the command:
    ```crontab
    0 * * * * cd /opt/myapp && ./run_task.sh
    ```
  * Ensure the script explicitly sets its own working directory:
    ```bash
    #!/usr/bin/env bash
    cd "$(dirname "$0")" || exit 1
    ```

#### 3. Syntax Mismatch: User Crontab vs. System Crontab
There are two primary formats for crontabs:

* **User Crontabs** (`crontab -e`):
  ```text
  # Format: [m] [h] [dom] [mon] [dow] [command]
  0 2 * * * /usr/local/bin/backup.sh
  ```
* **System Crontabs** (`/etc/crontab` and files in `/etc/cron.d/`):
  These files **require** a username field between the time definition and the command:
  ```text
  # Format: [m] [h] [dom] [mon] [dow] [user] [command]
  0 2 * * * root /usr/local/bin/backup.sh
  ```

If you put a username inside a user crontab (`crontab -e`), cron attempts to run the username as a command and fails. Conversely, omitting the username in `/etc/cron.d/` causes the command to fail immediately.

#### 4. Percent Signs (`%`) in the Command
In crontab lines, the `%` character denotes a newline unless escaped. Any text after an unescaped `%` is passed to the command as standard input.

* **Failing Command:**
  ```crontab
  # Fails because %Y%m%d is interpreted as newlines
  0 0 * * * tar -czf /backups/backup-$(date +%Y%m%d).tar.gz /data
  ```
* **Fix:** Escape every `%` with a backslash `\`:
  ```crontab
  0 0 * * * tar -czf /backups/backup-$(date +\%Y\%m\%d).tar.gz /data
  ```

#### 5. Script Permissions and Shebang Lines
* **Executable Bit:** Ensure the target file has execute permissions:
  ```bash
  chmod +x /path/to/script.sh
  ```
* **Shebang:** Ensure the interpreter is declared on the very first line of the script:
  ```bash
  #!/usr/bin/env bash
  ```
* **Windows Line Endings:** If a script was edited on Windows, CRLF line endings (`\r\n`) will cause cron/bash to throw `^M: bad interpreter` or syntax errors. Run `dos2unix script.sh` to remove them.

#### 6. Missing Trailing Newline
Classic implementations of Vixie Cron ignore the last line of a crontab file if it does not end with an empty newline. Always hit `Enter` after the final line when saving a crontab.

#### 7. Access Control Files
Verify that the target user is permitted to use cron. Check the following files:
* `/etc/cron.allow`: If this file exists, the user **must** be listed inside it.
* `/etc/cron.deny`: If this file exists and `cron.allow` does not, the user **must not** be listed inside it.

---

### Step 3: Reproducing the Execution Environment

To test your script in the exact environment cron uses, strip your current shell of its variables and execute the command through a bare non-interactive shell:

```bash
env -i HOME="$HOME" PATH="/usr/bin:/bin" SHELL="/bin/sh" /bin/sh -c "/path/to/script.sh"
```

If the command fails under this command, the problem is an environment variable dependency (e.g., missing `$PATH`, database secrets, or API keys). Define those missing variables directly within the script or at the top of the crontab file.
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Server Fault](https://serverfault.com/questions/449651/why-is-my-crontab-not-working-and-how-can-i-troubleshoot-it).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
