"""
MacTech iTool - Vector-Style Apple Forensic Shield & Logo Generator
Creates ultra-crisp Cupertino-inspired titanium Apple repair & diagnostic icons in multiple resolutions.
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_apple_icon(output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    size = 2048
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = size // 2, size // 2

    # 1. Outer Titanium / Cyber Shield Container
    bg_pad = 120
    radius = 380

    # Deep obsidian glass fill
    draw.rounded_rectangle(
        [bg_pad, bg_pad, size - bg_pad, size - bg_pad],
        radius=radius,
        fill=(11, 14, 20, 255),
        outline=(0, 113, 227, 255),  # Apple Electric Blue #0071E3
        width=28
    )

    # Inner cyan/indigo precision ring
    draw.rounded_rectangle(
        [bg_pad + 26, bg_pad + 26, size - bg_pad - 26, size - bg_pad - 26],
        radius=radius - 20,
        fill=None,
        outline=(0, 199, 190, 140),  # Apple Cyan #00C7BE
        width=10
    )

    # High-tech diagnostic grid lines
    grid_color = (25, 35, 52, 160)
    for offset in [-650, -450, -250, 0, 250, 450, 650]:
        draw.line([(bg_pad + 70, cy + offset), (size - bg_pad - 70, cy + offset)], fill=grid_color, width=6)
        draw.line([(cx + offset, bg_pad + 70), (cx + offset, size - bg_pad - 70)], fill=grid_color, width=6)

    # 2. Apple Silhouette Outline & Diagnostic Caduceus / Cross Motif
    # Apple Body
    body_r = 440
    body_cy = cy + 40
    # Left apple cheek
    draw.ellipse([cx - body_r - 20, body_cy - body_r, cx + 80, body_cy + body_r], fill=(0, 113, 227, 220))
    # Right apple cheek
    draw.ellipse([cx - 80, body_cy - body_r, cx + body_r + 20, body_cy + body_r], fill=(0, 113, 227, 220))
    # Bottom fill
    draw.ellipse([cx - 360, body_cy + 100, cx + 360, body_cy + body_r + 40], fill=(0, 113, 227, 220))
    # Apple Leaf at top
    leaf_cx = cx + 80
    leaf_cy = body_cy - body_r - 90
    draw.pieslice([leaf_cx - 160, leaf_cy - 160, leaf_cx + 160, leaf_cy + 160], start=30, end=150, fill=(48, 209, 88, 255))
    draw.pieslice([leaf_cx - 160, leaf_cy - 160, leaf_cx + 160, leaf_cy + 160], start=210, end=330, fill=(48, 209, 88, 255))

    # Diagnostic Stethoscope / Pulse wave across center
    pulse_pts = [
        (cx - 380, body_cy),
        (cx - 200, body_cy),
        (cx - 140, body_cy - 160),
        (cx - 60, body_cy + 180),
        (cx + 20, body_cy - 220),
        (cx + 100, body_cy + 120),
        (cx + 160, body_cy - 60),
        (cx + 220, body_cy),
        (cx + 380, body_cy)
    ]
    draw.line(pulse_pts, fill=(255, 255, 255, 255), width=24, joint="curve")

    # Hardware chip icon at bottom center
    chip_w, chip_h = 240, 160
    chip_y = body_cy + 220
    draw.rectangle([cx - chip_w // 2, chip_y - chip_h // 2, cx + chip_w // 2, chip_y + chip_h // 2], fill=(15, 23, 42, 240), outline=(0, 199, 190, 255), width=8)

    # 3. Downsample to standard sizes
    # icon-512.png
    img_512 = img.resize((512, 512), Image.Resampling.LANCZOS)
    img_512.save(os.path.join(output_dir, "icon.png"), "PNG")
    
    # icon.ico
    img_ico = img.resize((256, 256), Image.Resampling.LANCZOS)
    img_ico.save(os.path.join(output_dir, "icon.ico"), format="ICO", sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])

    # 4. Generate Banner Logo (1200x400)
    banner = Image.new("RGBA", (1400, 420), (11, 14, 20, 255))
    b_draw = ImageDraw.Draw(banner)
    
    # Left icon
    mini_icon = img.resize((320, 320), Image.Resampling.LANCZOS)
    banner.paste(mini_icon, (60, 50), mini_icon)

    # Gradient accent line
    b_draw.rectangle([420, 70, 426, 350], fill=(0, 113, 227, 255))

    # Text using default bitmap fallback or basic drawing
    # MacTech iTool branding text
    banner.save(os.path.join(output_dir, "logo.png"), "PNG")
    print(f"Generated icons in {output_dir}")

if __name__ == "__main__":
    base = os.path.dirname(os.path.abspath(__file__))
    create_apple_icon(base)
