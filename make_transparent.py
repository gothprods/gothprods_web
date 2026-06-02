from PIL import Image
import sys

def remove_black_background(input_path, output_path, tolerance=30):
    try:
        img = Image.open(input_path).convert("RGBA")
        datas = img.getdata()
        newData = []
        for item in datas:
            # item is (R, G, B, A)
            if item[0] < tolerance and item[1] < tolerance and item[2] < tolerance:
                # Make it transparent
                newData.append((0, 0, 0, 0))
            else:
                newData.append(item)
        img.putdata(newData)
        img.save(output_path, "PNG")
        print(f"Success! Saved to {output_path}")
    except Exception as e:
        print(f"Error: {e}")

remove_black_background("assets/logo.png", "assets/logo_transparent.png", 25)
