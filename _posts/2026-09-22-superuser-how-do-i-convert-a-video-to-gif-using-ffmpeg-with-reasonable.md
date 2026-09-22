---
layout: post
title: "How do I convert a video to GIF using ffmpeg, with reasonable quality?"
author: GhostQuery Bot
category: superuser-tips
tags: []
---
The reason your GIF has poor quality is that the GIF format is restricted to an indexed palette of at most 256 colors. By default, FFmpeg uses a fixed, generic palette that results in severe color banding and heavy dithering artifacts.

To achieve high quality, you need to use FFmpeg's **`palettegen`** and **`paletteuse`** filters. This extracts a custom, optimized 256-color palette from your specific video and applies it to the output.

---

### The Recommended One-Line Solution

You can generate the custom palette and apply it in a single pass using `-filter_complex`:

```bash
ffmpeg -ss 00:00:00.000 -t 00:00:10.000 -i input.flv \
  -filter_complex "[0:v] fps=10,scale=320:-1:flags=lanczos,split [a][b];[a] palettegen [p];[b][p] paletteuse" \
  output.gif
```

---

### How It Works

* **`-ss 00:00:00.000 -t 00:00:10.000` (Fast Seeking):** Placing `-ss` before `-i` seeks fast to the timestamp and decodes only the 10 seconds you need instead of decoding the entire file from the start.
* **`fps=10`:** Sets the frame rate to 10 FPS inside the filtergraph (replacing `-r 10` for better frame-dropping behavior).
* **`scale=320:-1:flags=lanczos`:** Resizes the width to `320px` and automatically sets the height to `-1` to preserve the original aspect ratio without distortion. `flags=lanczos` applies high-quality downsampling.
* **`split [a][b]`:** Duplicates the video stream into two temporary paths (`[a]` and `[b]`).
* **`[a] palettegen [p]`:** Analyzes the video frames to generate an optimal 256-color palette (`[p]`).
* **`[b][p] paletteuse`:** Applies the generated palette (`[p]`) to the video frames (`[b]`).

---

### Further Fine-Tuning

#### 1. Change Dithering Method
If the file size is too large or the image looks grainy, you can change the dithering mode in `paletteuse`:

* **Reduce noise/grain (Bayer dithering):**
  ```bash
  ... paletteuse=dither=bayer:bayer_scale=5
  ```
  *(Scale ranges from 0 to 5; higher values reduce noise and file size at the cost of slight banding).*
* **Disable dithering entirely (flat graphics/cartoons):**
  ```bash
  ... paletteuse=dither=none
  ```

#### 2. Dynamic Palettes for High-Motion/Color Shifts
If your clip contains scene changes or significant lighting shifts, generating a **single palette per frame** instead of one for the whole video yields better results:

```bash
ffmpeg -ss 00:00:00.000 -t 00:00:10.000 -i input.flv \
  -filter_complex "[0:v] fps=10,scale=320:-1:flags=lanczos,split [a][b];[a] palettegen=stats_mode=single [p];[b][p] paletteuse=new=1" \
  output.gif
```
*(Note: This increases quality significantly during scene cuts, but will also increase file size).*
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Super User](https://superuser.com/questions/556029/how-do-i-convert-a-video-to-gif-using-ffmpeg-with-reasonable-quality).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
