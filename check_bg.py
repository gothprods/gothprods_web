from PIL import Image
import os

folder = '/Users/juancarenales/Documents/Antigravity/assets/logos/'
for file in ['metallica.png', 'gojira.png', 'knockedloose.png']:
    path = os.path.join(folder, file)
    if os.path.exists(path):
        img = Image.open(path).convert("RGBA")
        width, height = img.size
        # Sample the corners to guess the background color
        corners = [
            img.getpixel((0, 0)),
            img.getpixel((width - 1, 0)),
            img.getpixel((0, height - 1)),
            img.getpixel((width - 1, height - 1))
        ]
        print(f"{file} dimensions: {width}x{height}, corner pixels: {corners}")
