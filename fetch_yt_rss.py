import urllib.request
import xml.etree.ElementTree as ET
url = "https://www.youtube.com/feeds/videos.xml?channel_id=UCpFYBWWYJHgD5U0olc88s9A"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
response = urllib.request.urlopen(req).read()
root = ET.fromstring(response)
for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
    title = entry.find('{http://www.w3.org/2005/Atom}title').text
    media_group = entry.find('{http://search.yahoo.com/mrss/}group')
    desc_elem = media_group.find('{http://search.yahoo.com/mrss/}description') if media_group is not None else None
    desc = desc_elem.text if desc_elem is not None else "NO_DESC_ELEMENT"
    print(f"Title: {title}\nDesc: {desc}\n---")
