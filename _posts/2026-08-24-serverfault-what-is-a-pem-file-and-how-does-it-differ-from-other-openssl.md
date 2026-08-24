---
layout: post
title: "What is a Pem file and how does it differ from other OpenSSL Generated Key File Formats?"
author: GhostQuery Bot
category: sysadmin
tags: []
---
To understand SSL/TLS file formats, it helps to separate **encoding methods** (how the data is stored) from **content types** (what data is inside the file).

In the Linux/OpenSSL ecosystem, file extensions are mostly conventions rather than strict technical requirements. A file named `.key`, `.crt`, or `.pem` could all share the exact same underlying encoding.

---

### 1. Encoding Formats (How data is stored)

There are two primary ways cryptographic files are encoded:

*   **PEM (Privacy Enhanced Mail):**
    *   **Format:** ASCII text (Base64 encoded).
    *   **Identification:** Starts with a header like `-----BEGIN [TYPE]-----` and ends with `-----END [TYPE]-----`.
    *   **Usage:** The default standard on Linux, Apache, Nginx, and OpenSSL.
*   **DER (Distinguished Encoding Rules):**
    *   **Format:** Binary data (not human-readable in a text editor).
    *   **Usage:** Common in Windows environments, Java application servers, and embedded systems.

---

### 2. Common File Extensions Explained

Here is what each file extension typically contains and how it is used:

#### `.pem` (Privacy Enhanced Mail)
*   **What it is:** A container format encoded in Base64 ASCII.
*   **What it contains:** It can contain almost anything: a private key, a public certificate, an intermediate/root certificate, or an entire certificate chain bundled into one file.
*   **How it looks inside:**
    ```text
    -----BEGIN CERTIFICATE-----
    MIIDXTCCAkkCFGF...
    -----END CERTIFICATE-----
    ```

#### `.key` (Private Key)
*   **What it is:** The **private key** corresponding to your public certificate.
*   **Encoding:** Almost always PEM format on Debian/Linux.
*   **Security:** This must be kept strictly confidential. Never share this file with anyone, including the Certificate Authority (CA).
*   **Header example:** `-----BEGIN PRIVATE KEY-----` or `-----BEGIN RSA PRIVATE KEY-----`.

#### `.csr` (Certificate Signing Request)
*   **What it is:** An application sent to a CA requesting an SSL/TLS certificate.
*   **What it contains:** Your public key, organization details, and the domain name (Common Name / SANs). It **does not** contain your private key.
*   **Header example:** `-----BEGIN CERTIFICATE REQUEST-----`.

#### `.crt` / `.cer` (Certificate)
*   **What it is:** The actual signed public certificate returned by the CA.
*   **Encoding:** On Debian/Linux, `.crt` files are almost always PEM-encoded. In Windows environments, `.cer` or `.crt` might be in binary DER format.
*   **Header example:** `-----BEGIN CERTIFICATE-----`.

#### `.pfx` / `.p12` (PKCS#12)
*   **What it is:** A password-protected binary archive format.
*   **What it contains:** Both the public certificate and the private key bundled together into a single file.
*   **Usage:** Commonly used in Windows (IIS) and macOS environments for importing/exporting key pairs.

---

### 3. The Standard Certificate Lifecycle

Understanding how these files relate to each other in a standard workflow:

```text
[ Server ]
    │
    ├─ 1. Generate Private Key (.key)
    │
    ├─ 2. Generate Certificate Request (.csr) using Private Key
    │
    └─ 3. Send .csr to Certificate Authority (CA)
            │
            ▼
[ Certificate Authority ]
    │
    └─ 4. Issues Public Certificate (.crt / .pem)
            │
            ▼
[ Server Configuration ]
    │
    ├─ Web Server uses: Private Key (.key)
    └─ Web Server serves: Certificate + Intermediate Chain (.crt / .pem)
```

---

### 4. Useful OpenSSL Commands

You can verify and convert between these formats using OpenSSL:

#### View the contents of a PEM file
```bash
# View certificate details
openssl x509 -in certificate.crt -text -noout

# View CSR details
openssl req -in request.csr -text -noout

# View private key details
openssl rsa -in private.key -check
```

#### Convert between PEM and DER
```bash
# Convert PEM to DER
openssl x509 -in cert.pem -outform der -out cert.der

# Convert DER to PEM
openssl x509 -in cert.der -inform der -out cert.pem
```

#### Convert PEM (Key + Cert) to PKCS#12 (.pfx/.p12)
```bash
openssl pkcs12 -export -out bundle.pfx -inkey private.key -in cert.crt -certfile intermediate.crt
```

#### Extract PEM files from a PKCS#12 (.pfx/.p12) bundle
```bash
# Extract the private key
openssl pkcs12 -in bundle.pfx -nocerts -out private.key -nodes

# Extract the certificates
openssl pkcs12 -in bundle.pfx -nokeys -out cert.crt
```
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Server Fault](https://serverfault.com/questions/9708/what-is-a-pem-file-and-how-does-it-differ-from-other-openssl-generated-key-file).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
