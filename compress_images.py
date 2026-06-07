import os
from PIL import Image

def compress_directory(dir_name):
    max_dim = 1200
    for root, dirs, files in os.walk(dir_name):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                filepath = os.path.join(root, file)
                try:
                    size_kb = os.path.getsize(filepath) / 1024
                    if size_kb > 300:  # Only compress if larger than 300KB
                        img = Image.open(filepath)
                        modified = False
                        
                        # Resize if too large
                        if img.width > max_dim or img.height > max_dim:
                            img.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
                            modified = True
                        
                        if filepath.lower().endswith('.png'):
                            # For PNGs, if they are massive (e.g. > 1MB), they are likely photos saved as PNG.
                            # We can convert them to RGB and save as optimized JPG but keeping the same .png extension 
                            # so we don't break the database references.
                            # Browsers don't care about the extension, they read the magic bytes.
                            if size_kb > 1000:
                                if img.mode in ('RGBA', 'P', 'LA'):
                                    # Create a white background
                                    bg = Image.new('RGB', img.size, (255, 255, 255))
                                    if img.mode == 'RGBA':
                                        bg.paste(img, mask=img.split()[3])
                                    else:
                                        bg.paste(img)
                                    img = bg
                                else:
                                    img = img.convert('RGB')
                                img.save(filepath, 'JPEG', quality=85, optimize=True)
                                print(f"Compressed heavy PNG to JPEG format (kept .png ext): {filepath} (Was {size_kb:.1f}KB)")
                            else:
                                if modified:
                                    img.save(filepath, 'PNG', optimize=True)
                                    print(f"Resized and optimized PNG: {filepath} (Was {size_kb:.1f}KB)")
                        else:
                            if img.mode != 'RGB':
                                img = img.convert('RGB')
                            img.save(filepath, 'JPEG', quality=85, optimize=True)
                            print(f"Optimized JPG: {filepath} (Was {size_kb:.1f}KB)")
                except Exception as e:
                    print(f"Error compressing {filepath}: {e}")

compress_directory('assets')
compress_directory('updates')
print("Done compressing images.")
