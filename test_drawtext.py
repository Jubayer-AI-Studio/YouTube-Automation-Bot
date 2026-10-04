import subprocess
from pathlib import Path

chunks = [
    (0.0, 3.0, "WHAT IF AN AI COULD REWRITE"),
    (3.0, 6.0, "ITS OWN CODE OVERNIGHT?"),
    (6.0, 9.0, "THAT IS ALREADY HAPPENING!")
]

filters = [
    "scale=1080:1920:force_original_aspect_ratio=increase",
    "crop=1080:1920",
    "drawtext=text='JUBAYER AI SPECIALIST':fontcolor=yellow:fontsize=44:box=1:boxcolor=black@0.7:boxborderw=16:x=(w-text_w)/2:y=180"
]

for start, end, text in chunks:
    clean_txt = text.replace('"', '').replace("'", "")
    filters.append(
        f"drawtext=text='{clean_txt}':enable='between(t,{start:.2f},{end:.2f})':"
        f"fontcolor=white:fontsize=56:box=1:boxcolor=black@0.8:boxborderw=20:"
        f"x=(w-text_w)/2:y=(h-text_h)/2"
    )

vf = ",".join(filters)
cmd = [
    "ffmpeg", "-y",
    "-stream_loop", "-1",
    "-i", "assets/stock/ai_network_2.mp4",
    "-vf", vf,
    "-t", "9",
    "-c:v", "libx264",
    "-preset", "ultrafast",
    "test_timed_drawtext.mp4"
]
res = subprocess.run(cmd, capture_output=True, text=True)
print("Return code:", res.returncode)
if res.returncode != 0:
    print(res.stderr[-400:])
else:
    print("SUCCESS! Rendered timed video.")
