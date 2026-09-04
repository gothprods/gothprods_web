import re

with open('templates/admin_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Hide Galeria
content = re.sub(
    r'<div style="background: #1a1a1a; padding: 15px; border-radius: 8px; border: 1px solid #333; margin-bottom: 15px;">\s*<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">\s*<label style="display: flex; align-items: center; gap: 10px; cursor: pointer; font-weight: bold; margin: 0; color: var\(--accent-color\);">\s*<label class="switch" style="margin: 0;">\s*<input type="checkbox" name="show_galeria_nocturna".*?</label>\s*La Galería Nocturna\s*</label>\s*</div>\s*<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">.*?</div>\s*</div>',
    '<input type="hidden" name="show_galeria_nocturna" value="1">',
    content, flags=re.DOTALL
)

# 2. Hide Metal Pulse
content = re.sub(
    r'<div style="background: #1a1a1a; padding: 15px; border-radius: 8px; border: 1px solid #333; margin-bottom: 15px;">\s*<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">\s*<label style="display: flex; align-items: center; gap: 10px; cursor: pointer; font-weight: bold; margin: 0; color: var\(--accent-color\);">\s*<label class="switch" style="margin: 0;">\s*<input type="checkbox" name="show_metalpulse".*?</label>\s*Metal Pulse\s*</label>\s*</div>\s*<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">.*?</div>\s*</div>',
    '<input type="hidden" name="show_metalpulse" value="1">',
    content, flags=re.DOTALL
)

# 3. Hide Reviews
content = re.sub(
    r'<div style="background: #1a1a1a; padding: 15px; border-radius: 8px; border: 1px solid #333; margin-bottom: 15px;">\s*<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">\s*<label style="display: flex; align-items: center; gap: 10px; cursor: pointer; font-weight: bold; margin: 0; color: var\(--accent-color\);">\s*<label class="switch" style="margin: 0;">\s*<input type="checkbox" name="show_reviews".*?</label>\s*Reseñas de Conciertos\s*</label>\s*</div>\s*<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">.*?</div>\s*</div>',
    '<input type="hidden" name="show_reviews" value="1">',
    content, flags=re.DOTALL
)

# 4. Hide Interviews
content = re.sub(
    r'<div style="background: #1a1a1a; padding: 15px; border-radius: 8px; border: 1px solid #333; margin-bottom: 15px;">\s*<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">\s*<label style="display: flex; align-items: center; gap: 10px; cursor: pointer; font-weight: bold; margin: 0; color: var\(--accent-color\);">\s*<label class="switch" style="margin: 0;">\s*<input type="checkbox" name="show_interviews".*?</label>\s*Entrevistas Under\s*</label>\s*</div>\s*<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">.*?</div>\s*</div>',
    '<input type="hidden" name="show_interviews" value="1">',
    content, flags=re.DOTALL
)

# 5. Insert Nuestros Podcasts, Conciertos and Servicios at the appropriate places.
# Insert Podcasts and Conciertos above "El Noticiero Nocturno"
podcasts_conciertos = """
<div style="background: #1a1a1a; padding: 15px; border-radius: 8px; border: 1px solid #333; margin-bottom: 15px;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
        <label style="display: flex; align-items: center; gap: 10px; cursor: pointer; font-weight: bold; margin: 0; color: var(--accent-color);">
            Nuestros Podcasts <span style="font-size: 0.75rem; color: #888;">(Menú)</span>
        </label>
    </div>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
        <div><label style="font-size: 0.8rem; color: #aaa;">Título en el Menú</label><input type="text" name="title_podcasts" value="{{ settings.get('title_podcasts', 'Nuestros Podcasts') }}" style="background: #222; padding: 8px; border-radius: 4px; border: 1px solid #444; width: 100%; color: #fff;"></div>
        <div><label style="font-size: 0.8rem; color: #aaa;">Ícono (Imagen)</label><input type="file" name="icon_podcasts" accept="image/*" style="background: #222; padding: 6px; border-radius: 4px; border: 1px solid #444; width: 100%; color: #fff; font-size: 0.8rem;"></div>
    </div>
</div>

<div style="background: #1a1a1a; padding: 15px; border-radius: 8px; border: 1px solid #333; margin-bottom: 15px;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
        <label style="display: flex; align-items: center; gap: 10px; cursor: pointer; font-weight: bold; margin: 0; color: var(--accent-color);">
            Conciertos <span style="font-size: 0.75rem; color: #888;">(Menú)</span>
        </label>
    </div>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
        <div><label style="font-size: 0.8rem; color: #aaa;">Título en el Menú</label><input type="text" name="title_conciertos" value="{{ settings.get('title_conciertos', 'Conciertos') }}" style="background: #222; padding: 8px; border-radius: 4px; border: 1px solid #444; width: 100%; color: #fff;"></div>
        <div><label style="font-size: 0.8rem; color: #aaa;">Ícono (Imagen)</label><input type="file" name="icon_conciertos" accept="image/*" style="background: #222; padding: 6px; border-radius: 4px; border: 1px solid #444; width: 100%; color: #fff; font-size: 0.8rem;"></div>
    </div>
</div>
"""

content = content.replace('El Noticiero Nocturno\n        </label>', 'El Noticiero Nocturno\n        </label>')
# Actually, let's insert it right before El Noticiero Nocturno div
news_div = '<div style="background: #1a1a1a; padding: 15px; border-radius: 8px; border: 1px solid #333; margin-bottom: 15px;">\n    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">\n        <label style="display: flex; align-items: center; gap: 10px; cursor: pointer; font-weight: bold; margin: 0; color: var(--accent-color);">\n            <label class="switch" style="margin: 0;">\n                <input type="checkbox" name="show_news"'

content = content.replace(news_div, podcasts_conciertos + news_div)

# 6. Insert Servicios before Contáctanos
servicios_div = """
<div style="background: #1a1a1a; padding: 15px; border-radius: 8px; border: 1px solid #333; margin-bottom: 15px;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
        <label style="display: flex; align-items: center; gap: 10px; cursor: pointer; font-weight: bold; margin: 0; color: var(--accent-color);">
            <label class="switch" style="margin: 0;">
                <input type="checkbox" name="show_servicios" value="1" {% if settings.get('show_servicios', '1') == '1' %}checked{% endif %}>
                <span class="slider"></span>
            </label>
            Servicios
        </label>
    </div>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
        <div><label style="font-size: 0.8rem; color: #aaa;">Título en el Menú</label><input type="text" name="title_servicios" value="{{ settings.get('title_servicios', 'Servicios') }}" style="background: #222; padding: 8px; border-radius: 4px; border: 1px solid #444; width: 100%; color: #fff;"></div>
        <div><label style="font-size: 0.8rem; color: #aaa;">Ícono (Imagen)</label><input type="file" name="icon_servicios" accept="image/*" style="background: #222; padding: 6px; border-radius: 4px; border: 1px solid #444; width: 100%; color: #fff; font-size: 0.8rem;"></div>
    </div>
</div>
"""

contacto_div = '<div style="background: #1a1a1a; padding: 15px; border-radius: 8px; border: 1px solid #333; margin-bottom: 15px;">\n    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">\n        <label style="display: flex; align-items: center; gap: 10px; cursor: pointer; font-weight: bold; margin: 0; color: var(--accent-color);">\n            <label class="switch" style="margin: 0;">\n                <input type="checkbox" name="show_contactanos"'

content = content.replace(contacto_div, servicios_div + contacto_div)

# 7. Modificar Agenda para esconder los campos de "Título de Menú" y "Ícono" que ya no se usarán para el menú principal.
content = re.sub(
    r'<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">\s*<div>\s*<label style="font-size: 0.8rem; color: #aaa;">Título en el Menú</label>\s*<input type="text" name="title_agenda".*?</div>\s*<div>\s*<label style="font-size: 0.8rem; color: #aaa;">Ícono \(Imagen\)</label>\s*<input type="file" name="icon_agenda".*?</div>\s*</div>\s*</div>\s*<div style="background: #1a1a1a; padding: 15px; border-radius: 8px; border: 1px solid #333; margin-bottom: 15px;">',
    '<input type="hidden" name="show_agenda" value="1">\n</div>\n<div style="background: #1a1a1a; padding: 15px; border-radius: 8px; border: 1px solid #333; margin-bottom: 15px;">',
    content, flags=re.DOTALL
)

with open('templates/admin_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("done")
