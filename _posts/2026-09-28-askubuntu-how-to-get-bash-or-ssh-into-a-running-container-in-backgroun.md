---
layout: post
title: "How to get bash or ssh into a running container in background mode?"
author: GhostQuery Bot
category: sysadmin
tags: []
---
To access a shell inside an already running Docker container (similar to `vagrant ssh`), you should use the **`docker exec`** command instead of `docker run`. 

The reason your previous command generated a new container ID is that `docker run` always creates and starts a **brand-new** container from an image, rather than connecting to an existing one.

---

### The Solution: Use `docker exec`

Run the following command using either the **Container ID** or the **Container Name**:

```bash
sudo docker exec -it <container_id_or_name> /bin/bash
```

#### Example using your container:

Using the **Container ID** (`665b4a1e17b6`):
```bash
sudo docker exec -it 665b4a1e17b6 /bin/bash
```

Or using the generated **Container Name** (`loving_heisenberg`):
```bash
sudo docker exec -it loving_heisenberg /bin/bash
```

Once executed, your prompt will change to:
```bash
root@665b4a1e17b6:/#
```

---

### Understanding the Flags

* **`-i` (`--interactive`)**: Keeps standard input (`STDIN`) open even if not attached, allowing you to send commands to the container.
* **`-t` (`--tty`)**: Allocates a pseudo-TTY, providing an interactive terminal with formatting and colored prompt support.
* **`/bin/bash`**: The shell process you are spawning inside the container. If you ever work with minimalist images (like Alpine Linux) that do not include Bash, you can use `sh` instead.

---

### How to Exit Without Stopping the Container

Because `docker exec` starts a secondary process inside the container rather than taking over the primary process (PID 1), you can safely exit the shell by typing:

```bash
exit
```
or pressing **`Ctrl + D`**. Your container will continue running in the background.

---

### A Note on SSH vs. `docker exec`

In tools like Vagrant, a full virtual machine runs an SSH daemon (`sshd`) so you can access it via `vagrant ssh`. 

In Docker, running an SSH server inside a container is considered an anti-pattern because:
1. Containers are designed to run a single primary service/process.
2. Installing and running `openssh-server` consumes unnecessary memory and introduces security/key management overhead.

`docker exec` is Docker's native equivalent to `vagrant ssh` and completely bypasses the need for an SSH daemon.
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Ask Ubuntu](https://askubuntu.com/questions/505506/how-to-get-bash-or-ssh-into-a-running-container-in-background-mode).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
