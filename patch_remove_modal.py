import re

# 1. Update index.html
with open("templates/index.html", "r") as f:
    content = f.read()

# Replace the button with social buttons
old_btn = """                                        <p style="font-size: 0.95rem; line-height: 1.4; margin-bottom: 15px; color: #ccc; white-space: pre-line;">{{ evento.bio_corta|truncate(1200) }}</p>
                                        <button onclick="openEventoModal({{ evento.id }})" style="background: transparent; color: var(--accent-color); border: 1px solid var(--accent-color); padding: 5px 12px; font-size: 0.85rem; border-radius: 4px; cursor: pointer; text-transform: uppercase; font-family: 'Oswald', sans-serif; letter-spacing: 1px; transition: all 0.3s;"><i class="fa-solid fa-book-open"></i> Leer más del evento</button>"""

new_btns = """                                        <p style="font-size: 0.95rem; line-height: 1.4; margin-bottom: 15px; color: #ccc; white-space: pre-line;">{{ evento.bio_corta|truncate(1200) }}</p>
                                        <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-top: 15px;">
                                            {% if evento.fb_link %}<a href="{{ evento.fb_link }}" target="_blank" class="platform-btn" style="background: transparent; padding: 5px 12px; font-size: 0.85rem; border-radius: 4px; color: var(--accent-color); text-decoration: none; border: 1px solid var(--accent-color); transition: all 0.3s;" onmouseover="this.style.background='var(--accent-color)'; this.style.color='#000';" onmouseout="this.style.background='transparent'; this.style.color='var(--accent-color)';"><i class="fa-brands fa-facebook-f"></i> {{ evento.promotor }}</a>{% endif %}
                                            {% if evento.ig_link %}<a href="{{ evento.ig_link }}" target="_blank" class="platform-btn" style="background: transparent; padding: 5px 12px; font-size: 0.85rem; border-radius: 4px; color: var(--accent-color); text-decoration: none; border: 1px solid var(--accent-color); transition: all 0.3s;" onmouseover="this.style.background='var(--accent-color)'; this.style.color='#000';" onmouseout="this.style.background='transparent'; this.style.color='var(--accent-color)';"><i class="fa-brands fa-instagram"></i> {{ evento.promotor }}</a>{% endif %}
                                        </div>"""
content = content.replace(old_btn, new_btns)

# Remove the Evento Modals block entirely
modal_pattern = re.compile(r'<!-- EVENTO MODALS -->.*?<!-- BANDA MODALS \(One for each band\) -->', re.DOTALL)
content = modal_pattern.sub('<!-- BANDA MODALS (One for each band) -->', content)

with open("templates/index.html", "w") as f:
    f.write(content)


# 2. Update admin_dashboard.html
with open("templates/admin_dashboard.html", "r") as f:
    admin_content = f.read()

old_admin_field = """            <label style="margin-top: 15px;">Sobre el Evento (Resumen - Máximo 1200 caracteres)</label>
            <textarea name="bio_corta" rows="6" maxlength="1200" placeholder="Escribe aquí toda la información necesaria para balancear el espacio con la Banda de la Semana..." required></textarea>

            <label style="margin-top: 15px;">Texto del Artículo</label>
            <textarea name="texto_articulo" rows="6" placeholder="Escribe aquí tu artículo completo sobre el evento..." required></textarea>"""

new_admin_field = """            <label style="margin-top: 15px;">Sobre el Evento (Máximo 1200 caracteres)</label>
            <textarea name="bio_corta" rows="6" maxlength="1200" placeholder="Escribe aquí toda la información necesaria para balancear el espacio con la Banda de la Semana..." required></textarea>"""

admin_content = admin_content.replace(old_admin_field, new_admin_field)

with open("templates/admin_dashboard.html", "w") as f:
    f.write(admin_content)

print("Modals and text field removed successfully")
