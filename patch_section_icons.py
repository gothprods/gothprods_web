import re

# 1. Add CSS class
with open("index.css", "a") as f:
    f.write("\n.section-medal {\n    width: 65px;\n    height: 65px;\n    object-fit: contain;\n    background: #000;\n    border: 2px solid rgba(113, 109, 74, 0.6);\n    filter: drop-shadow(0 0 6px rgba(113, 109, 74, 0.8));\n    border-radius: 50%;\n    flex-shrink: 0;\n}\n")

# 2. Patch index.html
with open("templates/index.html", "r") as f:
    content = f.read()

def replacer(match):
    # match.group(1) is the inner h2
    return f"""<div class="header-titles" style="display: flex; align-items: center; gap: 15px; justify-content: center;">
                    {{% set icon_path = settings.get('{icon_key}', '{default_icon}') %}}
                    <img loading="lazy" src="{{{{ icon_path if icon_path.startswith('http') or icon_path.startswith('assets') else 'updates/' + icon_path }}}}" class="section-medal">
                    <div class="header-text-group" style="text-align: left; margin: 0;">
                        {match.group(1)}
                    </div>
                </div>"""

# Bandas y Eventos Destacados (Bandas de la Semana section)
# Currently: <div class="section-header">\n <h2 style="font-size: 2.2rem;">Bandas de la <span>Semana</span></h2>
icon_key = 'icon_destacados'
default_icon = 'assets/destacados_icon.png'
content = re.sub(r'<div class="section-header">\s*(<h2 style="font-size: 2\.2rem;">Bandas de la <span>Semana</span></h2>)', replacer, content, 1)

# El Pit
icon_key = 'icon_el_pit'
default_icon = 'assets/el_pit_icon.png'
content = re.sub(r'<div class="section-header">\s*(<h2>El <span>Pit</span></h2>)', replacer, content, 1)

# Reseñas de Conciertos
icon_key = 'icon_reviews'
default_icon = 'assets/resenas_icon.png'
content = re.sub(r'<div class="section-header">\s*(<h2>Reseñas de <span>Conciertos</span></h2>)', replacer, content, 1)

# El Noticiero Nocturno
icon_key = 'icon_news'
default_icon = 'assets/noticiero_icon.png'
content = re.sub(r'<div class="section-header">\s*(<h2>El Noticiero <span>Nocturno</span></h2>)', replacer, content, 1)

# Entrevistas Under
icon_key = 'icon_interviews'
default_icon = 'assets/entrevistas_icon.png'
content = re.sub(r'<div class="section-header" style="justify-content: flex-start; align-items: flex-end; gap: 20px;">\s*(<h2>Entrevistas <span>Under</span></h2>)', 
f"""<div class="section-header" style="justify-content: flex-start; align-items: flex-end; gap: 20px;">
                <div class="header-titles" style="display: flex; align-items: center; gap: 15px; justify-content: center;">
                    {{% set icon_path = settings.get('{icon_key}', '{default_icon}') %}}
                    <img loading="lazy" src="{{{{ icon_path if icon_path.startswith('http') or icon_path.startswith('assets') else 'updates/' + icon_path }}}}" class="section-medal">
                    <div class="header-text-group" style="text-align: left; margin: 0;">
                        \\1
                    </div>
                </div>""", content, 1)

# Agenda Metalera
icon_key = 'icon_agenda'
default_icon = 'assets/agenda_icon.png'
content = re.sub(r'<div class="section-header">\s*(<h2>Agenda <span>Metalera 2026</span></h2>)', replacer, content, 1)

# La Galeria Nocturna
# Currently: <img loading="lazy" src="{{ settings.get('galeria_bg', 'assets/galeria-logo-new.webp') }}" alt="La Galería Nocturna Logo" class="section-logo">
content = re.sub(r'<img loading="lazy" src="\{\{ settings\.get\(\'galeria_bg\', \'assets/galeria-logo-new\.webp\'\) \}\}" alt="La Galería Nocturna Logo" class="section-logo">',
"""{% set icon_path = settings.get('icon_galeria', 'assets/galeria_nocturna_icon.jpg') %}
                        <img loading="lazy" src="{{ icon_path if icon_path.startswith('http') or icon_path.startswith('assets') else 'updates/' + icon_path }}" alt="La Galería Nocturna Logo" class="section-medal">""", content)

# Metal Pulse
content = re.sub(r'<img loading="lazy" src="\{\{ settings\.get\(\'metalpulse_bg\', \'assets/metal-pulse-logo\.webp\'\) \}\}" alt="Metal Pulse Logo" class="section-logo">',
"""{% set icon_path = settings.get('icon_metalpulse', 'assets/metal_pulse_icon.jpg') %}
                    <img loading="lazy" src="{{ icon_path if icon_path.startswith('http') or icon_path.startswith('assets') else 'updates/' + icon_path }}" alt="Metal Pulse Logo" class="section-medal">""", content)

# Eventos Destacados
# Bandas y Eventos Destacados shares icon.
icon_key = 'icon_destacados'
default_icon = 'assets/destacados_icon.png'
content = re.sub(r'<div class="section-header">\s*(<h2 style="font-size: 2\.2rem;">Eventos <span>Destacados</span></h2>)', replacer, content, 1)

with open("templates/index.html", "w") as f:
    f.write(content)

print("Patch applied.")
