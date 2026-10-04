import sys
from typing import List, Dict, Any
from modules.youtube_uploader import get_authenticated_youtube_service
from modules.script_generator import call_openrouter
from config import OPENROUTER_API_KEY

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def generate_smart_reply(comment_text: str, video_title: str) -> str:
    """
    Generates a friendly, witty, engaging reply to a viewer's comment using OpenRouter AI.
    """
    if not OPENROUTER_API_KEY:
        return "Thanks for watching! More mind-blowing AI content coming soon! 🚀"

    prompt = f"""
You are the creator of "{video_title}" on a top AI YouTube channel.
A viewer left this comment: "{comment_text}"
Write a short (1-2 sentences), friendly, witty reply. Sound like an excited human tech enthusiast, NOT a bot.
Return only the reply text, nothing else.
"""
    try:
        # Use non-JSON mode for comment replies
        import requests, os
        from dotenv import load_dotenv
        load_dotenv()
        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"},
            json={"model": "qwen/qwen3.8-27b:free", "messages": [{"role": "user", "content": prompt}]},
            timeout=20
        )
        return r.json()["choices"][0]["message"]["content"].strip()
    except Exception:
        return "Appreciate you watching! Stay tuned for the next AI breakdown. 🧠⚡"

def reply_to_channel_comments():
    """
    Checks recent video comments and posts smart AI responses.
    """
    youtube = get_authenticated_youtube_service()
    if not youtube:
        print("[Notice] YouTube credentials not set. Comment bot is running in simulation mode.")
        sample_reply = generate_smart_reply("Is this actually real? Wow!", "AI Solves Quantum Physics")
        print(f"Simulated AI Reply: '{sample_reply}'")
        return

    try:
        # Fetch top recent comments on channel
        request = youtube.commentThreads().list(
            part="snippet",
            allThreadsRelatedToChannelId="UC3E01_Tm9zrrY7LWLAynNtA",
            maxResults=10,
            moderationStatus="published"
        )
        response = request.execute()
        
        for item in response.get("items", []):
            top_comment = item["snippet"]["topLevelComment"]["snippet"]
            comment_id = item["id"]
            author = top_comment["authorDisplayName"]
            text = top_comment["textDisplay"]
            
            print(f"Replying to {author}: '{text}'")
            # Reply using YouTube API
            reply_text = generate_smart_reply(text, "Latest AI Video")
            youtube.comments().insert(
                part="snippet",
                body={
                    "snippet": {
                        "parentId": comment_id,
                        "textOriginal": reply_text
                    }
                }
            ).execute()
            print(f"✅ Replied: '{reply_text}'")
    except Exception as e:
        print(f"[Warning] Comment bot encountered an issue: {e}")

if __name__ == "__main__":
    print("Testing comment bot...")
    reply_to_channel_comments()
