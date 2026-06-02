from PIL import Image, ImageOps
import os

folder = '/Users/juancarenales/Documents/Antigravity/assets/logos/'

def process_logo(filename, invert_mask=False, cutoff=20):
    path = os.path.join(folder, filename)
    if not os.path.exists(path):
        return
        
    img = Image.open(path).convert("RGB")
    gray = ImageOps.grayscale(img)
    
    if invert_mask:
        gray = ImageOps.invert(gray)
    
    gray = gray.point(lambda p: 0 if p < cutoff else int((p - cutoff) * (255 / (255 - cutoff))))
    
    new_img = Image.new("RGBA", img.size, (255, 255, 255, 255))
    new_img.putalpha(gray)
    new_img.save(path)
    print(f"Processed {filename}")

process_logo('acdc.png', invert_mask=False, cutoff=20)
process_logo('dreamtheater.png', invert_mask=True, cutoff=20)
