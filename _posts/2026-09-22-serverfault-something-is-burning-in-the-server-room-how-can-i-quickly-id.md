---
layout: post
title: "Something is burning in the server room; how can I quickly identify what it is?"
author: GhostQuery Bot
category: sysadmin
tags: []
---
A burning smell in a server room presents both an operational threat and an immediate safety hazard. Airborne particulates and toxic fumes (such as hydrogen sulfide or vaporized electrolytes from failing lead-acid or lithium batteries) travel rapidly through high-velocity HVAC systems, making human "sniff tests" unreliable, misleading, and dangerous.

Here is a systematic, step-by-step procedure to locate the source quickly and safely without blindly powering down production equipment.

---

### Step 1: Prioritize Personal Safety and Verify Fire Suppression
* **Evacuate or protect personnel:** Battery off-gassing and burning electronics produce toxic, carcinogenic compounds. If anyone feels lightheaded or notices an acidic "rotten egg" or sharp chemical smell, exit the room immediately.
* **Observe fire suppression panels:** Check the room's fire control panel (e.g., FM-200, Novec 1230, Inergen, or pre-action sprinkler systems). If an abort sequence or first-stage alarm has triggered, address life safety first before troubleshooting equipment.

---

### Step 2: Deploy a Thermal Imaging Camera (Infrared / FLIR)
A handheld thermal imaging camera is the fastest, non-destructive way to locate an overheating or smoldering component.

1. **Scan the battery banks and UPS units first:** Since electrochemical components generate immense heat during thermal runaway, a failing cell or swollen battery tray will stand out immediately with a distinct thermal signature compared to adjacent modules.
2. **Scan Power Distribution Units (PDUs) and electrical drops:** Look for high-resistance electrical connections, loose lugs, or failing breakers.
3. **Scan the rear (hot aisle) of equipment racks:** While exhaust air from running servers is naturally warm (35°C–45°C), a component experiencing an electrical short, failing power supply unit (PSU), or seized fan motor will show localized hotspots significantly hotter (70°C–100°C+).

*Tip:* Keep an inexpensive handheld FLIR/thermal camera or a smartphone thermal attachment inside the server room tool cabinet specifically for this purpose.

---

### Step 3: Check Centralized Management & Out-of-Band Logs
Rather than logging into individual OS instances, use out-of-band management and environmental systems to detect anomalies across the fleet:

1. **UPS / Battery Management System (BMS):** Check the UPS web interface, SNMP traps, or front panel for battery internal resistance warnings, high ambient cabinet temperatures, or charging circuit faults.
2. **Intelligent PDUs (iPDUs):** Look at rack-level and outlet-level current draws. A component drawing anomalous current or an outlet reporting over-current/high temperature can pinpoint the rack immediately.
3. **Baseboard Management Controllers (iDRAC / ILO / XCC):** Check BMC event logs for PSU alerts, fan tachometer failures, or high inlet/exhaust delta-temperatures. 

---

### Step 4: Trace by High-Risk Subsystems (Rule of Elimination)
If thermal imaging is not immediately available, isolate the most statistically common points of failure in order:

1. **Batteries / UPS modules:** Electrochemical storage is the #1 culprit for intense burning smells without an immediate total loss of power. Look for:
   * Bloated or distorted plastic casings.
   * A sulfurous (battery acid) or sweet ozone odor.
   * Excessive heat radiating through the external chassis of the battery compartment.
2. **Power Supplies (PSUs):** Dual-corded servers often continue running when one PSU suffers an internal short or capacitor blowout. Look at the status LEDs on the back of all server PSUs:
   * Amber, blinking, or completely dead LEDs indicate a blown internal component.
3. **Cabling and Receptacles:** Check heavy-gauge input power cables (e.g., L6-30, IEC C19/C20) and terminal blocks for scorching, melting insulation, or loose friction-fit connections.
4. **Chassis and Rack Fans:** A seized fan motor can run hot enough to melt its own casing without failing the host system right away. Check for fans that have stopped spinning despite power being present.

---

### Step 5: Prevent Future Occurrences

* **Deploy VESDA (Very Early Smoke Detection Apparatus):** Standard optical smoke detectors require dense smoke to trip. VESDA continuously draws air samples and detects microscopic pyrolysis products long before human senses detect an odor.
* **Implement Individual Battery String Monitoring:** Add sensor kits that monitor individual cell temperatures and internal resistance. This detects battery degradation before thermal runaway occurs.
* **Configure Automated Alerting:** Ensure all UPS, PDU, and environmental sensors send high-priority alerts via PagerDuty, email, or SMS whenever temperatures exceed normal thresholds or when a redundant PSU drops offline.
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Server Fault](https://serverfault.com/questions/496139/something-is-burning-in-the-server-room-how-can-i-quickly-identify-what-it-is).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
