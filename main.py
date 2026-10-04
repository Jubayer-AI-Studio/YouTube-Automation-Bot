import os
import sys
import time
import argparse
from datetime import datetime
from pathlib import Path
import requests

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from modules.script_generator import generate_script_and_seo
from modules.voice_generator import generate_voice
from modules.thumbnail_engine import create_high_ctr_thumbnail
from modules.video_engine import render_short_video
from modules.youtube_uploader import upload_video_to_youtube
from modules.comment_bot import reply_to_channel_comments

def send_telegram_alert(message: str):
    """
    Sends real-time updates directly to your mobile phone via Telegram Bot.
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"[Warning] Failed to send Telegram alert: {e}")

def run_pipeline(topic: str = "", privacy: str = "unlisted"):
    """
    Executes the complete autonomous YouTube creation and upload pipeline.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    print("\n" + "=" * 60)
    print(f"🚀 STARTING AUTONOMOUS YOUTUBE PIPELINE [{timestamp}]")
    print("=" * 60)

    # 1. AI Script & SEO
    print("\n[Step 1/5] Generating viral script, hook, and SEO metadata...")
    blueprint = generate_script_and_seo(topic)
    print(f"🎬 Title: {blueprint['title']}")
    print(f"🔥 Hook: {blueprint['hook']}")

    # 2. Neural Voiceover
    print("\n[Step 2/5] Synthesizing ultra-realistic neural speech...")
    audio_file = f"voice_{timestamp}.mp3"
    audio_path = generate_voice(blueprint['script'], filename=audio_file)
    print(f"🎙️ Audio saved: {audio_path.name}")

    # 3. High-CTR Thumbnail
    print("\n[Step 3/5] Designing high-CTR thumbnail...")
    thumb_file = f"thumb_{timestamp}.png"
    thumb_path = create_high_ctr_thumbnail(
        hook_text=blueprint['hook'],
        badge_text="NEW BREAKTHROUGH",
        output_filename=thumb_file
    )
    print(f"🖼️ Thumbnail saved: {thumb_path.name}")

    # 4. Video Assembly & Burning Subtitles
    print("\n[Step 4/5] Rendering 1080x1920 Short video with burned subtitles...")
    video_file = f"short_{timestamp}.mp4"
    video_path = render_short_video(
        audio_path=audio_path,
        script_text=blueprint['script'],
        output_filename=video_file
    )
    print(f"📹 Video rendered: {video_path.name}")

    # 5. YouTube Upload
    print(f"\n[Step 5/5] Publishing to YouTube (Privacy: {privacy})...")
    upload_result = upload_video_to_youtube(
        video_path=video_path,
        title=blueprint['title'],
        description=blueprint['description'],
        tags=blueprint['tags'],
        privacy_status=privacy,
        thumbnail_path=thumb_path
    )

    # Send mobile notification
    msg = (
        f"<b>🤖 YouTube Autonomous Pipeline Complete!</b>\n\n"
        f"<b>Title:</b> {blueprint['title']}\n"
        f"<b>Status:</b> {upload_result.get('status')}\n"
        f"<b>URL:</b> {upload_result.get('url')}\n"
        f"<b>Time:</b> {datetime.now().strftime('%I:%M %p, %d %b %Y')}"
    )
    send_telegram_alert(msg)

    # Check & Reply to Comments
    print("\n💬 Running autonomous viewer comment replier...")
    reply_to_channel_comments()

    print("\n" + "=" * 60)
    print("🎉 PIPELINE RUN COMPLETED SUCCESSFULLY!")
    print("=" * 60 + "\n")
    return upload_result

def schedule_runner():
    """
    Runs the pipeline automatically twice daily (e.g., 2:00 PM and 9:00 PM).
    """
    print("\n⏰ Autonomous 24/7 Scheduler Started. Waiting for scheduled slots...")
    posted_today = set()

    while True:
        now = datetime.now()
        current_time_str = now.strftime("%H:%M")
        date_str = now.strftime("%Y-%m-%d")

        # Slot 1: 14:00 (2:00 PM BST / Morning US)
        # Slot 2: 21:00 (9:00 PM BST / Afternoon US)
        for slot in ["14:00", "21:00"]:
            key = f"{date_str}_{slot}"
            if current_time_str == slot and key not in posted_today:
                print(f"\n⏰ Triggering scheduled publication for {slot} slot...")
                try:
                    run_pipeline(privacy="public")
                    posted_today.add(key)
                except Exception as e:
                    print(f"❌ Scheduled run encountered an error: {e}")

        time.sleep(30)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autonomous YouTube Channel Pipeline")
    parser.add_argument("--topic", type=str, default="", help="Custom topic for the video")
    parser.add_argument("--privacy", type=str, default="unlisted", choices=["private", "unlisted", "public"], help="Privacy status for YouTube upload")
    parser.add_argument("--schedule", action="store_true", help="Start continuous 24/7 scheduler (posts 2x daily)")

    args = parser.parse_args()

    if args.schedule:
        schedule_runner()
    else:
        run_pipeline(topic=args.topic, privacy=args.privacy)
