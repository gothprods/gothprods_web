import os
import sys

# Ensure PIL is found, we know user_site is where we installed
user_site = os.path.expanduser('~/Library/Python/3.9/lib/python/site-packages')
if user_site not in sys.path:
    sys.path.append(user_site)

import urllib.request
import urllib.parse
import json
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

def create_placeholder(text, filename):
    img = Image.new('RGB', (800, 400), color=(0, 0, 0))
    d = ImageDraw.Draw(img)
    try:
        # Just drawing simple text
        d.text((50, 180), text, fill=(255, 255, 255))
    except Exception:
        pass
    img.save(filename, "JPEG")
    print(f"Created placeholder for {text}")

def search_wikipedia_image(query):
    search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(query)}&utf8=&format=json"
    try:
        req = urllib.request.Request(search_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            if not data['query']['search']:
                return None
            title = data['query']['search'][0]['title']
            
            page_url = f"https://en.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(title)}&prop=pageimages&format=json&pithumbsize=800"
            req2 = urllib.request.Request(page_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req2, timeout=10) as response2:
                data2 = json.loads(response2.read().decode())
                pages = data2['query']['pages']
                page_id = list(pages.keys())[0]
                if 'thumbnail' in pages[page_id]:
                    return pages[page_id]['thumbnail']['source']
    except Exception as e:
        print(f"Wikipedia error for {query}: {e}")
    return None

items = [
  {"query": "AC/DC band", "filename": "AC_DC.jpg"},
  {"query": "Dream Theater band", "filename": "Dream Theater.jpg"},
  {"query": "Ill Niño band", "filename": "Ill Nino.jpg"},
  {"query": "Jinjer band", "filename": "Jinjer.jpg"},
  {"query": "Architects (British band)", "filename": "Architects.jpg"},
  {"query": "Black Label Society band", "filename": "Black Label Society.jpg"},
  {"query": "Midnight (band)", "filename": "Midnigth.jpg"},
  {"query": "Amaranthe band", "filename": "Amaranthe.jpg"},
  {"query": "A.N.I.M.A.L.", "filename": "A.N.I.M.A.L.jpg"},
  {"query": "Twisted Sister band", "filename": "Twisted Sister (Sebastian Bach).jpg"},
  {"query": "Tankard (band)", "filename": "Tankard.jpg"},
  {"query": "Beyond Creation band", "filename": "Beyond Creation y Felluja.jpg"},
  {"query": "Vader (band)", "filename": "Vader.jpg"},
  {"query": "In Flames band", "filename": "In Flames.jpg"},
  {"query": "Megadeth band", "filename": "Megadeth.jpg"},
  {"query": "Gutalax band", "filename": "Gutalax.jpg"},
  {"query": "Dogma (band)", "filename": "Dogma.jpg"},
  {"query": "San Luis Metal Fest", "filename": "San Luís Metal Fest.jpg"},
  {"query": "Korn band", "filename": "Korn.jpg"},
  {"query": "Metallica band", "filename": "Metallica - Gojira y Knocked Loose.jpg"},
  {"query": "Metallica band", "filename": "Metallica - Pantera y Avatar.jpg"},
  {"query": "System of a Down band", "filename": "System Of A Down.jpg"},
  {"query": "Turilli / Lione Rhapsody band", "filename": "Turilli _ Lione Rhapsody.jpg"},
  {"query": "Rush (band)", "filename": "Rush.jpg"},
  {"query": "Lacrimosa (band)", "filename": "Lacrimosa.jpg"},
  {"query": "Helloween band", "filename": "Helloween.jpg"},
  {"query": "Ladrones (band)", "filename": "Ladrones.jpg"},
  {"query": "Candelabrum Metal Fest", "filename": "Candelabrum Metal Fest V.jpg"},
  {"query": "Sonata Arctica band", "filename": "Sonata Arctica.jpg"},
  {"query": "Iron Maiden band", "filename": "Iron Maiden.jpg"},
  {"query": "AfterShock Festival", "filename": "AfterShock - Putero de Bandas.jpg"},
  {"query": "Opeth band", "filename": "Opeth.jpg"},
  {"query": "ZZ Top band", "filename": "ZZtop.jpg"},
  {"query": "Knotfest festival", "filename": "Knotfest - Bad Omens, Lamb of God, Poppy, The Ghost Inside, Blood Incantation, Sylosis, Vana, y Versailles.jpg"},
  {"query": "Babymetal band", "filename": "Babymetal.jpg"},
  {"query": "Deep Purple band", "filename": "Deep Purple.jpg"},
  {"query": "Fear Factory band", "filename": "Heavy Metal X’Mas 2026 - Fear Factory.jpg"}
]

save_dir = "/Users/juancarenales/Documents/Antigravity"

for item in items:
    filename = item["filename"]
    filepath = os.path.join(save_dir, filename)
    if os.path.exists(filepath):
        print(f"Skipping {filename}")
        continue
        
    print(f"Searching Wikipedia for {item['query']}...")
    img_url = search_wikipedia_image(item['query'])
    
    if img_url:
        print(f"Found URL: {img_url}")
        req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                img_data = response.read()
                try:
                    img = Image.open(BytesIO(img_data))
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    img.save(filepath, "JPEG")
                    print(f"Saved {filename}")
                except Exception as e:
                    print(f"Failed to save image {filename}: {e}")
                    create_placeholder(item["query"], filepath)
        except Exception as e:
            print(f"Failed to download image {filename}: {e}")
            create_placeholder(item["query"], filepath)
    else:
        print(f"Could not find image for {item['query']}")
        create_placeholder(item["query"], filepath)

print("Done.")
