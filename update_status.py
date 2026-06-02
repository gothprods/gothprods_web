import re

with open('index.html', 'r') as f:
    html = f.read()

def update_status(match):
    full_str = match.group(0)
    
    # Process Cancelado
    if 'cancelado' in full_str.lower():
        # Add badge if not there
        if 'Evento Cancelado' not in full_str:
            full_str = full_str.replace('<div class="agenda-date">', '<span style="color: #faa; font-size: 0.8rem; font-weight: bold; margin-bottom: 5px; text-transform: uppercase; display: block;">Evento Cancelado</span>\n                        <div class="agenda-date">')
        
        # Update button
        full_str = re.sub(r'<a href="#" class="btn-secondary".*?</a>', 
                         r'<a href="#" class="btn-secondary" style="pointer-events: none; opacity: 0.6; background: #600; color: #faa; border-color: #800;">Cancelado</a>', 
                         full_str)
                         
    # Process Funado
    elif 'funado' in full_str.lower():
        # Add badge if not there
        if 'Banda Funada' not in full_str:
            full_str = full_str.replace('<div class="agenda-date">', '<span style="color: #d8a6d8; font-size: 0.8rem; font-weight: bold; margin-bottom: 5px; text-transform: uppercase; display: block;">Banda Funada</span>\n                        <div class="agenda-date">')
        
        # Update button
        full_str = re.sub(r'<a href="#" class="btn-secondary".*?</a>', 
                         r'<a href="#" class="btn-secondary" style="pointer-events: none; opacity: 0.6; background: #400040; color: #d8a6d8; border-color: #602060;">Funado</a>', 
                         full_str)
                         
    return full_str

html = re.sub(r'<li class="agenda-item">.*?</li>', update_status, html, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(html)
