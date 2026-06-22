from PIL import Image

def remove_bg(path, is_white=False):
    try:
        img = Image.open(path).convert("RGBA")
        datas = img.getdata()
        newData = []
        for item in datas:
            # item is (R, G, B, A)
            if is_white:
                # If pixel is close to white, make transparent
                if item[0] > 200 and item[1] > 200 and item[2] > 200:
                    newData.append((255, 255, 255, 0))
                else:
                    newData.append(item)
            else:
                # If pixel is close to black, make transparent
                if item[0] < 50 and item[1] < 50 and item[2] < 50:
                    newData.append((0, 0, 0, 0))
                else:
                    newData.append(item)
        img.putdata(newData)
        img.save(path, "WEBP")
        print(f"Processed {path}")
    except Exception as e:
        print(f"Error processing {path}: {e}")

# Process Johny Metal and Metal Memes
remove_bg("updates/logo_aliado_3_962dbab4_JM.webp", is_white=False) # Assuming black background
remove_bg("updates/logo_aliado_4_2fcbfbac_Metal_Memes.webp", is_white=False) # Assuming black background

