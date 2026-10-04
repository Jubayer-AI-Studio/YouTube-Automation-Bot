import os
import sys
import pickle
from pathlib import Path
from typing import Dict, Any, List

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from config import CLIENT_SECRETS_FILE, TOKEN_PICKLE_FILE

# Scopes needed to upload videos and set thumbnails
SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl"
]

def get_authenticated_youtube_service():
    """
    Authenticates with YouTube Data API v3 using OAuth 2.0.
    Stores user credentials in token.pickle for subsequent automatic runs.
    """
    if not CLIENT_SECRETS_FILE.exists():
        print(f"\n[Notice] {CLIENT_SECRETS_FILE.name} not found!")
        print("To enable automatic uploads to your channel:")
        print("1. Go to Google Cloud Console (console.cloud.google.com)")
        print("2. Enable 'YouTube Data API v3'")
        print("3. Create OAuth 2.0 Client ID credentials (Desktop app)")
        print(f"4. Download JSON and save as: {CLIENT_SECRETS_FILE}\n")
        return None

    credentials = None
    if TOKEN_PICKLE_FILE.exists():
        with open(TOKEN_PICKLE_FILE, "rb") as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRETS_FILE), SCOPES)
            print("\n🔗 Opening browser for YouTube authorization... Please log in and click Allow.")
            sys.stdout.flush()
            credentials = flow.run_local_server(port=8088, prompt="consent")

        with open(TOKEN_PICKLE_FILE, "wb") as token:
            pickle.dump(credentials, token)

    return build("youtube", "v3", credentials=credentials)

def upload_video_to_youtube(
    video_path: Path,
    title: str,
    description: str,
    tags: List[str],
    privacy_status: str = "unlisted",  # 'private', 'unlisted', or 'public'
    thumbnail_path: Path = None
) -> Dict[str, Any]:
    """
    Uploads a video to YouTube with SEO metadata and optional custom thumbnail.
    """
    youtube = get_authenticated_youtube_service()
    if not youtube:
        print("[Dry-Run] Simulated successful YouTube upload (API credentials pending).")
        return {
            "status": "simulated",
            "video_id": "SIMULATED_ID",
            "url": f"https://youtu.be/simulated",
            "title": title
        }

    body = {
        "snippet": {
            "title": title[:100],
            "description": description[:5000],
            "tags": tags[:30],
            "categoryId": "28"  # Science & Technology
        },
        "status": {
            "privacyStatus": privacy_status,
            "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload(str(video_path), mimetype="video/mp4", resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    
    print(f"Uploading {video_path.name} to YouTube ({privacy_status})...")
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%...")

    video_id = response.get("id")
    video_url = f"https://youtu.be/{video_id}"
    print(f"✅ Video uploaded successfully! Video URL: {video_url}")

    # Upload thumbnail if available
    if thumbnail_path and thumbnail_path.exists():
        try:
            print(f"Setting custom thumbnail for video {video_id}...")
            youtube.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(str(thumbnail_path), mimetype="image/png")
            ).execute()
            print("✅ Thumbnail updated successfully!")
        except Exception as e:
            print(f"[Tip/Notice] Custom thumbnail not applied: {e}")
            print("Note: To enable custom thumbnails on YouTube, verify your phone number once at youtube.com/verify.")

    return {
        "status": "success",
        "video_id": video_id,
        "url": video_url,
        "title": title
    }

if __name__ == "__main__":
    print("Testing YouTube uploader module...")
    status = upload_video_to_youtube(
        video_path=Path("assets/video/test_rendered_short.mp4"),
        title="Test Autonomous AI Short",
        description="SEO description test",
        tags=["AI", "Test"],
        privacy_status="unlisted"
    )
    print(status)
