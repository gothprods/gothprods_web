import re

with open('index.html', 'r') as f:
    html = f.read()

# Replace Evento Cancelado
old_cancelado_tag = r'<span style="color: #faa; font-size: 0.8rem; font-weight: bold; margin-bottom: 5px; text-transform: uppercase; display: block;">Evento Cancelado</span>\n\s*'
new_cancelado_tag = '<span style="position: absolute; top: -10px; left: 50%; transform: translateX(-50%); background: #600; color: #faa; padding: 4px 12px; border-radius: 6px; font-size: 0.8rem; font-weight: bold; text-transform: uppercase; z-index: 10; border: 1px solid #faa; white-space: nowrap;">Cancelado</span>\n                        '

# Replace Banda Funada
old_funada_tag = r'<span style="color: #d8a6d8; font-size: 0.8rem; font-weight: bold; margin-bottom: 5px; text-transform: uppercase; display: block;">Banda Funada</span>\n\s*'
new_funada_tag = '<span style="position: absolute; top: -10px; left: 50%; transform: translateX(-50%); background: #400040; color: #d8a6d8; padding: 4px 12px; border-radius: 6px; font-size: 0.8rem; font-weight: bold; text-transform: uppercase; z-index: 10; border: 1px solid #d8a6d8; white-space: nowrap;">Banda Funada</span>\n                        '

def fix_item(match):
    full_str = match.group(0)
    
    has_cancelado = re.search(old_cancelado_tag, full_str)
    has_funada = re.search(old_funada_tag, full_str)
    
    if has_cancelado:
        full_str = re.sub(old_cancelado_tag, '', full_str)
        # Add to the beginning of the li item content
        full_str = full_str.replace('<li class="agenda-item">', '<li class="agenda-item">\n                        ' + new_cancelado_tag)
        
    if has_funada:
        full_str = re.sub(old_funada_tag, '', full_str)
        full_str = full_str.replace('<li class="agenda-item">', '<li class="agenda-item">\n                        ' + new_funada_tag)
        
    return full_str

html = re.sub(r'<li class="agenda-item">.*?</li>', fix_item, html, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(html)
