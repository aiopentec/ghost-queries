---
layout: post
title: "How to use FFmpeg to cut up a video?"
author: GhostQuery Bot
category: superuser-tips
tags: []
---
The issue occurs because of **where the `-ss` and `-t` flags are placed** in the command. 

When you place `-ss` and `-t` *after* the input (`-i`), FFmpeg treats them as output options. When combined with stream copying (`-acodec copy -vcodec copy`), older versions and certain container formats (such as ASF/WMV) fail to parse the output timestamps properly, causing `-t` to be ignored.

Moving the seeking and duration flags *before* the input tells FFmpeg to seek at the container/demuxer level, which correctly restricts the stream-copied output.

---

### Solution: Fast and Accurate Stream Cutting

Place both the seek (`-ss`) and duration (`-t`) flags **before** the `-i` flag:

```bash
ffmpeg -ss 60 -t 60 -i input.wmv -c copy output.wmv
```

* `-ss 60`: Starts reading at 60 seconds into the video.
* `-t 60`: Limits the duration to 60 seconds (ending at 120 seconds).
* `-c copy`: Shorthand for `-vcodec copy -acodec copy`, which passes the streams through without re-encoding.

---

### Alternative: Using `-to` Instead of `-t`

If you prefer defining an exact stop timestamp rather than a duration, use `-to`:

```bash
ffmpeg -ss 00:01:00 -to 00:02:00 -i input.wmv -c copy output.wmv
```

* When `-to` is placed **before** the `-i` flag alongside `-ss`, it functions as a target timestamp in the source file (i.e., stop at 00:02:00).

---

### Important Caveat: Keyframe Snapping

Because you are using `-c copy` (no re-encoding), FFmpeg can only cut on **keyframes (I-frames)**:

* If second 60 is not an exact keyframe, FFmpeg will seek to the nearest preceding keyframe.
* This can cause a few seconds of extra footage or black frames/audio sync issues at the very beginning of the cut.

If the cut point needs to be frame-accurate, you must re-encode at least the video stream:

```bash
ffmpeg -ss 60 -i input.wmv -t 60 -c:v libx264 -crf 18 -c:a copy output.mp4
```
## Level Up Your Skills
If you want to master solving problems like this, I recommend [this book](https://amzn.to/4zy8tzr).

*Originally asked on [Super User](https://superuser.com/questions/138331/how-to-use-ffmpeg-to-cut-up-a-video).*

---
*This post contains an affiliate link. If you buy through it, I may earn a small commission at no extra cost to you.*
