# YouTube Transcript Extractor

![Python](https://img.shields.io/badge/Made%20with-Python-blue.svg)
![yt-transcript](https://img.shields.io/badge/youtube--transcript--api-latest-red)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

Extracts subtitles from any YouTube video and saves them as a `.txt` file.

---

## Setup

1. `pip install youtube-transcript-api`
2. Run: `python main.py <URL or video_id> [lang]`

---

## Usage

```bash
python main.py https://youtu.be/dQw4w9WgXcQ
python main.py dQw4w9WgXcQ en
```

---

## Output

- Format: `.txt`
- Location: same folder as script
- Filename: `<video_id>.txt`
