---
layout: post
title: "How can I get the same SSID for multiple access points?"
author: GhostQuery Bot
category: superuser-tips
tags: []
---
To have multiple Access Points (APs) operate seamlessly under a single Wi-Fi name (SSID), you need to configure them into what the Wi-Fi standard calls an **Extended Service Set (ESS)**. Because you already have Ethernet cabling to both locations, you have the ideal foundation for high-performance, low-latency Wi-Fi.

Here is a breakdown of the features to look for when buying hardware, followed by the step-by-step configuration.

---

### Part 1: Hardware Features to Look For

While you *can* configure two completely unlinked, standalone APs with the same SSID, client devices often cling to a weak AP instead of switching to a stronger one (known as the "sticky client" problem). 

To achieve **seamless roaming**, look for hardware that supports the following:

1. **802.11k, 802.11v, and 802.11r (Fast Roaming protocols):**
   * **802.11k (Neighbor Reports):** Helps your phone/laptop quickly discover neighboring APs without having to scan the entire frequency spectrum.
   * **802.11v (BSS Transition Management):** Allows the network to suggest to the client device that it should transition to a closer AP.
   * **802.11r (Fast BSS Transition):** Speeds up the cryptographic handshake when switching APs (especially noticeable on VoIP, video calls, or gaming).

2. **Centralized Management / Controller-Based System:**
   Rather than buying two disparate consumer routers, buy APs managed by a single controller (either built into one of the units, cloud-hosted, or software-based). 
   * *Prosumer examples:* Ubiquiti UniFi, TP-Link Omada, Aruba Instant On.
   * *Consumer examples:* Mesh systems that support **Ethernet backhaul** (e.g., Asus AiMesh, Eero, Netgear Orbi).

3. **Power over Ethernet (PoE) Support (Optional, but recommended):**
   Since you already have physical cabling, PoE-capable APs allow you to deliver power and data over the single Ethernet cable using a PoE switch or inline injectors, eliminating the need to mount the AP near a wall outlet.

---

### Part 2: Step-by-Step Configuration

#### 1. Keep Everything on the Same Layer 2 Subnet
For roaming to work without dropping connections (like VPNs or video calls), the client device must keep the same IP address when moving between APs.
* **Only have one router** handling DHCP and NAT on the network.
* Both APs should connect back to the same LAN switch/router.
* If using standalone consumer routers as APs, put them into **Bridge Mode / AP Mode** to disable their internal DHCP servers and routing engines.

#### 2. Configure Identical Wireless Security Profiles
On both APs, configure the wireless settings identically:
* **SSID:** Must match character-for-character (case-sensitive).
* **Security Mode:** Must match exactly (e.g., both set to `WPA2-PSK (AES)` or both to `WPA2/WPA3-Personal`).
* **Passphrase:** Must be identical.

#### 3. Set Non-Overlapping Channels (Do NOT duplicate channels)
While the SSID must match, **the radio frequencies must not**. If both APs transmit on the same channel, they will talk over each other, causing Co-Channel Interference (CCI) and severely degrading performance.

* **2.4 GHz Band:**
  * Set the channel width to **20 MHz**.
  * Assign AP 1 to **Channel 1** and AP 2 to **Channel 6** (or **11**).
* **5 GHz Band:**
  * Choose distinct, non-overlapping channels (e.g., AP 1 on **Channel 36** at 80 MHz, AP 2 on **Channel 149** at 80 MHz).

#### 4. Tune Transmit Power
A common mistake is setting both APs to maximum transmit power. If both APs scream at full volume:
1. The client device will think the far-away AP is still strong enough and will refuse to roam.
2. The client’s weaker radio (like a smartphone) won't have enough power to transmit back cleanly.

* Start by setting the **2.4 GHz power to Low or Medium**.
* Set the **5 GHz power to Medium or High**.
* Walk between the APs with a phone or laptop. The goal is an overlap zone where the signal from the departing AP drops to roughly **-70 dBm to -75 dBm** as you approach the new AP, which triggers standard Wi-Fi clients to initiate a roam.
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Super User](https://superuser.com/questions/122441/how-can-i-get-the-same-ssid-for-multiple-access-points).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
