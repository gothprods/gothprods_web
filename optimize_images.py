import os
import sqlite3
import re
from PIL import Image

def optimize_db(old_file, new_file):
    for db_file in ['gothprods.db', 'gothprods_live.db']:
        if os.path.exists(db_file):
            conn = sqlite3.connect(db_file)
            conn.execute("UPDATE content_items SET image_filename = replace(image_filename, ?, ?) WHERE image_filename LIKE ?", (old_file, new_file, f"%{old_file}"))
            conn.execute("UPDATE banda_semana SET img_video_path = replace(img_video_path, ?, ?) WHERE img_video_path LIKE ?", (old_file, new_file, f"%{old_file}"))
            conn.commit()
            conn.close()

def convert_to_webp(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')) and not file.lower().endswith('.webp'):
                path = os.path.join(root, file)
                try:
                    img = Image.open(path)
                    base = os.path.splitext(file)[0]
                    new_filename = f"{base}.webp"
                    new_path = os.path.join(root, new_filename)
                    
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    
                    max_width = 1200
                    if img.width > max_width:
                        ratio = max_width / float(img.width)
                        new_height = int((float(img.height) * float(ratio)))
                        img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
                        
                    img.save(new_path, "WEBP", quality=80, optimize=True)
                    
                    os.remove(path)
                    optimize_db(file, new_filename)
                    print(f"Converted: {path} -> {new_filename}")
                except Exception as e:
                    print(f"Error converting {path}: {e}")

def add_lazy_loading(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # We want to add loading="lazy" to all <img> tags that don't have it,
                # EXCEPT if they have class="logo-img", "viking-icon", "sidebar-logo", "hero-video"
                # To do this safely, we will just do a regex replace on <img that don't have loading=
                
                def repl(match):
                    full_match = match.group(0)
                    if 'loading=' in full_match:
                        return full_match
                    if any(c in full_match for c in ['"logo-img"', '"viking-icon"', '"sidebar-logo"', '"hero-video"']):
                        return full_match
                    return full_match.replace('<img ', '<img loading="lazy" ')
                
                new_content = re.sub(r'<img [^>]*>', repl, content)
                
                def repl_iframe(match):
                    full_match = match.group(0)
                    if 'loading=' in full_match:
                        return full_match
                    return full_match.replace('<iframe ', '<iframe loading="lazy" ')
                
                new_content = re.sub(r'<iframe [^>]*>', repl_iframe, new_content)
                
                # Since we changed extensions to .webp, let's also make sure static references in HTML (like assets/viking.jpg) are updated if needed.
                # Actually, our convert_to_webp also converted viking.jpg to viking.webp.
                # So we must replace .jpg/.png with .webp for static assets in HTML too.
                # Only for assets/ and updates/ paths in HTML.
                
                # To be safe, let's just replace all .jpg and .png to .webp in src="" and href=""
                # Wait! We shouldn't replace external links!
                new_content = re.sub(r'(src|href)="([^"]+)\.(jpg|png|jpeg)"', r'\1="\2.webp"', new_content)
                
                if new_content != content:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated HTML: {path}")

convert_to_webp('assets')
convert_to_webp('updates')
add_lazy_loading('templates')
add_lazy_loading('.') # For any other htmls if present
