import urllib.request
import xml.etree.ElementTree as ET
url = "https://www.youtube.com/feeds/videos.xml?channel_id=UCpFYBWWYJHgD5U0olc88s9A"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
response = urllib.request.urlopen(req).read()
root = ET.fromstring(response)
for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
    title = entry.find('{http://www.w3.org/2005/Atom}title').text
    if 'Declaraciones' in title or 'Episodio 18' in title:
        pub = entry.find('{http://www.w3.org/2005/Atom}published').text
        print(f"Title: {title} | Published: {pub}")
