import urllib.request
import xml.etree.ElementTree as ET
url = "https://feeds.ivoox.com/feed_fg_f11154894_filtro_1.xml"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
response = urllib.request.urlopen(req).read()
root = ET.fromstring(response)
print("Ivoox feed items:")
for item in root.findall('.//item')[:15]:
    title = item.find('title').text
    pubDate = item.find('pubDate').text
    print(f"{pubDate} - {title}")
