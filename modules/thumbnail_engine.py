import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from config import THUMBNAIL_DIR

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def create_high_ctr_thumbnail(
    hook_text: str,
    badge_text: str = "AI BREAKTHROUGH",
    output_filename: str = "thumbnail.png"
) -> Path:
    """
    Generates a high-contrast 1280x720 YouTube thumbnail designed for high click-through-rates.
    """
    width, height = 1280, 720
    output_path = THUMBNAIL_DIR / output_filename
    
    # 1. Create dark tech gradient background
    img = Image.new("RGB", (width, height), color=(10, 14, 26))
    draw = ImageDraw.Draw(img)
    
    # Add subtle glowing radial effect in the center
    for r in range(400, 0, -20):
        alpha = int(25 * (1 - r / 400))
        draw.ellipse(
            [width//2 - r, height//2 - r, width//2 + r, height//2 + r],
            fill=(15 + alpha, 25 + alpha * 2, 60 + alpha * 3)
        )
        
    # Add cyber border
    draw.rectangle([15, 15, width - 15, height - 15], outline=(0, 229, 255), width=4)
    
    # 2. Draw Top Alert Badge (e.g. "AI BREAKTHROUGH" in neon yellow/orange)
    badge_x, badge_y = 60, 60
    # Try to load Arial or default system bold font
    try:
        font_badge = ImageFont.truetype("arialbd.ttf", 36)
        font_main = ImageFont.truetype("arialbd.ttf", 74)
        font_sub = ImageFont.truetype("arialbd.ttf", 46)
    except IOError:
        font_badge = ImageFont.load_default()
        font_main = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    badge_bbox = draw.textbbox((badge_x, badge_y), badge_text.upper(), font=font_badge)
    b_padding_x, b_padding_y = 25, 14
    draw.rounded_rectangle(
        [badge_x, badge_y, badge_bbox[2] + b_padding_x * 2, badge_bbox[3] + b_padding_y * 2],
        radius=12, fill=(255, 61, 0)
    )
    draw.text((badge_x + b_padding_x, badge_y + b_padding_y), badge_text.upper(), font=font_badge, fill=(255, 255, 255))
    
    # 3. Main Headline Words (Large, Bold, High Contrast)
    words = hook_text.upper().split()
    line1 = " ".join(words[:3]) if len(words) >= 3 else hook_text.upper()
    line2 = " ".join(words[3:7]) if len(words) > 3 else ""
    
    # Text with heavy black shadow for extreme legibility
    def draw_text_with_shadow(x, y, text, font, fill_color):
        shadow_offset = 6
        draw.text((x + shadow_offset, y + shadow_offset), text, font=font, fill=(0, 0, 0))
        draw.text((x, y), text, font=font, fill=fill_color)
        
    draw_text_with_shadow(60, 220, line1, font_main, (255, 255, 255))
    if line2:
        draw_text_with_shadow(60, 330, line2, font_main, (255, 235, 59))  # Neon Yellow
        
    # 4. Bottom Hook Tag (Dynamically fitted)
    tag_text = "MUST WATCH BEFORE 2027"
    tag_x, tag_y = 60, height - 130
    tag_bbox = draw.textbbox((tag_x, tag_y), tag_text, font=font_sub)
    draw.rounded_rectangle(
        [tag_x, tag_y, tag_bbox[2] + 40, tag_bbox[3] + 20],
        radius=8, fill=(0, 200, 83)
    )
    draw.text((tag_x + 20, tag_y + 10), tag_text, font=font_sub, fill=(0, 0, 0))
    
    img.save(str(output_path), quality=95)
    return output_path

if __name__ == "__main__":
    print("Testing thumbnail engine...")
    thumb = create_high_ctr_thumbnail("THEY BUILT IT! AI REVOLUTION", badge_text="SECRET TECH")
    print(f"Thumbnail created at: {thumb}")
