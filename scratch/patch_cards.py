import re

with open('app.py', 'r') as f:
    content = f.read()

# We'll use regex to match each card generator block and replace them with compact versions.

# Noticiero
old_noticiero_regex = re.compile(r'noticiero_cards = "".join\(\[f"""\n    <table.*?Leer Nota Completa.*?</table>\n    """ for n in noticiero\]\)', re.DOTALL)
new_noticiero = '''noticiero_cards = "".join([f"""
    <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#0d0d0d" class="darkmode-inner" style="background-color: #0d0d0d !important; border: 1px solid #716d4a; border-radius: 6px; overflow: hidden; margin-bottom: 10px;">
        <tr>
            <td width="110" valign="top" bgcolor="#0d0d0d" style="background-color: #0d0d0d !important; padding: 0;">
                <img src="{get_full_img_url(n['image_filename'], band_title=n['title'], sec='El Noticiero Nocturno')}" alt="{n['title']}" style="width: 110px; height: 110px; object-fit: cover; display: block; border-right: 1px solid #716d4a;" />
            </td>
            <td valign="top" bgcolor="#0d0d0d" style="background-color: #0d0d0d !important; padding: 10px 12px; color: #ffffff !important;">
                <div style="margin-bottom: 4px;">
                    <span style="background-color: #716d4a !important; color: #ffffff !important; font-weight: bold; font-size: 9px; padding: 2px 5px; border-radius: 2px; text-transform: uppercase;">Noticia</span>
                    <span style="color: #ffffff !important; font-size: 10px; margin-left: 6px;">📅 {n['created_at'][:10] if n['created_at'] else ''}</span>
                </div>
                <h3 style="color: #716d4a !important; margin: 0 0 4px 0; font-size: 14px; line-height: 1.2; font-weight: bold;">{n['title']}</h3>
                <p style="color: #ffffff !important; font-size: 11px; line-height: 1.3; margin: 0 0 6px 0;">{(n['short_desc'] or n['full_desc'] or '')[:90]}...</p>
                <a href="https://gothprods.com" target="_blank" style="color: #716d4a !important; font-size: 11px; font-weight: bold; text-decoration: underline;">Leer Nota &rarr;</a>
            </td>
        </tr>
    </table>
    """ for n in noticiero])'''

# Reseñas
old_resenas_regex = re.compile(r'reseñas_cards = "".join\(\[f"""\n    <table.*?Leer Reseña Completa.*?</table>\n    """ for r in reseñas\]\)', re.DOTALL)
new_resenas = '''reseñas_cards = "".join([f"""
    <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#0d0d0d" class="darkmode-inner" style="background-color: #0d0d0d !important; border: 1px solid #716d4a; border-radius: 6px; overflow: hidden; margin-bottom: 10px;">
        <tr>
            <td width="110" valign="top" bgcolor="#0d0d0d" style="background-color: #0d0d0d !important; padding: 0;">
                <img src="{get_full_img_url(r['image_filename'], band_title=r['title'], sec='Reseñas de Conciertos')}" alt="{r['title']}" style="width: 110px; height: 110px; object-fit: cover; display: block; border-right: 1px solid #716d4a;" />
            </td>
            <td valign="top" bgcolor="#0d0d0d" style="background-color: #0d0d0d !important; padding: 10px 12px; color: #ffffff !important;">
                <div style="margin-bottom: 4px;">
                    <span style="background-color: #716d4a !important; color: #ffffff !important; font-weight: bold; font-size: 9px; padding: 2px 5px; border-radius: 2px; text-transform: uppercase;">Reseña</span>
                    <span style="color: #ffffff !important; font-size: 10px; margin-left: 6px;">📅 {r['created_at'][:10] if r['created_at'] else ''}</span>
                </div>
                <h3 style="color: #716d4a !important; margin: 0 0 4px 0; font-size: 14px; line-height: 1.2; font-weight: bold;">{r['title']}</h3>
                <p style="color: #ffffff !important; font-size: 11px; line-height: 1.3; margin: 0 0 6px 0;">{(r['short_desc'] or r['full_desc'] or '')[:90]}...</p>
                <a href="https://gothprods.com" target="_blank" style="color: #716d4a !important; font-size: 11px; font-weight: bold; text-decoration: underline;">Leer Reseña &rarr;</a>
            </td>
        </tr>
    </table>
    """ for r in reseñas])'''

# Entrevistas
old_entrevistas_regex = re.compile(r'entrevistas_cards = "".join\(\[f"""\n    <table.*?Ver Entrevista en GothProds.*?</table>\n    """ for e in entrevistas\]\)', re.DOTALL)
new_entrevistas = '''entrevistas_cards = "".join([f"""
    <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#0d0d0d" class="darkmode-inner" style="background-color: #0d0d0d !important; border: 1px solid #716d4a; border-radius: 6px; overflow: hidden; margin-bottom: 10px;">
        <tr>
            <td width="110" valign="top" bgcolor="#0d0d0d" style="background-color: #0d0d0d !important; padding: 0;">
                <img src="{get_full_img_url(e['image_filename'], band_title=e['title'], sec='Entrevistas Under')}" alt="{e['title']}" style="width: 110px; height: 110px; object-fit: cover; display: block; border-right: 1px solid #716d4a;" />
            </td>
            <td valign="top" bgcolor="#0d0d0d" style="background-color: #0d0d0d !important; padding: 10px 12px; color: #ffffff !important;">
                <div style="margin-bottom: 4px;">
                    <span style="background-color: #716d4a !important; color: #ffffff !important; font-weight: bold; font-size: 9px; padding: 2px 5px; border-radius: 2px; text-transform: uppercase;">Entrevista</span>
                    <span style="color: #ffffff !important; font-size: 10px; margin-left: 6px;">📅 {e['created_at'][:10] if e['created_at'] else ''}</span>
                </div>
                <h3 style="color: #716d4a !important; margin: 0 0 4px 0; font-size: 14px; line-height: 1.2; font-weight: bold;">{e['title']}</h3>
                <p style="color: #ffffff !important; font-size: 11px; line-height: 1.3; margin: 0 0 6px 0;">{(e['short_desc'] or e['full_desc'] or '')[:90]}...</p>
                <a href="https://gothprods.com" target="_blank" style="color: #716d4a !important; font-size: 11px; font-weight: bold; text-decoration: underline;">Ver Entrevista &rarr;</a>
            </td>
        </tr>
    </table>
    """ for e in entrevistas])'''

# Galeria
old_galeria_regex = re.compile(r'galeria_cards = "".join\(\[f"""\n    <table.*?Reproducir Episodio.*?</table>\n    """ for g in galeria\]\)', re.DOTALL)
new_galeria = '''galeria_cards = "".join([f"""
    <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#0d0d0d" class="darkmode-inner" style="background-color: #0d0d0d !important; border: 1px solid #716d4a; border-radius: 6px; overflow: hidden; margin-bottom: 10px;">
        <tr>
            <td width="110" valign="top" bgcolor="#0d0d0d" style="background-color: #0d0d0d !important; padding: 0;">
                <img src="{get_full_img_url(g['image_filename'], band_title=g['title'], sec='La Galería Nocturna')}" alt="{g['title']}" style="width: 110px; height: 110px; object-fit: cover; display: block; border-right: 1px solid #716d4a;" />
            </td>
            <td valign="top" bgcolor="#0d0d0d" style="background-color: #0d0d0d !important; padding: 10px 12px; color: #ffffff !important;">
                <div style="margin-bottom: 4px;">
                    <span style="background-color: #716d4a !important; color: #ffffff !important; font-weight: bold; font-size: 9px; padding: 2px 5px; border-radius: 2px; text-transform: uppercase;">Podcast</span>
                    <span style="color: #ffffff !important; font-size: 10px; margin-left: 6px;">📅 {g['created_at'][:10] if g['created_at'] else ''}</span>
                </div>
                <h3 style="color: #716d4a !important; margin: 0 0 4px 0; font-size: 14px; line-height: 1.2; font-weight: bold;">{g['title']}</h3>
                <p style="color: #ffffff !important; font-size: 11px; line-height: 1.3; margin: 0 0 6px 0;">{(g['short_desc'] or g['full_desc'] or '')[:90]}...</p>
                <a href="https://gothprods.com" target="_blank" style="color: #716d4a !important; font-size: 11px; font-weight: bold; text-decoration: underline;">Reproducir &rarr;</a>
            </td>
        </tr>
    </table>
    """ for g in galeria])'''


# Bandas y Eventos (Radar del Caos)
old_bandas_regex = re.compile(r'b_html = "".join\(\[f"""\n        <table.*?</p>\n                </td>\n            </tr>\n        </table>\n        """ for b in bandas\]\)', re.DOTALL)
new_bandas = '''b_html = "".join([f"""
        <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#0d0d0d" class="darkmode-inner" style="background-color: #0d0d0d !important; border: 1px solid #716d4a; border-radius: 6px; overflow: hidden; margin-bottom: 10px;">
            <tr>
                <td width="110" valign="top" bgcolor="#0d0d0d" style="background-color: #0d0d0d !important; padding: 0;">
                    <img src="{get_full_img_url(b['img_video_path'] or b['ultimo_lanzamiento_url'])}" style="width: 110px; height: 100px; object-fit: cover; display: block; border-right: 1px solid #716d4a;" />
                </td>
                <td valign="top" bgcolor="#0d0d0d" style="background-color: #0d0d0d !important; padding: 10px 12px; color: #ffffff !important;">
                    <span style="background-color: #716d4a !important; color: #ffffff !important; font-weight: bold; font-size: 9px; padding: 2px 5px; border-radius: 2px; text-transform: uppercase; display: inline-block;">Banda Destacada</span>
                    <h3 style="color: #716d4a !important; margin: 4px 0; font-size: 14px; font-weight: bold;">{b['nombre']} ({b['pais'] or 'Underground'})</h3>
                    <p style="color: #ffffff !important; font-size: 11px; margin: 0; line-height: 1.3;">{(b['texto_resena'] or b['bio_larga'] or '')[:90]}...</p>
                </td>
            </tr>
        </table>
        """ for b in bandas])'''

old_eventos_regex = re.compile(r'e_html = "".join\(\[f"""\n        <table.*?</p>\n                </td>\n            </tr>\n        </table>\n        """ for e in eventos\]\)', re.DOTALL)
new_eventos = '''e_html = "".join([f"""
        <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#0d0d0d" class="darkmode-inner" style="background-color: #0d0d0d !important; border: 1px solid #716d4a; border-radius: 6px; overflow: hidden; margin-bottom: 10px;">
            <tr>
                <td width="110" valign="top" bgcolor="#0d0d0d" style="background-color: #0d0d0d !important; padding: 0;">
                    <img src="{get_full_img_url(e['img_video_path'])}" style="width: 110px; height: 100px; object-fit: cover; display: block; border-right: 1px solid #716d4a;" />
                </td>
                <td valign="top" bgcolor="#0d0d0d" style="background-color: #0d0d0d !important; padding: 10px 12px; color: #ffffff !important;">
                    <span style="background-color: #716d4a !important; color: #ffffff !important; font-weight: bold; font-size: 9px; padding: 2px 5px; border-radius: 2px; text-transform: uppercase; display: inline-block;">Evento Destacado</span>
                    <h3 style="color: #716d4a !important; margin: 4px 0; font-size: 14px; font-weight: bold;">{e['nombre_evento']}</h3>
                    <p style="color: #ffffff !important; font-size: 11px; margin: 0; line-height: 1.3;">📍 {e['ciudad']}, {e['pais']} <br/> 📅 {e['fecha_evento']}</p>
                </td>
            </tr>
        </table>
        """ for e in eventos])'''

content, n1 = old_noticiero_regex.subn(new_noticiero, content)
content, n2 = old_resenas_regex.subn(new_resenas, content)
content, n3 = old_entrevistas_regex.subn(new_entrevistas, content)
content, n4 = old_galeria_regex.subn(new_galeria, content)
content, n5 = old_bandas_regex.subn(new_bandas, content)
content, n6 = old_eventos_regex.subn(new_eventos, content)

print(f"Replacements: {n1}, {n2}, {n3}, {n4}, {n5}, {n6}")

with open('app.py', 'w') as f:
    f.write(content)

