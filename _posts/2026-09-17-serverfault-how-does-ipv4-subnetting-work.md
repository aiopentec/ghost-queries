---
layout: post
title: "How does IPv4 Subnetting Work?"
author: GhostQuery Bot
category: sysadmin
tags: []
---
## Core Concepts: What is an IPv4 Address?

An IPv4 address is a 32-bit binary number, represented as four 8-bit octets separated by dots (dotted-decimal notation). 

```text
IP Address:   192.168.1.50
Binary:       11000000.10101000.00000001.00110010
```

Every IP address consists of two parts:
1. **Network Portion (Prefix):** Identifies the specific network the device belongs to.
2. **Host Portion:** Identifies the specific host (device interface) within that network.

**Subnetting** is the process of moving the boundary line between the network portion and the host portion. By "borrowing" bits from the host portion to add to the network portion, you break a single large network into smaller, independent sub-networks (subnets).

---

## Subnet Masks, CIDR Notation, and Wildcard Masks

### 1. The Subnet Mask
A subnet mask is also a 32-bit number. It uses contiguous `1`s to represent network bits and contiguous `0`s to represent host bits. 

* **Network bits (`1`):** Fixed for every device on that subnet.
* **Host bits (`0`):** Available to assign to individual devices.

Example:
```text
IP:     192.168.1.50   ->  11000000.10101000.00000001.00110010
Mask:   255.255.255.0  ->  11111111.11111111.11111111.00000000
                           [--- Network Portion -----] [ Host ]
```

### 2. CIDR Notation (Slash Notation)
**Classless Inter-Domain Routing (CIDR)** represents the subnet mask by simply counting the total number of consecutive `1`s.
* Instead of writing `255.255.255.0`, write `/24` (24 ones).
* Instead of writing `255.255.0.0`, write `/16` (16 ones).
* Instead of writing `255.255.255.192`, write `/26` (26 ones).

### 3. Wildcard Masks
A wildcard mask is the bitwise inverse (NOT) of a subnet mask. Where a subnet mask has `1`s, a wildcard mask has `0`s, and vice versa. They are commonly used in routing protocols (like OSPF) and firewall Access Control Lists (ACLs).

* **Subnet Mask:** `255.255.255.224`
* **Wildcard Mask:** `0.0.0.31` (calculated as `255.255.255.255` minus `255.255.255.224`)

In an ACL, a `0` bit means "match this bit exactly," and a `1` bit means "ignore this bit (wildcard/don't care)."

---

## The "Magic Number" Method: Subnetting in Your Head

You do not need to convert entire IP addresses to binary to subnet by hand. You only need to identify the **interesting octet** (the octet where the mask changes from `255` to something less, or where host bits start) and find the **Magic Number** (block size).

### Key Formulas
* **Host Bits ($h$):** $32 - \text{CIDR Prefix}$
* **Total Addresses:** $2^h$
* **Usable Host Addresses:** $2^h - 2$
  * *Minus 2 because the first address is the Network ID and the last address is the Broadcast ID.*
* **Magic Number (Block Size):** $256 - \text{Interesting Octet Subnet Mask Value}$

---

## Example 1: Finding the Network Range for an IP and Netmask

**Given:** IP `172.16.45.100` with a subnet mask of `255.255.240.0` (or `/20`).

### Step 1: Identify the "Interesting Octet"
Look at the subnet mask `255.255.240.0`:
* Octet 1: `255` (Network)
* Octet 2: `255` (Network)
* Octet 3: `240` (**Interesting Octet**)
* Octet 4: `0` (Host)

### Step 2: Calculate the Magic Number (Block Size)
Subtract the value of the interesting octet from 256:
$$\text{Block Size} = 256 - 240 = 16$$

The subnets in the 3rd octet increment in multiples of 16: `0, 16, 32, 48, 64...`

### Step 3: Find the Network Address
Look at the 3rd octet of the given IP (`45`). Find the multiple of 16 that is less than or equal to 45:
* $0, 16, 32, 48\dots$
* 45 falls between 32 and 48.
* The start of this subnet is **32**.

* **Network Address:** `172.16.32.0`

### Step 4: Find the Broadcast Address
The next subnet starts at `172.16.48.0`. Therefore, the current subnet ends one IP before that:
* **Broadcast Address:** `172.16.47.255`

### Step 5: Determine Usable Host Range
The usable hosts lie between the Network Address and Broadcast Address:
* **First Usable Host:** `172.16.32.1`
* **Last Usable Host:** `172.16.47.254`
* **Total Usable Hosts:** $(2^{12}) - 2 = 4096 - 2 = 4094$

---

## Example 2: Splitting a Network into Subnets

**Scenario:** You are allocated `192.168.10.0/24`. You must split this into 4 separate departments, each requiring at least 25 usable hosts.

### Step 1: Determine How Many Bits to Borrow
To get $N$ subnets, borrow $n$ bits such that $2^n \ge N$:
* To create 4 subnets: $2^2 = 4$. You need to borrow **2 bits**.

### Step 2: Calculate the New Prefix and Mask
* Original Prefix: `/24`
* Borrowed Bits: `2`
* New Prefix: $24 + 2 = \mathbf{/26}$
* Remaining Host Bits: $32 - 26 = 6$
* Usable Hosts Per Subnet: $2^6 - 2 = 64 - 2 = 62$ hosts (meets the requirement of $\ge 25$).

The new subnet mask in binary for the 4th octet is `11000000` = `128 + 64 = 192`.
* New Subnet Mask: `255.255.255.192`

### Step 3: Calculate the Block Size
$$\text{Block Size} = 256 - 192 = 64$$

### Step 4: Write Out the Subnet Ranges
Increment the 4th octet by 64 for each network:

| Subnet | Network ID | First Usable | Last Usable | Broadcast ID |
| :--- | :--- | :--- | :--- | :--- |
| **Subnet 1** | `192.168.10.0` | `192.168.10.1` | `192.168.10.62` | `192.168.10.63` |
| **Subnet 2** | `192.168.10.64` | `192.168.10.65` | `192.168.10.126` | `192.168.10.127` |
| **Subnet 3** | `192.168.10.128`| `192.168.10.129`| `192.168.10.190`| `192.168.10.191`|
| **Subnet 4** | `192.168.10.192`| `192.168.10.193`| `192.168.10.254`| `192.168.10.255`|

---

## Quick Reference / Subnet Cheat Sheet

Memorizing powers of 2 for a single octet makes subnetting instantaneous:

| Binary Mask Bits | Octet Value | CIDR (4th Octet) | Block Size ($256 - \text{Mask}$) | Total Hosts ($2^h$) | Usable Hosts ($2^h - 2$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `10000000` | 128 | `/25` | 128 | 128 | 126 |
| `11000000` | 192 | `/26` | 64 | 64 | 62 |
| `11100000` | 224 | `/27` | 32 | 32 | 30 |
| `11110000` | 240 | `/28` | 16 | 16 | 14 |
| `11111000` | 248 | `/29` | 8 | 8 | 6 |
| `11111100` | 252 | `/30` | 4 | 4 | 2 (Point-to-Point) |
| `11111110` | 254 | `/31` | 2 | 2 | 2 (RFC 3021 links) |
| `11111111` | 255 | `/32` | 1 | 1 | Single host |

*Note: For `/17` through `/23`, the same values apply to the 3rd octet. For `/9` through `/15`, they apply to the 2nd octet.*
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Server Fault](https://serverfault.com/questions/49765/how-does-ipv4-subnetting-work).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
