import re

html_path = 'index.html'
with open(html_path, 'r') as f:
    html = f.read()

# 1. Update Ominum
html = re.sub(
    r'(<div class="card-image"\s*style="background-image: url\(\'https://img\.youtube\.com/vi/ZxZ2Uht40bA/maxresdefault\.jpg\'\);")',
    r'\1 position: relative;">\n                            <span style="position: absolute; bottom: 8px; right: 8px; font-size: 1.8rem; filter: drop-shadow(0px 2px 4px rgba(0,0,0,0.8));">🇸🇪</span>\n                        <!-- OMINUM FLAG END -->',
    html
)
# Fix the double closing tag if the above regex didn't consume `>`. Ah wait, the regex above matches up to `"` then replaces it with `... position: relative;">`. The original had `;"></div>` but since the regex only matched `;"`, it leaves `></div>` un-replaced, which is wrong.

# Let's do it safer:
with open(html_path, 'r') as f:
    html = f.read()

# Ominum
html = re.sub(
    r'(background-image:\s*url\(\'https://img\.youtube\.com/vi/ZxZ2Uht40bA/maxresdefault\.jpg\'\);?)([^>]*>)\s*</div>',
    r'\1 position: relative;\2\n                            <span style="position: absolute; bottom: 8px; right: 8px; font-size: 1.8rem; filter: drop-shadow(0px 2px 4px rgba(0,0,0,0.8));">🇸🇪</span>\n                        </div>',
    html
)

# Athica
html = re.sub(
    r'(background-image:\s*url\(\'https://img\.youtube\.com/vi/RjHD5Jtx4sM/maxresdefault\.jpg\'\);?)([^>]*>)\s*</div>',
    r'\1 position: relative;\2\n                            <span style="position: absolute; bottom: 8px; right: 8px; font-size: 1.8rem; filter: drop-shadow(0px 2px 4px rgba(0,0,0,0.8));">🇵🇦</span>\n                        </div>',
    html
)

# Honara
html = re.sub(
    r'(background-image:\s*url\(\'https://img\.youtube\.com/vi/2GDTVHHIRI8/maxresdefault\.jpg\'\);?)([^>]*>)\s*</div>',
    r'\1 position: relative;\2\n                            <span style="position: absolute; bottom: 8px; right: 8px; font-size: 1.8rem; filter: drop-shadow(0px 2px 4px rgba(0,0,0,0.8));">🇪🇸</span>\n                        </div>',
    html
)

# Stay Design Updates
# We need to change RjHD5Jtx4sM to G4Z3MhWUzdA but ONLY for Stay Design.
# Stay Design is inside the 3rd interview card.
# Let's match the Stay Design block:
stay_design_pattern = re.compile(r'(<!-- Stay Design -->.*?)(<!-- Honara -->)', re.DOTALL)
match = stay_design_pattern.search(html)
if match:
    block = match.group(1)
    
    # Replace thumb
    block = re.sub(r'https://img\.youtube\.com/vi/RjHD5Jtx4sM/maxresdefault\.jpg', 'https://img.youtube.com/vi/G4Z3MhWUzdA/maxresdefault.jpg', block)
    # Replace YT link
    block = re.sub(r'https://youtu\.be/RjHD5Jtx4sM\?si=BhmmGOLS7WL6-MR5', 'https://youtu.be/G4Z3MhWUzdA?si=obZScR1Kd7d9aO2w', block)
    # Replace Spotify link
    block = re.sub(r'https://open\.spotify\.com/episode/1GCf4eU2rpnZrvdpwtlYvz\?si=4946680075df47e4', 'https://open.spotify.com/episode/1GCf4eU2rpnZrvdpwtlYvz?si=d43b01a194924da0', block)
    
    html = html.replace(match.group(1), block)

with open(html_path, 'w') as f:
    f.write(html)

print("Applied!")
