import re

# 1. Update index.css
with open('index.css', 'r') as f:
    css = f.read()

css = css.replace(
    ".agenda-details h3 {\n    display: none; /* Hide H3 since we use logos now */\n}",
    ".agenda-details h3 {\n    display: none; /* Hide H3 since we use logos now */\n}\n\n.agenda-item.no-logo .agenda-logo {\n    display: none;\n}\n\n.agenda-item.no-logo .agenda-details h3 {\n    display: block;\n    margin-bottom: 0.5rem;\n    font-size: 1.6rem;\n    color: var(--accent-color);\n}"
)

with open('index.css', 'w') as f:
    f.write(css)

# 2. Update index.html
with open('index.html', 'r') as f:
    html = f.read()

# Replace Black Label Society event
bls_old = """<div class="agenda-date"><span class="month">ABR</span><span class="day">23</span></div>
                        <div class="agenda-details"><h3>Black Label Society</h3><p>Foro Velódromo | 23 de abril</p></div>
                        <a href="#" class="btn-secondary">Tickets</a>"""

bls_new = """<div class="agenda-date"><span class="month">ABR</span><span class="day">--</span></div>
                        <div class="agenda-details"><h3>Black Label Society</h3><p>Foro Velódromo | <span style="color: red;">Cancelado</span></p></div>
                        <a href="#" class="btn-secondary" style="pointer-events: none; opacity: 0.5;">Tickets</a>"""

html = html.replace(bls_old, bls_new)

# Replace onerror in all imgs
html = re.sub(
    r'onerror="this\.onerror=null; this\.src=\'https://placehold\.co/.*?\'"',
    r'onerror="this.style.display=\'none\'; this.closest(\'.agenda-item\').classList.add(\'no-logo\');"',
    html
)

with open('index.html', 'w') as f:
    f.write(html)
