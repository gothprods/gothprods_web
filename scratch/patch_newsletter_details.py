import re

with open('app.py', 'r') as f:
    content = f.read()

# 1. Update pulse_items to include Spotify link
old_pulse = '''                            <strong style="color: #716d4a !important; font-size: 14px; display: block;">{t['title']}</strong>
                            <span style="color: #ffffff !important; font-size: 12px;">{t['short_desc']}</span>'''
new_pulse = '''                            <strong style="color: #716d4a !important; font-size: 14px; display: block;">{t['title']}</strong>
                            <span style="color: #ffffff !important; font-size: 12px; display: block; margin-bottom: 2px;">{t['short_desc']}</span>
                            {f\'\'\'<a href="{t["sp_link"]}" target="_blank" style="color: #1DB954 !important; font-size: 11px; text-decoration: none; font-weight: bold;">Escuchar en Spotify &rarr;</a>\'\'\' if t.get("sp_link") else ""}'''
content = content.replace(old_pulse, new_pulse)

# 2. Update Bandas in Radar del Caos
old_bandas = '''                    <h3 style="color: #716d4a !important; margin: 4px 0; font-size: 14px; font-weight: bold;">{b['nombre']} ({b['pais'] or 'Underground'})</h3>
                    <p style="color: #ffffff !important; font-size: 11px; margin: 0; line-height: 1.3;">{(b['texto_resena'] or b['bio_larga'] or '')[:90]}...</p>'''
new_bandas = '''                    <h3 style="color: #716d4a !important; margin: 4px 0; font-size: 14px; font-weight: bold;">{b['nombre']} ({b['pais'] or 'Underground'})</h3>
                    {f\'\'\'<h4 style="font-size: 11px; color: #716d4a !important; margin: 0 0 4px 0; font-style: italic;">"{b["titulo_resena"]}"</h4>\'\'\' if b.get("titulo_resena") else ""}
                    <p style="color: #ffffff !important; font-size: 11px; margin: 0; line-height: 1.3;">{(b['texto_resena'] or b['bio_larga'] or '')[:90]}...</p>'''
content = content.replace(old_bandas, new_bandas)

# 3. Update Eventos in Radar del Caos
old_eventos = '''                    <h3 style="color: #716d4a !important; margin: 4px 0; font-size: 14px; font-weight: bold;">{e['nombre_evento']}</h3>
                    <p style="color: #ffffff !important; font-size: 11px; margin: 0; line-height: 1.3;">📍 {e['ciudad']}, {e['pais']} <br/> 📅 {e['fecha_evento']}</p>'''
new_eventos = '''                    <h3 style="color: #716d4a !important; margin: 4px 0; font-size: 14px; font-weight: bold;">{e['titulo_articulo'] if e.get('titulo_articulo') else e['nombre_evento']}</h3>
                    {f\'\'\'<p style="color: #716d4a !important; font-size: 11px; margin: 0 0 4px 0; font-weight: bold;">{e["nombre_evento"]}</p>\'\'\' if e.get("titulo_articulo") and e["titulo_articulo"] != e["nombre_evento"] else ""}
                    <p style="color: #ffffff !important; font-size: 11px; margin: 0; line-height: 1.3;">📍 {e['ciudad']}, {e['pais']} <br/> 📅 {e['fecha_evento']}</p>'''
content = content.replace(old_eventos, new_eventos)


with open('app.py', 'w') as f:
    f.write(content)
print("Done!")
