from PIL import Image

def remove_white(input_path, output_path, tolerance=200):
    img = Image.open(input_path).convert("RGBA")
    datas = img.getdata()
    newData = []
    for item in datas:
        if item[0] > tolerance and item[1] > tolerance and item[2] > tolerance:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    img.putdata(newData)
    img.save(output_path, "PNG")

remove_white('/Users/juancarenales/.gemini/antigravity/brain/aa680c66-20d4-4d12-8045-aff2ebd4e89f/media__1780808600388.png', 'assets/logo-new.png')
