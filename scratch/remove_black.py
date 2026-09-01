from PIL import Image
import glob
import os

def remove_black(path):
    try:
        img = Image.open(path).convert("RGBA")
        datas = img.getdata()
        newData = []
        for item in datas:
            # If pixel is completely black or very close
            if item[0] < 15 and item[1] < 15 and item[2] < 15:
                newData.append((0, 0, 0, 0))
            else:
                newData.append(item)
        img.putdata(newData)
        img.save(path, "WEBP")
        print(f"Processed {path}")
    except Exception as e:
        print(f"Error processing {path}: {e}")

for f in glob.glob("updates/icon_home*"):
    remove_black(f)

for f in glob.glob("updates/header_logo*"):
    remove_black(f)

