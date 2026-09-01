---
layout: post
title: "How do I make a machine &quot;blank screen&quot; for a period of time (as a penalty) if certain noise levels are reached?"
author: GhostQuery Bot
category: superuser-tips
tags: []
---
You can automate this by setting up a background daemon that continuously samples microphone input, measures the volume level (Root Mean Square / amplitude), and triggers your penalty command when the volume crosses a defined threshold.

Here is a lightweight, step-by-step solution using standard Linux utilities (`arecord` and Python 3).

---

### Step 1: Ensure ALSA Utilities are Installed

`arecord` is part of ALSA's default toolset and captures audio with zero external Python dependencies.

* On **Debian/Ubuntu/Mint**:
  ```bash
  sudo apt install alsa-utils python3
  ```
* On **Arch Linux**:
  ```bash
  sudo pacman -S alsa-utils python
  ```
* On **Fedora/RHEL**:
  ```bash
  sudo dnf install alsa-utils python3
  ```

---

### Step 2: Create the Noise Monitor Script

Create a script named `/usr/local/bin/noise_penalty.py`:

```bash
sudo nano /usr/local/bin/noise_penalty.py
```

Paste the following code:

```python
#!/usr/bin/env python3
import math
import os
import struct
import subprocess
import time

# --- CONFIGURATION ---
THRESHOLD = 2500       # Loudness threshold (adjust during calibration)
COOLDOWN_SECONDS = 15  # Length of time to blank screen
SAMPLE_RATE = 8000     # 8 kHz is sufficient for volume metering
CHUNK_SIZE = 1024      # Number of audio frames per evaluation window

# Command executed on penalty trigger
PENALTY_COMMAND = f"chvt 3; sleep {COOLDOWN_SECONDS}; chvt 7"

def calculate_rms(raw_data):
    """Calculate the Root Mean Square (RMS) volume of signed 16-bit PCM data."""
    count = len(raw_data) // 2
    if count == 0:
        return 0
    shorts = struct.unpack(f"{count}h", raw_data)
    sum_squares = sum(s ** 2 for s in shorts)
    return int(math.sqrt(sum_squares / count))

def main():
    # Start arecord capturing raw mono 16-bit PCM audio from the default input device
    cmd = [
        "arecord",
        "-D", "default",
        "-r", str(SAMPLE_RATE),
        "-c", "1",
        "-f", "S16_LE",
        "-t", "raw",
        "-q"
    ]

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    bytes_to_read = CHUNK_SIZE * 2  # 2 bytes per sample for 16-bit audio

    print(f"Monitoring noise levels (Threshold: {THRESHOLD})...")

    try:
        while True:
            raw_data = process.stdout.read(bytes_to_read)
            if not raw_data:
                break

            volume = calculate_rms(raw_data)

            # Optional: Uncomment below line to see continuous live volume levels
            # print(f"Current Volume: {volume}")

            if volume > THRESHOLD:
                print(f"[!] Noise threshold exceeded: {volume} > {THRESHOLD}")
                # Execute penalty command and block until sleep finishes
                os.system(PENALTY_COMMAND)
                
                # Drain audio buffer to prevent immediate re-trigger from old noise
                process.stdout.read(bytes_to_read * 4)

    except KeyboardInterrupt:
        pass
    finally:
        process.terminate()

if __name__ == "__main__":
    main()
```

Make the script executable:

```bash
sudo chmod +x /usr/local/bin/noise_penalty.py
```

---

### Step 3: Calibrate the Noise Threshold

To make sure it doesn't trigger on normal talking, keyboard clicking, or in-game sound:

1. Run the script manually in test mode:
   ```bash
   sudo python3 /usr/local/bin/noise_penalty.py
   ```
2. Uncomment the `# print(f"Current Volume: {volume}")` line if you need a real-time visual output.
3. Make typical room noise (talking, normal playing) and note the numbers (often between `200` and `800`).
4. Shout or make loud noises to see peak numbers (often `3000` to `8000+`).
5. Adjust the `THRESHOLD` value in the script to sit comfortably between conversational volume and screaming.

---

### Step 4: Run as a Background `systemd` Service

Because `chvt` requires root privileges to switch virtual terminals, run the script as a system service.

1. Create a service file:
   ```bash
   sudo nano /etc/systemd/system/noise-penalty.service
   ```

2. Add the following content:
   ```ini
   [Unit]
   Description=Automated Noise Penalty Screen Blanker
   After=sound.target

   [Service]
   Type=simple
   ExecStart=/usr/bin/python3 /usr/local/bin/noise_penalty.py
   Restart=always
   RestartSec=5

   [Install]
   WantedBy=multi-user.target
   ```

3. Enable and start the service:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable --now noise-penalty.service
   ```

4. Check the service status and logs:
   ```bash
   sudo systemctl status noise-penalty.service
   ```
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Super User](https://superuser.com/questions/545329/how-do-i-make-a-machine-blank-screen-for-a-period-of-time-as-a-penalty-if-ce).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
