import re

html_path = 'index.html'
with open(html_path, 'r') as f:
    html = f.read()

# Remove the old flags next to youtube buttons
flags = ['🇸🇪', '🇵🇦', '🇲🇽', '🇪🇸']
for flag in flags:
    old_flag_str = f'\n                            <span style="font-size: 1.5rem; display: flex; align-items: center; justify-content: center; margin-left: 0.5rem;">{flag}</span>'
    html = html.replace(old_flag_str, '')

# We will inject the new circular flag as the FIRST element inside <div class="episode-actions" ...>
def inject_circular_flag(html_str, title, flag):
    # Find <h3>{title}</h3> ... <div class="episode-actions"[^>]*>
    pattern = re.compile(rf'(<h3>{title}</h3>.*?<div class="episode-actions"[^>]*>)', re.DOTALL)
    
    circular_flag_html = f'\n                            <span style="display: flex; align-items: center; justify-content: center; width: 40px; height: 40px; border-radius: 50%; background-color: var(--bg-main, #111); border: 2px solid var(--accent-color); font-size: 1.2rem; margin-right: auto; box-shadow: 0 2px 8px rgba(0,0,0,0.5);">{flag}</span>'
    
    def replacer(match):
        return match.group(1) + circular_flag_html
        
    return pattern.sub(replacer, html_str, count=1)

html = inject_circular_flag(html, 'Ominum', '🇸🇪')
html = inject_circular_flag(html, 'Athica', '🇵🇦')
html = inject_circular_flag(html, 'Stay Design', '🇲🇽')
html = inject_circular_flag(html, 'Honara', '🇪🇸')

with open(html_path, 'w') as f:
    f.write(html)

print("Moved to bottom left circular!")
