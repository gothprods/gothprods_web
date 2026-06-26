import urllib.request
import re
import json

url = "https://www.youtube.com/channel/UCpFYBWWYJHgD5U0olc88s9A/streams"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    match = re.search(r'var ytInitialData = (\{.*?\});</script>', html)
    if match:
        data = json.loads(match.group(1))
        tabs = data.get('contents', {}).get('twoColumnBrowseResultsRenderer', {}).get('tabs', [])
        for tab in tabs:
            if 'tabRenderer' in tab:
                url_path = tab['tabRenderer'].get('endpoint', {}).get('commandMetadata', {}).get('webCommandMetadata', {}).get('url', '')
                if '/streams' in url_path:
                    items = tab['tabRenderer']['content']['richGridRenderer']['contents']
                    for item in items:
                        if 'richItemRenderer' in item:
                            content = item['richItemRenderer']['content']
                            print(list(content.keys()))
except Exception as e:
    print("Error:", e)
