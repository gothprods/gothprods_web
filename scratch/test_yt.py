import urllib.request
import re
import json

def fetch_videos(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read().decode('utf-8')
    match = re.search(r'var ytInitialData = (\{.*?\});</script>', html)
    if not match: return []
    data = json.loads(match.group(1))
    videos = []
    
    # Try to find the richGridRenderer
    def find_grid(node):
        if isinstance(node, dict):
            if 'richGridRenderer' in node:
                return node['richGridRenderer']
            for k, v in node.items():
                res = find_grid(v)
                if res: return res
        elif isinstance(node, list):
            for v in node:
                res = find_grid(v)
                if res: return res
        return None
        
    grid = find_grid(data)
    if grid:
        for item in grid.get('contents', []):
            if 'richItemRenderer' in item:
                content = item['richItemRenderer']['content']
                if 'videoRenderer' in content:
                    v = content['videoRenderer']
                    title = v['title']['runs'][0]['text']
                    videoId = v['videoId']
                    videos.append((title, videoId))
    return videos

print("Videos:", fetch_videos('https://www.youtube.com/channel/UCpFYBWWYJHgD5U0olc88s9A/videos'))
print("Streams:", fetch_videos('https://www.youtube.com/channel/UCpFYBWWYJHgD5U0olc88s9A/streams'))
