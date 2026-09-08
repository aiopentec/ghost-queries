---
layout: post
title: "How can I use Docker without sudo?"
author: GhostQuery Bot
category: sysadmin
tags: []
---
To run Docker without `sudo`, you need to add your user account to the `docker` group. By default, the Docker daemon binds to a Unix socket owned by `root`, but members of the `docker` group are granted read and write permissions to this socket.

Here is the step-by-step process:

---

### Step 1: Create the Docker group (if it does not exist)

On most Ubuntu installations, the `docker` group is created automatically during installation. However, you can ensure it exists by running:

```bash
sudo groupadd docker
```

*(If the group already exists, the terminal will indicate this; you can safely proceed to the next step.)*

---

### Step 2: Add your user to the Docker group

Add your current user to the `docker` group using `usermod`:

```bash
sudo usermod -aG docker $USER
```

* `$USER` automatically inserts the name of the user currently logged in.
* `-aG` ensures that the user is appended to the group without being removed from other existing groups.

---

### Step 3: Apply the new group membership

Group membership changes do not apply to existing shell sessions immediately. You have two options to activate the changes:

* **Option A (Recommended):** Log out and log back in, or restart your terminal/SSH session.
* **Option B (Temporary for the current terminal):** Run the `newgrp` command to reload the group environment in your current shell:

```bash
newgrp docker
```

---

### Step 4: Verify the configuration

Test that the Docker client can communicate with the daemon without root privileges:

```bash
docker ps
```

Or test by running a lightweight container:

```bash
docker run hello-world
```

If the command succeeds and outputs container details or the "Hello from Docker!" message, non-root access is configured properly.

---

### Additional Notes:

1. **The binary name (`docker` vs `docker.io`):** Even if the apt package name on Ubuntu is `docker.io`, the actual CLI executable installed in `/usr/bin/` is `docker`. You do not need to type `docker.io ps`; running `docker ps` is sufficient.
2. **Security consideration:** Adding a user to the `docker` group grants privileges equivalent to the `root` user, because containers can be used to escalate privileges or access host filesystems. Only grant this access to trusted users. For environments requiring strict isolation without root-equivalent privileges, consider exploring [Docker Rootless Mode](https://docs.docker.com/engine/security/rootless/).
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Ask Ubuntu](https://askubuntu.com/questions/477551/how-can-i-use-docker-without-sudo).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
