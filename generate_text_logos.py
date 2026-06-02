import os
import re
from PIL import Image, ImageDraw, ImageFont

html_path = 'index.html'
with open(html_path, 'r') as f:
    html = f.read()

# Find all agenda items
# We look for <img src="assets/logos/X.png" ... alt="Y Logo" ...>
pattern = r'src="assets/logos/([^"]+\.png)"[^>]+alt="([^"]+) Logo"'
matches = re.findall(pattern, html)

# Try to use a heavy font
font_paths = [
    "/System/Library/Fonts/Supplemental/Impact.ttf",
    "/System/Library/Fonts/Supplemental/Arial Black.ttf",
    "/Library/Fonts/Impact.ttf",
    "/Library/Fonts/Arial Black.ttf"
]
font_path = None
for fp in font_paths:
    if os.path.exists(fp):
        font_path = fp
        break

if not font_path:
    font_path = "/System/Library/Fonts/Helvetica.ttc"

def generate_logo(filename, text):
    width, height = 400, 100
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Try different font sizes until it fits
    fontsize = 60
    font = None
    while fontsize > 10:
        try:
            font = ImageFont.truetype(font_path, fontsize)
        except:
            font = ImageFont.load_default()
            break
            
        # Get text bounding box
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        
        if tw < width - 20 and th < height - 20:
            break
        fontsize -= 2
        
    if font is None:
        font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        
    # Draw text with outline
    x = (width - tw) / 2
    y = (height - th) / 2
    
    # Outline
    outline_color = (200, 0, 0, 255) # Red outline
    text_color = (255, 255, 255, 255) # White text
    
    thickness = max(1, fontsize // 15)
    for adj_x in range(-thickness, thickness + 1):
        for adj_y in range(-thickness, thickness + 1):
            draw.text((x + adj_x, y + adj_y), text, font=font, fill=outline_color)
            
    draw.text((x, y), text, font=font, fill=text_color)
    
    out_path = os.path.join('assets/logos', filename)
    img.save(out_path, "PNG")
    print(f"Generated {filename} for {text}")

# Ensure directory exists
os.makedirs('assets/logos', exist_ok=True)

generated = set()
for filename, text in matches:
    if filename not in generated:
        generate_logo(filename, text)
        generated.add(filename)

print("All text logos generated successfully.")
