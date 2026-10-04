import os
from pathlib import Path
from dotenv import load_dotenv

# Base Directories
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
AUDIO_DIR = ASSETS_DIR / "audio"
VIDEO_DIR = ASSETS_DIR / "video"
THUMBNAIL_DIR = ASSETS_DIR / "thumbnails"
TEMP_DIR = ASSETS_DIR / "temp"

for directory in [ASSETS_DIR, AUDIO_DIR, VIDEO_DIR, THUMBNAIL_DIR, TEMP_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Load environment variables
load_dotenv(BASE_DIR / ".env")

# API Keys
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = "qwen/qwen3.8-27b:free"   # Free, high-quality model via OpenRouter
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# Content Configuration
CHANNEL_NAME = "Jubayer AI Specialist"
CHANNEL_HANDLE = "@jubayeraispecialist"
DEFAULT_LANGUAGE = "en"
NICHE = (
    "AI News, Autonomous AI Breakthroughs, Recursive Self-Improvement, "
    "Cybersecurity AI Threats, Future Robotics & AGI (inspired by Matt Wolfe, TED, Forbes Tech)"
)

# Voice Settings (Edge-TTS Neural Voices)
VOICE_EN_MALE = "en-US-ChristopherNeural"  # Professional, engaging, confident
VOICE_EN_FEMALE = "en-US-AriaNeural"
VOICE_BN_MALE = "bn-BD-PradeepNeural"      # For optional Bengali audio track
VOICE_BN_FEMALE = "bn-BD-NabanitaNeural"

# Video Dimensions
SHORTS_WIDTH = 1080
SHORTS_HEIGHT = 1920
SHORTS_TARGET_DURATION = 40  # 35 - 45 seconds

LONG_VIDEO_WIDTH = 1920
LONG_VIDEO_HEIGHT = 1080
LONG_TARGET_DURATION = 240   # 4 minutes

# YouTube API Paths
CLIENT_SECRETS_FILE = BASE_DIR / "client_secrets.json"
TOKEN_PICKLE_FILE = BASE_DIR / "token.pickle"
