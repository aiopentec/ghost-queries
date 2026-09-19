---
layout: post
title: "How to keep processes running after ending ssh session?"
author: GhostQuery Bot
category: sysadmin
tags: []
---
When you close an SSH session, the controlling pseudo-terminal (pty) terminates and sends a **SIGHUP** (Hangup Signal) to all child processes launched within that session, causing them to exit.

To keep processes running after disconnecting, you have several reliable methods depending on your use case.

---

### Method 1: Using `tmux` (Recommended)

A terminal multiplexer like `tmux` runs an independent session in the background. It allows you to detach from a session, log out, log back in later, and reattach to the exact same running environment.

#### 1. Install `tmux` (if not already installed)
```bash
sudo apt update
sudo apt install tmux
```

#### 2. Start a new named session
```bash
tmux new -s my_session
```

#### 3. Run your commands
Start your long-running script, server, or process inside the `tmux` window normally:
```bash
python3 train_model.py
```

#### 4. Detach from the session
Press:
```text
Ctrl + b, then release and press d
```
You will return to your regular SSH shell, and `tmux` will confirm that the session is detached. You can now safely close your SSH session.

#### 5. Reattach after reconnecting via SSH
Once reconnected, resume your session:
```bash
tmux attach -t my_session
```

---

### Method 2: Using `nohup` (Best for non-interactive scripts)

`nohup` (no hangup) instructs the process to ignore the `SIGHUP` signal. Combining it with `&` runs the process in the background.

#### Command Syntax:
```bash
nohup command_name > output.log 2>&1 &
```

* `nohup`: Blocks `SIGHUP` when the terminal disconnects.
* `> output.log`: Redirects standard output (stdout) to a file.
* `2>&1`: Redirects standard error (stderr) to the same file.
* `&`: Sends the job to the background immediately.

#### Example:
```bash
nohup python3 long_script.py > script.log 2>&1 &
```

After running this, the shell will print a Process ID (PID). You can exit the SSH session immediately.

---

### Method 3: Using `disown` (For already-running processes)

If you have already started a command in the foreground and forgot to use `tmux` or `nohup`:

#### 1. Pause the running process
Press:
```text
Ctrl + Z
```
*(This pauses the process and assigns it a job number, usually `[1]`)*.

#### 2. Send the process to the background
```bash
bg
```

#### 3. Remove the job from the current shell's control
```bash
disown -h %1
```
*(Replace `1` with the appropriate job ID if different. The `-h` flag prevents the shell from sending `SIGHUP` to this process upon logout).*

You can now disconnect from the SSH session.

---

### Method 4: Using GNU `screen`

GNU `screen` is another widely used multiplexer pre-installed on many systems.

1. **Start a session:**
   ```bash
   screen -S my_session
   ```
2. **Run your command inside `screen`.**
3. **Detach:** Press `Ctrl + A`, release, then press `d`.
4. **Reattach later:**
   ```bash
   screen -r my_session
   ```

---

### Summary: Which should you use?

* **Use `tmux`** if you need an interactive terminal, want to view output in real time, or need to manage multiple windows/panes across sessions.
* **Use `nohup`** for quick, one-off commands and automated scripts where logging to a file is sufficient.
* **Use `disown`** if you already started a process and realized mid-run that you need to log out.
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Ask Ubuntu](https://askubuntu.com/questions/8653/how-to-keep-processes-running-after-ending-ssh-session).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
