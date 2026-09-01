from PIL import Image
import glob

paths = glob.glob("updates/icon_home*")
if paths:
    img = Image.open(paths[0]).convert("RGB")
    px = img.getpixel((0,0))
    print("PIXEL COLOR:", px)
    if px[0] > 200 and px[1] > 200 and px[2] > 200:
        print("WHITE")
    elif px[0] < 50 and px[1] < 50 and px[2] < 50:
        print("BLACK")
    else:
        print("OTHER")
else:
    print("NO FILE")
