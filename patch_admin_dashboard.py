import re

html_template = """<div style="background: #1a1a1a; padding: 15px; border-radius: 8px; border: 1px solid #333; margin-bottom: 15px;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
        <label style="display: flex; align-items: center; gap: 10px; cursor: pointer; font-weight: bold; margin: 0; color: var(--accent-color);">
            <label class="switch" style="margin: 0;">
                <input type="checkbox" name="{switch_name}" value="1" {{% if settings.get('{switch_name}', '1') == '1' %}}checked{{% endif %}}>
                <span class="slider"></span>
            </label>
            {default_title}
        </label>
    </div>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
        <div>
            <label style="font-size: 0.8rem; color: #aaa;">Título en el Menú</label>
            <input type="text" name="{title_name}" value="{{{{ settings.get('{title_name}', '{default_title}') }}}}" style="background: #222; padding: 8px; border-radius: 4px; border: 1px solid #444; width: 100%; color: #fff;">
        </div>
        <div>
            <label style="font-size: 0.8rem; color: #aaa;">Ícono (Imagen)</label>
            <input type="file" name="{icon_name}" accept="image/*" style="background: #222; padding: 6px; border-radius: 4px; border: 1px solid #444; width: 100%; color: #fff; font-size: 0.8rem;">
        </div>
    </div>
</div>"""

items = [
    ("show_banda_semana", "title_destacados", "icon_destacados", "Bandas y Eventos Destacados"),
    ("show_el_pit", "title_el_pit", "icon_el_pit", "El Pit"),
    ("show_galeria_nocturna", "title_galeria", "icon_galeria", "La Galería Nocturna"),
    ("show_metalpulse", "title_metalpulse", "icon_metalpulse", "Metal Pulse"),
    ("show_reviews", "title_reviews", "icon_reviews", "Reseñas de Conciertos"),
    ("show_news", "title_news", "icon_news", "El Noticiero Nocturno"),
    ("show_interviews", "title_interviews", "icon_interviews", "Entrevistas Under"),
    ("show_agenda", "title_agenda", "icon_agenda", "Agenda Metalera"),
    ("show_contactanos", "title_contacto", "icon_contacto", "Contáctanos")
]

new_html = '<h4 style="color: var(--accent-color); margin-top: 30px; margin-bottom: 15px; border-bottom: 1px solid #333; padding-bottom: 5px;"><i class="fa-solid fa-bars-staggered"></i> Configuración del Menú Flotante</h4>\n'
new_html += '<div style="display: flex; flex-direction: column; gap: 10px;">\n'
for item in items:
    new_html += html_template.format(switch_name=item[0], title_name=item[1], icon_name=item[2], default_title=item[3]) + "\n"
new_html += '</div>\n'

with open("templates/admin_dashboard.html", "r") as f:
    content = f.read()

# Remove hamburger icon field
content = re.sub(r'<label>Ícono de Menú Hamburguesa.*?<input type="file" name="hamburger_icon".*?>\s*', '', content, flags=re.DOTALL)

# Replace the modules section
modules_start = r'<h4 style="color: var\(--accent-color\); margin-top: 30px; margin-bottom: 15px; border-bottom: 1px solid #333; padding-bottom: 5px;"><i class="fa-solid fa-layer-group"></i> Módulos y Secciones</h4>'
modules_end = r'</label>\s*</div>\s*<button type="submit"'

# We use sub to replace everything between modules_start and modules_end (exclusive of button)
pattern = re.compile(f'({modules_start}.*?</label>\\s*</div>)(\\s*<button type="submit")', re.DOTALL)

content = pattern.sub(new_html.replace('\\', '\\\\') + r'\2', content)

with open("templates/admin_dashboard.html", "w") as f:
    f.write(content)

print("HTML patched.")
