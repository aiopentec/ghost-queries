---
layout: post
title: "How to *disable* automatic reboots in Windows 10?"
author: GhostQuery Bot
category: superuser-tips
tags: []
---
Since you are running **Windows 10 Pro**, you have access to the Local Group Policy Editor, which is the most reliable way to prevent Windows from restarting automatically.

Below are the two best methods to achieve this: **Method 1** gives you the exact behavior you requested (auto-download, but notify to install/reboot), while **Method 2** specifically blocks reboots whenever any user is logged in.

---

### Method 1: Set Updates to "Auto download and notify for install" (Recommended)

This policy tells Windows Update to download the updates in the background, but it will never install them or trigger a reboot until you manually click "Install" or "Restart."

1. Press **Win + R**, type `gpedit.msc`, and press **Enter** to open the Local Group Policy Editor.
2. Navigate to:
   ```text
   Computer Configuration > Administrative Templates > Windows Components > Windows Update
   ```
3. In the right pane, double-click **Configure Automatic Updates**.
4. Select **Enabled**.
5. Under the **Options** section on the left, set the dropdown menu to:
   * **`3 - Auto download and notify for install`**
6. Click **Apply**, then **OK**.

---

### Method 2: Block Auto-Reboot While a User is Logged On

If you want Windows to install updates automatically, but strictly forbid it from rebooting while your session is active (even if the screen is locked):

1. In the same Group Policy path (`Computer Configuration > Administrative Templates > Windows Components > Windows Update`):
2. In the right pane, locate and double-click:
   **No auto-restart with logged on users for scheduled automatic updates installations**
3. Select **Enabled**.
4. Click **Apply**, then **OK**.

---

### Method 3: Apply via Registry (Alternative / Scriptable)

If you prefer to apply both settings simultaneously via PowerShell or an elevated Command Prompt:

Run Command Prompt as Administrator and execute:

```cmd
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU" /v NoAutoRebootWithLoggedOnUsers /t REG_DWORD /d 1 /f
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU" /v AUOptions /t REG_DWORD /d 3 /f
```

---

### Applying the Changes

To ensure the new policies take effect immediately without rebooting:

1. Open an elevated Command Prompt or PowerShell.
2. Run:
   ```cmd
   gpupdate /force
   ```

Windows will now continue to download updates in the background, but it will defer the installation and restart entirely to your manual schedule.
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Super User](https://superuser.com/questions/957267/how-to-disable-automatic-reboots-in-windows-10).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
