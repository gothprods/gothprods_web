import urllib.request
import urllib.parse
import json

def get_wiki_logo(band_name):
    try:
        # Search for the band page
        search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(band_name)}&utf8=&format=json"
        req = urllib.request.Request(search_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            if not data['query']['search']:
                return None
            title = data['query']['search'][0]['title']
            
            # Get images on the page
            images_url = f"https://en.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(title)}&prop=images&imlimit=50&format=json"
            req2 = urllib.request.Request(images_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req2, timeout=10) as response2:
                data2 = json.loads(response2.read().decode())
                pages = data2['query']['pages']
                page_id = list(pages.keys())[0]
                if 'images' not in pages[page_id]:
                    return None
                    
                images = pages[page_id]['images']
                logo_title = None
                for img in images:
                    img_title = img['title'].lower()
                    if 'logo' in img_title and (img_title.endswith('.png') or img_title.endswith('.svg') or img_title.endswith('.jpg')):
                        logo_title = img['title']
                        break
                        
                if not logo_title:
                    return None
                    
                # Get the URL of the logo image
                # If SVG, we can request a rasterized PNG thumbnail by specifying iiurlwidth
                imageinfo_url = f"https://en.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(logo_title)}&prop=imageinfo&iiprop=url&iiurlwidth=400&format=json"
                req3 = urllib.request.Request(imageinfo_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req3, timeout=10) as response3:
                    data3 = json.loads(response3.read().decode())
                    img_pages = data3['query']['pages']
                    img_page_id = list(img_pages.keys())[0]
                    img_info = img_pages[img_page_id]['imageinfo'][0]
                    if 'thumburl' in img_info:
                        return img_info['thumburl']
                    return img_info['url']
    except Exception as e:
        print(f"Error: {e}")
    return None

print("AC/DC:", get_wiki_logo("AC/DC band"))
print("Dream Theater:", get_wiki_logo("Dream Theater band"))
print("Architects:", get_wiki_logo("Architects (British band)"))
