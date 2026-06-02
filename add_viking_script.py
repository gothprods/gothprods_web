import re
import os

html_path = 'index.html'
with open(html_path, 'r') as f:
    html = f.read()

# 1. Update Highlights List
html = html.replace('<li><strong>May 22:</strong> Gojira y Knocked Loose</li>', '<li><strong>May 22:</strong> Metallica (Gojira y Knocked Loose)</li>')
html = html.replace('<li><strong>May 24:</strong> Pantera y Avatar</li>', '<li><strong>May 24:</strong> Metallica (Pantera y Avatar)</li>')

# 2. Add Havok to Julio
havok_html = """
                    <li class="agenda-item">
                        <img src="assets/viking.jpg" alt="Goth Prods Crew" class="agenda-viking-badge" title="El Crew de Goth Prods asistirá">
                        <img src="assets/logos/Havok.png"
                            onerror="this.style.display='none'; this.closest('.agenda-item').classList.add('no-logo');"
                            alt="Havok Logo" class="agenda-logo">
                        <div class="agenda-date"><span class="month">JUL</span><span class="day">03</span></div>
                        <div class="agenda-details">
                            <h3>Havok</h3>
                            <p>Foro Independencia | 3 de julio</p>
                        </div>
                        <a href="#" class="btn-secondary">Tickets</a>
                    </li>
"""
julio_section = """<div class="agenda-month">
                <h3>Julio</h3>
                <ul class="agenda-list">
                    <li class="agenda-item"
                        style="text-align: center; justify-content: center; color: var(--text-muted); font-style: italic;">
                        Pronto anunciaremos eventos para este mes.
                    </li>
                </ul>
            </div>"""
new_julio_section = f"""<div class="agenda-month">
                <h3>Julio</h3>
                <ul class="agenda-list">
{havok_html}
                </ul>
            </div>"""
html = html.replace(julio_section, new_julio_section)

# 3. Update May 22 and 24 Agenda Items
# We can find them using the dates
def replace_may_22(match):
    return match.group(0).replace('assets/logos/gojira.png', 'assets/logos/metallica.png') \
                         .replace('Gojira y Knocked Loose Logo', 'Metallica Logo') \
                         .replace('Gojira y Knocked Loose</h3>', 'Metallica</h3>') \
                         .replace('22 de mayo</p>', '22 de mayo<br><span style="color: var(--text-muted); font-size: 0.9em;">Teloneros: Gojira y Knocked Loose</span></p>')

html = re.sub(r'<li class="agenda-item">.*?<span class="month">MAY</span><span class="day">22</span>.*?</li>', replace_may_22, html, flags=re.DOTALL)

def replace_may_24(match):
    return match.group(0).replace('assets/logos/knockedloose.png', 'assets/logos/metallica.png') \
                         .replace('Pantera y Avatar Logo', 'Metallica Logo') \
                         .replace('Pantera y Avatar</h3>', 'Metallica</h3>') \
                         .replace('24 de mayo</p>', '24 de mayo<br><span style="color: var(--text-muted); font-size: 0.9em;">Teloneros: Pantera y Avatar</span></p>')

html = re.sub(r'<li class="agenda-item">.*?<span class="month">MAY</span><span class="day">24</span>.*?</li>', replace_may_24, html, flags=re.DOTALL)

# 4. Add Viking Badge to specific bands
viking_badge = '\n                        <img src="assets/viking.jpg" alt="Goth Prods Crew" class="agenda-viking-badge" title="El Crew de Goth Prods asistirá">'
bands_to_attend = ['Megadeth', 'Metallica', 'System Of A Down', 'Ladrones', 'Candelabrum', 'AfterShock', 'Iron Maiden', 'Opeth', 'Knotfest', 'Deep Purple']

def add_viking(match):
    item_html = match.group(0)
    # Check if already has viking badge
    if 'agenda-viking-badge' in item_html:
        return item_html
    
    # Check if it matches any of the target bands
    for band in bands_to_attend:
        if band in item_html: # We just check if the band name is in the html block (e.g. alt="Megadeth Logo" or h3)
            # Add viking badge right after <li class="agenda-item">
            return item_html.replace('<li class="agenda-item">', f'<li class="agenda-item">{viking_badge}', 1)
            
    return item_html

html = re.sub(r'<li class="agenda-item">.*?</li>', add_viking, html, flags=re.DOTALL)

with open(html_path, 'w') as f:
    f.write(html)

print("Agenda updated successfully.")
