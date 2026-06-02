from PIL import Image, ImageOps
import os

folder = '/Users/juancarenales/Documents/Antigravity/assets/logos/'

def process_logo(input_filename, output_filename, invert_mask=False, cutoff=20):
    input_path = os.path.join(folder, input_filename)
    output_path = os.path.join(folder, output_filename)
    if not os.path.exists(input_path):
        return
        
    img = Image.open(input_path).convert("RGB")
    gray = ImageOps.grayscale(img)
    
    if invert_mask:
        # If it's black text on white bg (like jinjer), invert it
        # so text becomes white (opaque) and bg becomes black (transparent)
        gray = ImageOps.invert(gray)
    
    gray = gray.point(lambda p: 0 if p < cutoff else int((p - cutoff) * (255 / (255 - cutoff))))
    
    new_img = Image.new("RGBA", img.size, (255, 255, 255, 255))
    new_img.putalpha(gray)
    new_img.save(output_path)
    print(f"Processed {input_filename} -> {output_filename}")

# Architects has black background, white text
process_logo('architects.jpg', 'architects.png', invert_mask=False, cutoff=20)

# Ill Nino has black background, white text
process_logo('illnino.jpg', 'ill_nino.png', invert_mask=False, cutoff=20)

# Jinjer has white background, black text
process_logo('jinjer.jpg', 'jinjer.png', invert_mask=True, cutoff=20)
