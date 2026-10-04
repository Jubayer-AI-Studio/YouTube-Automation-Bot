import os
import sys
import subprocess
import requests
from pathlib import Path
from typing import List
from config import PEXELS_API_KEY, TEMP_DIR, SHORTS_WIDTH, SHORTS_HEIGHT

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def search_pexels_videos(query: str, orientation: str = "portrait", per_page: int = 3) -> List[str]:
    """
    Searches Pexels for royalty-free HD video clips matching query.
    """
    if not PEXELS_API_KEY:
        print(f"[Notice] PEXELS_API_KEY not configured. Generating high-tech animated canvas...")
        return []

    url = f"https://api.pexels.com/videos/search?query={query}&orientation={orientation}&per_page={per_page}"
    headers = {"Authorization": PEXELS_API_KEY}
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        video_urls = []
        for video in data.get("videos", []):
            files = video.get("video_files", [])
            # Prefer 1080x1920 or highest HD mp4
            files.sort(key=lambda x: (x.get("width", 0) * x.get("height", 0)), reverse=True)
            for f in files:
                if f.get("file_type") == "video/mp4":
                    video_urls.append(f.get("link"))
                    break
        return video_urls
    except Exception as e:
        print(f"[Warning] Failed to fetch from Pexels: {e}")
        return []

def download_video(url: str, output_path: Path) -> Path:
    """
    Downloads a video file from URL.
    """
    res = requests.get(url, stream=True, timeout=30)
    res.raise_for_status()
    with open(output_path, "wb") as f:
        for chunk in res.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    return output_path

def generate_fallback_tech_background(output_path: Path, duration: int = 15, width: int = SHORTS_WIDTH, height: int = SHORTS_HEIGHT) -> Path:
    """
    Generates a stunning high-tech animated dark cyber canvas using FFmpeg lavfi.
    Works 100% offline without any external API or internet dependency!
    """
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", f"gradients=s={width}x{height}:c0=0x0d1117:c1=0x161b22:c2=0x1f6feb:speed=0.01",
        "-t", str(duration),
        "-pix_fmt", "yuv420p",
        "-c:v", "libx264",
        "-r", "30",
        str(output_path)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    return output_path

if __name__ == "__main__":
    print("Testing asset fetcher...")
    test_out = TEMP_DIR / "test_bg.mp4"
    generate_fallback_tech_background(test_out, duration=5)
    print(f"Fallback tech background generated successfully at: {test_out}")
