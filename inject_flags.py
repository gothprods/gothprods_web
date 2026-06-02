import re

html_path = 'index.html'
with open(html_path, 'r') as f:
    html = f.read()

def inject_flag(html_str, title, flag):
    # We find <h3>{title}</h3> then find the NEXT <i class="fa-brands fa-youtube"></i></a>
    # and we insert the span after the </a>
    pattern = re.compile(rf'(<h3>{title}</h3>.*?</i\s*>\s*</a>)', re.DOTALL)
    def replacer(match):
        return match.group(1) + f'\n                            <span style="font-size: 1.5rem; display: flex; align-items: center; justify-content: center; margin-left: 0.5rem;">{flag}</span>'
    return pattern.sub(replacer, html_str, count=1)

html = inject_flag(html, 'Ominum', '🇸🇪')
html = inject_flag(html, 'Athica', '🇵🇦')
html = inject_flag(html, 'Stay Design', '🇲🇽')
html = inject_flag(html, 'Honara', '🇪🇸')

with open(html_path, 'w') as f:
    f.write(html)
print("Done")
