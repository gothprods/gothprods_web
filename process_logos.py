from PIL import Image, ImageOps
import os

folder = '/Users/juancarenales/Documents/Antigravity/assets/logos/'

def process_logo(filename, invert_mask=False, cutoff=20):
    path = os.path.join(folder, filename)
    if not os.path.exists(path):
        return
        
    img = Image.open(path).convert("RGB")
    
    # Convert to grayscale to use as alpha mask
    gray = ImageOps.grayscale(img)
    
    if invert_mask:
        # If it's black text on white bg (like gojira), invert it
        # so text becomes white (opaque) and bg becomes black (transparent)
        gray = ImageOps.invert(gray)
    
    # We can apply a point operation to enhance contrast and remove noise
    # Anything below cutoff becomes 0, anything above gets stretched
    gray = gray.point(lambda p: 0 if p < cutoff else int((p - cutoff) * (255 / (255 - cutoff))))
    
    # Create a solid color image based on the original's primary text color (assume white)
    new_img = Image.new("RGBA", img.size, (255, 255, 255, 255))
    
    # Put the calculated alpha mask
    new_img.putalpha(gray)
    
    # Save the processed image
    new_img.save(path)
    print(f"Processed {filename}")

# Metallica has dark gray background (up to 40-50). Let's use cutoff=60 to clear background noise.
process_logo('metallica.png', invert_mask=False, cutoff=55)

# Gojira has solid white bg, black text
process_logo('gojira.png', invert_mask=True, cutoff=20)

# Knocked Loose has black bg, white text
process_logo('knockedloose.png', invert_mask=False, cutoff=15)
