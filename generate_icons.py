import os
from PIL import Image, ImageDraw

def generate_icon(size, output_path):
    img = Image.new('RGBA', (size, size), (15, 23, 42, 255)) # #0f172a
    draw = ImageDraw.Draw(img)
    
    # Outer subtle rounded border / glow
    margin = int(size * 0.08)
    draw.rounded_rectangle([margin, margin, size - margin, size - margin], radius=int(size * 0.22), fill=(30, 41, 59, 255), outline=(56, 189, 248, 180), width=int(size * 0.025))
    
    # Inner watch / stopwatch circle
    center = size / 2
    r = int(size * 0.28)
    draw.ellipse([center - r, center - r, center + r, center + r], outline=(14, 165, 233, 255), width=int(size * 0.04))
    
    # Stopwatch top button
    btn_w = int(size * 0.08)
    btn_h = int(size * 0.05)
    btn_y = center - r - btn_h - int(size * 0.02)
    draw.rectangle([center - btn_w//2, btn_y, center + btn_w//2, btn_y + btn_h], fill=(56, 189, 248, 255))
    
    # Inner lightning / runner accent inside watch
    lw = int(size * 0.035)
    # Runner / pulse stylized line
    points = [
        (center - r * 0.55, center),
        (center - r * 0.2, center),
        (center - r * 0.05, center - r * 0.45),
        (center + r * 0.15, center + r * 0.4),
        (center + r * 0.3, center),
        (center + r * 0.55, center)
    ]
    draw.line(points, fill=(56, 189, 248, 255), width=lw, joint='curve')
    
    img.save(output_path, 'PNG')
    print(f"Generated {output_path} ({size}x{size})")

base_dir = r"C:\Users\yonim\.gemini\antigravity\scratch\amazfit-workout-bridge"
generate_icon(192, os.path.join(base_dir, "icon-192.png"))
generate_icon(512, os.path.join(base_dir, "icon-512.png"))
