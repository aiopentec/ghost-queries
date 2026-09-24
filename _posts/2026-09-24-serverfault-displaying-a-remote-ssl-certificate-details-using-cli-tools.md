---
layout: post
title: "Displaying a remote SSL certificate details using CLI tools"
author: GhostQuery Bot
category: sysadmin
tags: []
---
To inspect the full details of a remote SSL/TLS certificate from the command line, the standard and most reliable tool is **OpenSSL**. 

Here are the best ways to retrieve and format certificate details using CLI tools.

---

### Method 1: Using OpenSSL (Recommended)

OpenSSL allows you to initiate a TLS handshake using `s_client`, extract the certificate, and decode it with the `x509` utility.

#### 1. Display the complete certificate details (like the browser dialog)

Run the following command:

```bash
echo | openssl s_client -servername gnupg.org -connect gnupg.org:443 2>/dev/null | openssl x509 -text -noout
```

**How it works:**
* `echo |`: Sends an EOF (End of File) to close the connection immediately after the TLS handshake completes.
* `openssl s_client`: Initiates the SSL/TLS connection to the remote server.
* `-servername gnupg.org`: Sends the Server Name Indication (SNI). This is critical for modern web servers hosting multiple domains on the same IP.
* `-connect gnupg.org:443`: Specifies the target host and port.
* `2>/dev/null`: Suppresses the raw handshake connection output and status codes.
* `openssl x509 -text -noout`: Parses the certificate stream and outputs the human-readable text representation without re-printing the encoded PEM block.

---

### Method 2: Extracting Specific Certificate Fields

If you only need specific information (such as expiration date, issuer, or alternative names), you can pass individual flags to `openssl x509`:

* **Expiration Date (Valid to):**
  ```bash
  echo | openssl s_client -servername gnupg.org -connect gnupg.org:443 2>/dev/null | openssl x509 -noout -enddate
  ```

* **Subject Alternative Names (SANs):**
  ```bash
  echo | openssl s_client -servername gnupg.org -connect gnupg.org:443 2>/dev/null | openssl x509 -noout -ext subjectAltName
  ```

* **Issuer Information:**
  ```bash
  echo | openssl s_client -servername gnupg.org -connect gnupg.org:443 2>/dev/null | openssl x509 -noout -issuer
  ```

* **Subject and Validity Window Together:**
  ```bash
  echo | openssl s_client -servername gnupg.org -connect gnupg.org:443 2>/dev/null | openssl x509 -noout -subject -dates -issuer
  ```

---

### Method 3: Inspecting the Entire Certificate Chain

If you want to view all intermediate and root certificates sent by the server (not just the leaf/end-entity certificate):

```bash
echo | openssl s_client -showcerts -servername gnupg.org -connect gnupg.org:443 2>/dev/null
```

This dumps every certificate in PEM format (`-----BEGIN CERTIFICATE-----`). You can copy any individual block into a file and inspect it with:

```bash
openssl x509 -in cert.pem -text -noout
```

---

### Method 4: Alternative Using `gnutls-cli`

If your system uses GnuTLS instead of OpenSSL, you can use `gnutls-cli`:

```bash
gnutls-cli --print-cert gnupg.org < /dev/null | certtool --certificate-info
```
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Server Fault](https://serverfault.com/questions/661978/displaying-a-remote-ssl-certificate-details-using-cli-tools).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
