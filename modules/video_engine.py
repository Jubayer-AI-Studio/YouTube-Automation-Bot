import os
import sys
import random
import subprocess
from pathlib import Path
from typing import List, Tuple
from config import VIDEO_DIR, TEMP_DIR, ASSETS_DIR, AUDIO_DIR, SHORTS_WIDTH, SHORTS_HEIGHT, CHANNEL_NAME

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

STOCK_DIR = ASSETS_DIR / "stock"
STOCK_DIR.mkdir(parents=True, exist_ok=True)
BG_MUSIC_PATH = AUDIO_DIR / "epic_bg_music.m4a"

def get_media_duration(file_path: Path) -> float:
    """Returns duration in seconds using ffprobe."""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(file_path)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(result.stdout.strip())

def clean_script_for_subtitles(script: str) -> List[str]:
    """Cleans script text and breaks into short, punchy 3-5 word chunks."""
    script = script.replace("—", " ").replace("–", " ").replace("-", " ")
    words = script.split()
    chunks = []
    current = []
    
    for word in words:
        current.append(word)
        if len(current) >= 4 or word.endswith((".", "!", "?", ",")):
            clean_chunk = " ".join(current).strip()
            if clean_chunk and clean_chunk not in [".", "!", "?", ","]:
                chunks.append(clean_chunk)
            current = []
            
    if current:
        chunks.append(" ".join(current).strip())
    return chunks

def build_timed_chunks(script: str, total_duration: float) -> List[Tuple[float, float, str]]:
    """Calculates start and end timestamps for each subtitle chunk."""
    chunks = clean_script_for_subtitles(script)
    if not chunks:
        chunks = [script]

    word_counts = [max(1, len(c.split())) for c in chunks]
    total_words = sum(word_counts)
    
    timed = []
    current_time = 0.0
    for chunk, count in zip(chunks, word_counts):
        duration = (count / total_words) * total_duration
        end_time = current_time + duration
        clean_text = chunk.upper().replace('"', '').replace("'", "").replace(":", " ")
        timed.append((current_time, end_time, clean_text))
        current_time = end_time
    return timed

def assemble_multicut_background(total_duration: float) -> Path:
    """
    Selects 3-4 Hollywood action clips and stitches them into a fast-paced
    multi-scene background video that cuts every 5-7 seconds.
    """
    all_clips = [
        STOCK_DIR / "jarvis_hud.mp4",
        STOCK_DIR / "robot_tunnel_action.mp4",
        STOCK_DIR / "action_robot_1.mp4",
        STOCK_DIR / "ai_network_2.mp4",
        STOCK_DIR / "cyberpunk_1.mp4"
    ]
    # Filter only existing clips
    available = [c for c in all_clips if c.exists()]
    if not available:
        available = list(STOCK_DIR.glob("*.mp4"))

    # Randomly shuffle so each video is unique
    selected_clips = list(available)
    random.shuffle(selected_clips)
    
    output_bg = TEMP_DIR / "multicut_bg.mp4"
    
    # Cut segments of ~6 seconds from each clip until total duration is met
    segment_duration = 6.0
    num_segments = int(total_duration / segment_duration) + 2
    
    segment_files = []
    for i in range(num_segments):
        src_clip = selected_clips[i % len(selected_clips)]
        seg_out = TEMP_DIR / f"seg_{i}.mp4"
        cmd = [
            "ffmpeg", "-y",
            "-stream_loop", "-1",
            "-i", str(src_clip),
            "-t", str(segment_duration),
            "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-an",
            str(seg_out)
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        segment_files.append(seg_out)
        
    # Create concat list
    concat_list_path = TEMP_DIR / "concat_list.txt"
    with open(concat_list_path, "w", encoding="utf-8") as f:
        for seg in segment_files:
            f.write(f"file '{seg.name}'\n")
            
    # Concatenate segments
    concat_cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list_path),
        "-c", "copy",
        str(output_bg)
    ]
    subprocess.run(concat_cmd, cwd=str(TEMP_DIR), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    return output_bg

def render_short_video(
    audio_path: Path,
    script_text: str,
    output_filename: str = "short_video.mp4",
    bg_video_path: Path = None
) -> Path:
    """
    Renders a Hollywood / Marvel / JARVIS style Short:
    - Multi-scene cuts every 5-6 seconds
    - Epic bass background music with audio ducking
    - Center-stage punchy bold captions with glowing black background
    - Channel watermark header
    """
    output_path = VIDEO_DIR / output_filename
    duration = get_media_duration(audio_path)
    
    # 1. Multi-scene action background
    print("🎬 Assembling Hollywood multi-scene action cuts (JARVIS / Mecha / CGI)...")
    bg_video = assemble_multicut_background(duration)
    
    # 2. Build Timed Captions
    timed_chunks = build_timed_chunks(script_text, duration)
    
    header_text = f"{CHANNEL_NAME.upper()}"
    
    filters = [
        f"drawtext=text='{header_text}':fontcolor=yellow:fontsize=46:box=1:boxcolor=black@0.75:boxborderw=18:x=(w-text_w)/2:y=180"
    ]
    
    for start, end, text in timed_chunks:
        filters.append(
            f"drawtext=text='{text}':enable='between(t,{start:.2f},{end:.2f})':"
            f"fontcolor=white:fontsize=58:box=1:boxcolor=black@0.85:boxborderw=22:"
            f"x=(w-text_w)/2:y=(h-text_h)/2"
        )
        
    vf = ",".join(filters)

    # 3. Audio Mixing: Voice + Epic Bass Background Music
    if BG_MUSIC_PATH.exists():
        print("🔊 Mixing epic bass background music with voiceover...")
        # Voice is input 1, Music is input 2
        # Duck music to 18% volume, mix with voice, normalize
        filter_complex = (
            f"[0:v]{vf}[v];"
            f"[2:a]volume=0.18,aloop=loop=-1:size=2e+09[bgm];"
            f"[1:a][bgm]amix=inputs=2:duration=first:dropout_transition=2[a]"
        )
        cmd = [
            "ffmpeg", "-y",
            "-i", str(bg_video),
            "-i", str(audio_path),
            "-i", str(BG_MUSIC_PATH),
            "-filter_complex", filter_complex,
            "-map", "[v]",
            "-map", "[a]",
            "-c:v", "libx264",
            "-preset", "faster",
            "-crf", "22",
            "-c:a", "aac",
            "-b:a", "192k",
            "-t", str(duration),
            "-pix_fmt", "yuv420p",
            str(output_path)
        ]
    else:
        cmd = [
            "ffmpeg", "-y",
            "-i", str(bg_video),
            "-i", str(audio_path),
            "-vf", vf,
            "-map", "0:v",
            "-map", "1:a",
            "-c:v", "libx264",
            "-preset", "faster",
            "-crf", "22",
            "-c:a", "aac",
            "-b:a", "192k",
            "-t", str(duration),
            "-pix_fmt", "yuv420p",
            str(output_path)
        ]
        
    print(f"🚀 Rendering Hollywood-Tier Short -> [{output_filename}]...")
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)
    print(f"✅ Video created successfully: {output_path.name}")
    return output_path

if __name__ == "__main__":
    print("Testing Hollywood-tier multi-cut video engine...")
    sample_audio = Path("assets/audio/voice_20260922_222811.mp3")
    sample_script = (
        "OpenAI is quietly building Iron Man's JARVIS in real life. "
        "Humanoid combat robots are already learning combat moves in secret labs. "
        "The future of Marvel tech is arriving faster than you think."
    )
    res = render_short_video(sample_audio, sample_script, "hollywood_test.mp4")
    print(f"Generated: {res}")
