import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Fix Dream Theater logo filename
html = html.replace('dream_theater.png', 'dreamtheater.png')

# 2. Add Viking badge to specific events
viking_html = '\n                        <img src="assets/viking.jpg" alt="Goth Prods Crew" class="agenda-viking-badge" title="El Crew de Goth Prods asistirá">'

events_to_badge = ['AC/DC', 'Dream Theater', 'Architects', 'Megadeth', 'System Of A Down']

def add_viking(match):
    full_str = match.group(0)
    # Check if the text matches any of the events
    for event in events_to_badge:
        if f'<h3>{event}</h3>' in full_str:
            # Avoid double insertion
            if 'agenda-viking-badge' not in full_str:
                return full_str.replace('<li class="agenda-item">', f'<li class="agenda-item">{viking_html}')
    return full_str

# Replace in li items
html = re.sub(r'<li class="agenda-item">.*?</li>', add_viking, html, flags=re.DOTALL)

# 3. Mark past events
past_events = ['AC/DC', 'Dream Theater', 'Jinjer']

def mark_past(match):
    full_str = match.group(0)
    for event in past_events:
        if f'<h3>{event}</h3>' in full_str:
            # Change Tickets button
            new_str = re.sub(r'<a href="#" class="btn-secondary">Tickets</a>', 
                             r'<a href="#" class="btn-secondary" style="pointer-events: none; opacity: 0.5; background: #333; color: #888; border-color: #444;">Finalizado</a>', 
                             full_str)
            # Add a FINALIZADO text right before agenda-date
            new_str = new_str.replace('<div class="agenda-date">', '<span style="color: #888; font-size: 0.8rem; font-weight: bold; margin-bottom: 5px; text-transform: uppercase;">Evento Pasado</span>\n                        <div class="agenda-date">')
            return new_str
    return full_str

html = re.sub(r'<li class="agenda-item">.*?</li>', mark_past, html, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(html)

# 4. Add the CSS class to index.css
with open('index.css', 'r') as f:
    css = f.read()

viking_css = """
.agenda-viking-badge {
    position: absolute;
    top: 15px;
    right: 15px;
    width: 45px;
    height: 45px;
    border-radius: 50%;
    border: 2px solid var(--accent-color);
    box-shadow: 0 0 15px rgba(165, 155, 93, 0.4);
    z-index: 5;
    object-fit: cover;
}
.agenda-item {
    position: relative;
}
"""

if '.agenda-viking-badge' not in css:
    css = css.replace('.agenda-item {', viking_css + '\n.agenda-item {')
    with open('index.css', 'w') as f:
        f.write(css)
