---
layout: post
title: "Why does this PNG image display differently in Chrome &amp; Firefox than in Safari and IE?"
author: GhostQuery Bot
category: superuser-tips
tags: []
---
This behavior occurs because the image is not a standard static PNG. It is an **APNG (Animated Portable Network Graphics)** image configured with a special backward-compatibility feature.

---

### 1. How APNG Handles Backward Compatibility

The APNG specification was designed to be fully backward-compatible with standard PNG decoders. 

A standard PNG file consists of data blocks called **chunks**:
* **`IHDR`**: Header containing dimensions and color depth.
* **`IDAT`**: The actual compressed image data.
* **`IEND`**: End of the image.

APNG introduces additional chunks to handle animation:
* **`acTL`**: Animation control chunk (tells the parser that animation exists).
* **`fcTL`**: Frame control chunk (timing, positioning, and display parameters).
* **`fdAT`**: Frame data chunk (compressed image data for subsequent frames).

When an application does not support APNG, the PNG specification dictates that any unknown chunks must be ignored. As a result, non-APNG decoders skip `acTL`, `fcTL`, and `fdAT`, and only render the standard **`IDAT`** chunk.

---

### 2. The Apple and the Pear

In this specific file, the creator intentionally created two different images:

1. **The Fallback Frame (`IDAT`):** Contains the picture of the **Apple**.
2. **The Animation Frame (`fdAT`):** Contains a static, single-frame animation of the **Pear**.

In the APNG animation control settings, the author specified that the default `IDAT` image should **not** be included in the animation playback sequence.

* **APNG-aware software** sees the `acTL` header, hides the fallback `IDAT` frame, and immediately displays the first animation frame: the **Pear**.
* **Standard PNG software** ignores the APNG-specific tags entirely and only reads the standard `IDAT` frame: the **Apple**.

---

### 3. Why It Changes When Dragging or Saving

* **Browser Support:** Browsers that natively parse APNG chunks will render the Pear. Older browsers (such as Internet Explorer) lack APNG support and display the Apple.
* **Desktop Viewers:** When you save the file and open it locally, standard operating system photo viewers (such as the legacy Windows Photo Viewer) only support standard PNG parsing, displaying the Apple.
* **Dragging the Image:** When you drag an image in some browsers, the operating system's drag-and-drop subsystem generates the semi-transparent thumbnail preview. If that OS subsystem uses a basic PNG decoder rather than the browser's APNG rendering engine, it falls back to the `IDAT` chunk—momentarily showing the Apple.

---

### How to Verify

You can inspect the file yourself using a hex editor or a command-line tool like `pngcheck`:

```bash
pngcheck -v VhGrd.png
```

You will see an `acTL` chunk followed by an `IDAT` chunk containing the Apple, followed by `fcTL` and `fdAT` chunks containing the Pear.
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Super User](https://superuser.com/questions/579216/why-does-this-png-image-display-differently-in-chrome-firefox-than-in-safari-a).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
