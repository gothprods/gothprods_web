import re

html_path = 'index.html'
with open(html_path, 'r') as f:
    html = f.read()

# 1. First, we remove all flags from card-image
# The flags are like: <span style="position: absolute; bottom: 8px; right: 8px; font-size: 1.8rem; filter: drop-shadow(0px 2px 4px rgba(0,0,0,0.8));">🇸🇪</span>
html = re.sub(
    r'\s*<span style="position: absolute; bottom: 8px; right: 8px; font-size: 1.8rem; filter: drop-shadow\(0px 2px 4px rgba\(0,0,0,0\.8\)\);">([^<]+)</span>',
    '',
    html
)

# And remove "position: relative;" from the background-image styles in those cards
html = html.replace(' position: relative;"', '"')

# 2. Add flags next to YouTube buttons for specific sections
# We'll match each card by its unique title or youtube link to make sure we append the correct flag.

def add_flag_to_card(html, title, flag):
    # Match the block for the specific card. We can search for the title in <h3>
    # and then find the closing </div> of episode-actions.
    # It's safer to find the <h3>Title</h3>, then find the youtube platform-btn.
    
    # regex to find the youtube button within the same interview-card-horizontal
    # that contains the title.
    # We look for <h3>{title}</h3> ... <a href="[^"]*" target="_blank" class="platform-btn"[^>]*><i class="fa-brands fa-youtube"></i></a>
    
    pattern = re.compile(rf'(<h3>{title}</h3>.*?<a href="[^"]*" target="_blank" class="platform-btn" style="[^"]*"><i class="fa-brands fa-youtube"></i></a>)', re.DOTALL)
    
    def replacer(match):
        return match.group(1) + f'\n                            <span style="font-size: 1.5rem; display: flex; align-items: center; justify-content: center;">{flag}</span>'
        
    return pattern.sub(replacer, html)

# Stay Design needs align-items: center added to its episode-actions
# Actually let's just make sure all episode-actions have align-items: center
html = html.replace('style="display: flex; gap: 0.5rem; flex-wrap: wrap;"', 'style="display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap;"')

html = add_flag_to_card(html, 'Ominum', '🇸🇪')
html = add_flag_to_card(html, 'Athica', '🇵🇦')
html = add_flag_to_card(html, 'Stay Design', '🇲🇽')
html = add_flag_to_card(html, 'Honara', '🇪🇸')

with open(html_path, 'w') as f:
    f.write(html)

print("Flags moved!")
