import re

with open('templates/admin_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

def hide_card(title_marker, content_str):
    # This regex finds the 1a1a1a div that contains the title_marker
    pattern = re.compile(
        r'(<div style="background: #1a1a1a; padding: 15px; border-radius: 8px; border: 1px solid #333; margin-bottom: 15px;">)([\s\S]{0,400}?' + re.escape(title_marker) + r')'
    )
    return pattern.sub(r'<div style="display: none; background: #1a1a1a; padding: 15px; border-radius: 8px; border: 1px solid #333; margin-bottom: 15px;">\2', content_str)

# 1. Hide unwanted cards entirely
content = hide_card('La Galería Nocturna\n        </label>', content)
content = hide_card('Metal Pulse\n        </label>', content)
content = hide_card('Reseñas de Conciertos\n        </label>', content)
content = hide_card('Entrevistas Under\n        </label>', content)

# 2. Hide only the title/icon fields of Agenda, but keep the poster part
# Agenda card is massive. The title/icon fields are in a grid at the end.
agenda_fields = """    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
        <div>
            <label style="font-size: 0.8rem; color: #aaa;">Título en el Menú</label>
            <input type="text" name="title_agenda" value="{{ settings.get('title_agenda', 'Agenda Metalera') }}" style="background: #222; padding: 8px; border-radius: 4px; border: 1px solid #444; width: 100%; color: #fff;">
        </div>
        <div>
            <label style="font-size: 0.8rem; color: #aaa;">Ícono (Imagen)</label>
            <input type="file" name="icon_agenda" accept="image/*" style="background: #222; padding: 6px; border-radius: 4px; border: 1px solid #444; width: 100%; color: #fff; font-size: 0.8rem;">
        </div>
    </div>"""

if agenda_fields in content:
    content = content.replace(agenda_fields, '<div style="display: none;">\n' + agenda_fields + '\n</div>')

# 3. Insert the 3 new cards (Podcasts, Conciertos, Servicios)
podcasts_html = """
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
"""

conciertos_html = """
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

servicios_html = """
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

# Podcats goes before El Noticiero
news_marker = '<div style="background: #1a1a1a; padding: 15px; border-radius: 8px; border: 1px solid #333; margin-bottom: 15px;">\n    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">\n        <label style="display: flex; align-items: center; gap: 10px; cursor: pointer; font-weight: bold; margin: 0; color: var(--accent-color);">\n            <label class="switch" style="margin: 0;">\n                <input type="checkbox" name="show_news"'
content = content.replace(news_marker, podcasts_html + '\n' + news_marker)

# Conciertos goes after El Noticiero, which means before Agenda
agenda_marker = '<div style="background: #1a1a1a; padding: 15px; border-radius: 8px; border: 1px solid #333; margin-bottom: 15px;">\n    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">\n        <label style="display: flex; align-items: center; gap: 10px; cursor: pointer; font-weight: bold; margin: 0; color: var(--accent-color);">\n            <label class="switch" style="margin: 0;">\n                <input type="checkbox" name="show_agenda"'
content = content.replace(agenda_marker, conciertos_html + '\n' + agenda_marker)

# Servicios goes before Contactanos
contacto_marker = '<div style="background: #1a1a1a; padding: 15px; border-radius: 8px; border: 1px solid #333; margin-bottom: 15px;">\n    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">\n        <label style="display: flex; align-items: center; gap: 10px; cursor: pointer; font-weight: bold; margin: 0; color: var(--accent-color);">\n            <label class="switch" style="margin: 0;">\n                <input type="checkbox" name="show_contactanos"'
content = content.replace(contacto_marker, servicios_html + '\n' + contacto_marker)

with open('templates/admin_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Safe patch applied")
