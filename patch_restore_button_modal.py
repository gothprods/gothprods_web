import re

with open("templates/index.html", "r") as f:
    content = f.read()

# 1. Restore the "Leer nota completa" button in the main card
old_btns = """                                        <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-top: 15px;">
                                            {% if evento.fb_link %}<a href="{{ evento.fb_link }}" target="_blank" class="platform-btn" style="background: transparent; padding: 5px 12px; font-size: 0.85rem; border-radius: 4px; color: var(--accent-color); text-decoration: none; border: 1px solid var(--accent-color); transition: all 0.3s;" onmouseover="this.style.background='var(--accent-color)'; this.style.color='#000';" onmouseout="this.style.background='transparent'; this.style.color='var(--accent-color)';"><i class="fa-brands fa-facebook-f"></i> {{ evento.promotor }}</a>{% endif %}
                                            {% if evento.ig_link %}<a href="{{ evento.ig_link }}" target="_blank" class="platform-btn" style="background: transparent; padding: 5px 12px; font-size: 0.85rem; border-radius: 4px; color: var(--accent-color); text-decoration: none; border: 1px solid var(--accent-color); transition: all 0.3s;" onmouseover="this.style.background='var(--accent-color)'; this.style.color='#000';" onmouseout="this.style.background='transparent'; this.style.color='var(--accent-color)';"><i class="fa-brands fa-instagram"></i> {{ evento.promotor }}</a>{% endif %}
                                        </div>"""

new_btn = """                                        <button onclick="openEventoModal({{ evento.id }})" style="background: transparent; color: var(--accent-color); border: 1px solid var(--accent-color); padding: 5px 12px; font-size: 0.85rem; border-radius: 4px; cursor: pointer; text-transform: uppercase; font-family: 'Oswald', sans-serif; letter-spacing: 1px; transition: all 0.3s;"><i class="fa-solid fa-book-open"></i> Leer nota completa</button>"""

content = content.replace(old_btns, new_btn)


# 2. Re-insert the Evento Modals block
evento_modals_html = """        <!-- EVENTO MODALS -->
        {% for evento in eventos_semana %}
        <div id="evento-modal-{{ evento.id }}" class="banda-modal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.9); z-index: 9999; justify-content: center; align-items: center; padding: 20px;">
            <div id="evento-modal-content-{{ evento.id }}" style="background: #111; max-width: 800px; width: 100%; max-height: 90vh; overflow-y: auto; border: 1px solid var(--accent-color); border-radius: 8px; position: relative;">
                <button onclick="closeEventoModal({{ evento.id }})" style="position: absolute; right: 20px; top: 20px; background: transparent; border: none; color: #fff; font-size: 2rem; cursor: pointer; z-index: 10;"><i class="fa-solid fa-times"></i></button>
                <div style="padding: 40px 30px;">
                    <h2 class="notranslate" style="color: var(--accent-color); font-size: 2.5rem; margin-bottom: 5px; text-align: center; font-family: 'Oswald', sans-serif; text-transform: uppercase;">{{ evento.titulo_articulo }}</h2>
                    <h3 style="text-align: center; color: #fff; font-size: 1.5rem; margin-bottom: 10px;">{{ evento.nombre_evento }}</h3>
                    <p style="text-align: center; color: #888; font-size: 1.1rem; margin-bottom: 30px;">
                        <i class="fa-solid fa-location-dot"></i> {{ evento.ciudad }}, {{ evento.pais }} | 
                        <i class="fa-solid fa-calendar-days"></i> {{ evento.fecha_evento }}<br>
                        <i class="fa-solid fa-bullhorn"></i> Promotor: {{ evento.promotor }}
                    </p>
                    <div style="text-align: center; margin-bottom: 30px;">
                        <img loading="lazy" src="{{ evento.img_video_path }}" style="width: 100%; max-width: 600px; height: auto; border-radius: 8px;">
                    </div>
                    <p style="font-size: 1.1rem; line-height: 1.8; color: #ddd; margin-bottom: 20px; text-align: justify; white-space: pre-line;">{{ evento.bio_corta }}</p>
                    <div style="display: flex; gap: 15px; justify-content: center; margin-top: 30px;">
                        {% if evento.fb_link %}<a href="{{ evento.fb_link }}" target="_blank" class="platform-btn" style="background: transparent; padding: 8px 15px; font-size: 0.95rem; border-radius: 4px; color: var(--accent-color); text-decoration: none; border: 1px solid var(--accent-color); min-width: auto; transition: all 0.3s;" onmouseover="this.style.background='var(--accent-color)'; this.style.color='#000';" onmouseout="this.style.background='transparent'; this.style.color='var(--accent-color)';"><i class="fa-brands fa-facebook-f"></i> {{ evento.promotor }}</a>{% endif %}
                        {% if evento.ig_link %}<a href="{{ evento.ig_link }}" target="_blank" class="platform-btn" style="background: transparent; padding: 8px 15px; font-size: 0.95rem; border-radius: 4px; color: var(--accent-color); text-decoration: none; border: 1px solid var(--accent-color); min-width: auto; transition: all 0.3s;" onmouseover="this.style.background='var(--accent-color)'; this.style.color='#000';" onmouseout="this.style.background='transparent'; this.style.color='var(--accent-color)';"><i class="fa-brands fa-instagram"></i> {{ evento.promotor }}</a>{% endif %}
                    </div>
                </div>
            </div>
        </div>
        {% endfor %}

        <!-- BANDA MODALS (One for each band) -->"""

content = content.replace("<!-- BANDA MODALS (One for each band) -->", evento_modals_html)

with open("templates/index.html", "w") as f:
    f.write(content)


# 3. Update admin_dashboard.html to remove maxlength
with open("templates/admin_dashboard.html", "r") as f:
    admin_content = f.read()

old_admin_field = """            <label style="margin-top: 15px;">Sobre el Evento (Máximo 1200 caracteres)</label>
            <textarea name="bio_corta" rows="6" maxlength="1200" placeholder="Escribe aquí toda la información necesaria para balancear el espacio con la Banda de la Semana..." required></textarea>"""

new_admin_field = """            <label style="margin-top: 15px;">Sobre el Evento (Ilimitado en Panel de Control, 1200 en Portada)</label>
            <textarea name="bio_corta" rows="6" placeholder="Todo el texto que pongas aquí se mostrará en 'Leer nota completa'. La portada mostrará los primeros 1200 caracteres." required></textarea>"""

admin_content = admin_content.replace(old_admin_field, new_admin_field)

with open("templates/admin_dashboard.html", "w") as f:
    f.write(admin_content)

print("Modal restored, button restored, admin limits removed")
