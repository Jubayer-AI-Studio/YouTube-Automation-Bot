<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=255,0,0,235,47,6&height=220&section=header&text=YouTube%20Automation%20Engine%20📺&fontSize=38&fontColor=fff&animation=twinkling&fontAlignY=38&desc=Autonomous%20Video%20Production%2C%20Thumbnail%20Card%20Engine%20%26%20Uploader&descFontSize=18&descAlignY=62" width="100%"/>

  [![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
  [![YouTube API](https://img.shields.io/badge/YouTube_Data_API-v3-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://developers.google.com/youtube/v3)
  [![Pillow](https://img.shields.io/badge/Pillow-Image_Generation-blue?style=for-the-badge)](https://python-pillow.org/)
  [![FFmpeg](https://img.shields.io/badge/FFmpeg-Video_Processing-007808?style=for-the-badge&logo=ffmpeg&logoColor=white)](https://ffmpeg.org/)
  [![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
</div>

---

# 📺 YouTube Automation Engine
> **End-to-End Autonomous Pipeline for Video Creation, Thumbnail Generation & Automated Uploads**

This Python-powered automation engine automates the entire content creator pipeline on YouTube: from generating automated thumbnail cards and rendering video sequences to scheduled publishing using the official YouTube Data API v3.

---

## 🌟 Core Modules

### 1. 🎨 Dynamic Thumbnail Generator (`modules/thumbnail_generator.py`)
* Automatically lays out typography, hero images, drop shadows, and high-contrast badges for high click-through rates (CTR).

### 2. 🎞️ Video Rendering Pipeline
* Combines audio commentary, background ambient tracks, and sequential scene frames with styled subtitles.

### 3. 🚀 YouTube Data API v3 Uploader (`modules/uploader.py`)
* Secure OAuth2 token refresh pipeline (`token.pickle`).
* Automatically formats titles, tags, categorized playlists, and privacy status (Public / Unlisted / Private).

---

## ⚡ Setup & Usage

```bash
# 1. Clone repository
git clone https://github.com/monisharani333022-eng/YouTube-Automation-Bot.git
cd YouTube-Automation-Bot

# 2. Install requirements
pip install -r requirements.txt

# 3. Configure credentials
# Copy your Google Cloud OAuth client secret as client_secrets.json
cp .env.example .env

# 4. Authenticate once with Google
python login.py

# 5. Run automation engine
python main.py
```

---

## 👤 Author

* **Developer:** [Jubayer Ahmad](https://github.com/monisharani333022-eng)
* **Email:** [monisharani333022@gmail.com](mailto:monisharani333022@gmail.com)
* **Location:** Dhaka, Bangladesh 🇧🇩

---

## 📄 License

Distributed under the MIT License.
