from PIL import Image, ImageOps
import os
import glob
import re

folder = 'assets/logos/'

def make_transparent_and_resize(path, target_height=100):
    try:
        img = Image.open(path).convert("RGBA")
        
        # Check corners to guess background color (white or black)
        w, h = img.size
        corners = [
            img.getpixel((0, 0)),
            img.getpixel((w-1, 0)),
            img.getpixel((0, h-1)),
            img.getpixel((w-1, h-1))
        ]
        
        # calculate average brightness of corners
        avg_brightness = sum([sum(c[:3])/3 for c in corners]) / 4
        
        # Convert to grayscale for alpha mask
        gray = img.convert("L")
        
        if avg_brightness > 127: # Background is likely white
            # We want dark pixels to be opaque, light pixels to be transparent
            gray = ImageOps.invert(gray)
            cutoff = 200 # Brightness above 200 becomes fully transparent
            # cutoff in inverted means original was < 55. 
            gray = gray.point(lambda p: 0 if p < 50 else p)
        else:
            # Background is likely black
            # We want light pixels to be opaque, dark pixels to be transparent
            cutoff = 40
            gray = gray.point(lambda p: 0 if p < cutoff else int((p - cutoff) * (255 / (255 - cutoff))))
            
        # create new image with solid color based on whether text was white or black
        # actually, let's preserve the original colors but just set the alpha channel
        new_img = img.copy()
        new_img.putalpha(gray)
        
        # Resize to standard height while maintaining aspect ratio
        aspect = w / h
        new_w = int(target_height * aspect)
        new_img = new_img.resize((new_w, target_height), Image.Resampling.LANCZOS)
        
        # Save as png
        base_name = os.path.splitext(os.path.basename(path))[0]
        out_path = os.path.join(folder, base_name + '.png')
        new_img.save(out_path, "PNG")
        
        # Remove old jpg if it was a jpg
        if path.lower().endswith('.jpg') or path.lower().endswith('.jpeg'):
            os.remove(path)
            
        return base_name + '.png'
    except Exception as e:
        print(f"Error processing {path}: {e}")
        return None

# Process all images in assets/logos
for img_path in glob.glob(os.path.join(folder, '*.*')):
    if img_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        # Process and replace
        make_transparent_and_resize(img_path)

print("Images processed.")

# Update index.html to replace .jpg with .png
html_path = 'index.html'
with open(html_path, 'r') as f:
    html = f.read()

# Replace any src="assets/logos/XXX.jpg" with .png
html = re.sub(r'(src="assets/logos/[^"]+)\.jpg"', r'\1.png"', html, flags=re.IGNORECASE)

with open(html_path, 'w') as f:
    f.write(html)
print("HTML updated for image paths.")
