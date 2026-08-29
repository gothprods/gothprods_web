import urllib.request
import re

req = urllib.request.Request('https://www.youtube.com/channel/UCpFYBWWYJHgD5U0olc88s9A/videos', headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read().decode('utf-8')

match = re.search(r'var ytInitialData = (\{.*?\});</script>', html)
if match:
    data = match.group(1)
    # Search for any videoId and title in the JSON string
    import json
    parsed = json.loads(data)
    
    # Just extract videoId and title using regex from the JSON string directly!
    video_ids = re.findall(r'"videoId":"([^"]+)"', data)
    for vid in set(video_ids):
        # find title near it
        # this is hacky but might work
        pass
    
    # A better way: just print out all "title":{"runs":[{"text":"...
    titles = re.findall(r'"title":\{"runs":\[\{"text":"([^"]+)"', data)
    print("Found titles:", titles[:10])
    
