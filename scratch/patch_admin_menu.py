import re

with open('templates/admin_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# I will replace the whole Configuración del Menú Flotante section up to the Agenda Metalera
start_str = '<h4 style="color: var(--accent-color); margin-top: 30px; margin-bottom: 15px; border-bottom: 1px solid #333; padding-bottom: 5px;"><i class="fa-solid fa-bars-staggered"></i> Configuración del Menú Flotante</h4>'
end_str = '<!-- SOCIAL MEDIA LINKS -->'

if start_str in content and end_str in content:
    start_idx = content.find(start_str)
    end_idx = content.find(end_str)
    
    new_html = start_str + """
<div style="display: flex; flex-direction: column; gap: 10px;">
    <!-- Radar del Caos -->
    <div style="background: #1a1a1a; padding: 15px; border-radius: 8px; border: 1px solid #333; margin-bottom: 15px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <label style="display: flex; align-items: center; gap: 10px; cursor: pointer; font-weight: bold; margin: 0; color: var(--accent-color);">
                Radar del Caos
            </label>
            <span style="font-size: 0.75rem; color: #888;">(Menú)</span>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
            <div><label style="font-size: 0.8rem; color: #aaa;">Título</label><input type="text" name="title_destacados" value="{{ settings.get('title_destacados', 'Radar del Caos') }}" style="background: #222; padding: 8px; border-radius: 4px; border: 1px solid #444; width: 100%; color: #fff;"></div>
            <div><label style="font-size: 0.8rem; color: #aaa;">Ícono (Imagen)</label><input type="file" name="icon_destacados" accept="image/*" style="background: #222; padding: 6px; border-radius: 4px; border: 1px solid #444; width: 100%; color: #fff; font-size: 0.8rem;"></div>
        </div>
    </div>

    <!-- El Pit -->
    <div style="background: #1a1a1a; padding: 15px; border-radius: 8px; border: 1px solid #333; margin-bottom: 15px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <label style="display: flex; align-items: center; gap: 10px; cursor: pointer; font-weight: bold; margin: 0; color: var(--accent-color);">
                El Pit
            </label>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
            <div><label style="font-size: 0.8rem; color: #aaa;">Título</label><input type="text" name="title_el_pit" value="{{ settings.get('title_el_pit', 'El Pit') }}" style="background: #222; padding: 8px; border-radius: 4px; border: 1px solid #444; width: 100%; color: #fff;"></div>
            <div><label style="font-size: 0.8rem; color: #aaa;">Ícono (Imagen)</label><input type="file" name="icon_el_pit" accept="image/*" style="background: #222; padding: 6px; border-radius: 4px; border: 1px solid #444; width: 100%; color: #fff; font-size: 0.8rem;"></div>
        </div>
    </div>

    <!-- Nuestros Podcasts -->
    <div style="background: #1a1a1a; padding: 15px; border-radius: 8px; border: 1px solid #333; margin-bottom: 15px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <label style="display: flex; align-items: center; gap: 10px; cursor: pointer; font-weight: bold; margin: 0; color: var(--accent-color);">
                Nuestros Podcasts
            </label>
            <span style="font-size: 0.75rem; color: #888;">(La Galería + Metal Pulse + Entrevistas)</span>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
            <div><label style="font-size: 0.8rem; color: #aaa;">Título en el Menú</label><input type="text" name="title_podcasts" value="{{ settings.get('title_podcasts', 'Nuestros Podcasts') }}" style="background: #222; padding: 8px; border-radius: 4px; border: 1px solid #444; width: 100%; color: #fff;"></div>
            <div><label style="font-size: 0.8rem; color: #aaa;">Ícono (Imagen)</label><input type="file" name="icon_podcasts" accept="image/*" style="background: #222; padding: 6px; border-radius: 4px; border: 1px solid #444; width: 100%; color: #fff; font-size: 0.8rem;"></div>
        </div>
    </div>

    <!-- El Noticiero Nocturno -->
    <div style="background: #1a1a1a; padding: 15px; border-radius: 8px; border: 1px solid #333; margin-bottom: 15px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <label style="display: flex; align-items: center; gap: 10px; cursor: pointer; font-weight: bold; margin: 0; color: var(--accent-color);">
                El Noticiero Nocturno
            </label>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
            <div><label style="font-size: 0.8rem; color: #aaa;">Título</label><input type="text" name="title_news" value="{{ settings.get('title_news', 'El Noticiero Nocturno') }}" style="background: #222; padding: 8px; border-radius: 4px; border: 1px solid #444; width: 100%; color: #fff;"></div>
            <div><label style="font-size: 0.8rem; color: #aaa;">Ícono (Imagen)</label><input type="file" name="icon_news" accept="image/*" style="background: #222; padding: 6px; border-radius: 4px; border: 1px solid #444; width: 100%; color: #fff; font-size: 0.8rem;"></div>
        </div>
    </div>

    <!-- Conciertos -->
    <div style="background: #1a1a1a; padding: 15px; border-radius: 8px; border: 1px solid #333; margin-bottom: 15px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <label style="display: flex; align-items: center; gap: 10px; cursor: pointer; font-weight: bold; margin: 0; color: var(--accent-color);">
                Conciertos
            </label>
            <span style="font-size: 0.75rem; color: #888;">(Reseñas + Agenda)</span>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
            <div><label style="font-size: 0.8rem; color: #aaa;">Título en el Menú</label><input type="text" name="title_conciertos" value="{{ settings.get('title_conciertos', 'Conciertos') }}" style="background: #222; padding: 8px; border-radius: 4px; border: 1px solid #444; width: 100%; color: #fff;"></div>
            <div><label style="font-size: 0.8rem; color: #aaa;">Ícono (Imagen)</label><input type="file" name="icon_conciertos" accept="image/*" style="background: #222; padding: 6px; border-radius: 4px; border: 1px solid #444; width: 100%; color: #fff; font-size: 0.8rem;"></div>
        </div>
    </div>

    <!-- El Equipo / Historia -->
    <div style="background: #1a1a1a; padding: 15px; border-radius: 8px; border: 1px solid #333; margin-bottom: 15px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <label style="display: flex; align-items: center; gap: 10px; cursor: pointer; font-weight: bold; margin: 0; color: var(--accent-color);">
                <label class="switch" style="margin: 0;">
                    <input type="checkbox" name="show_equipo_menu" value="1" {% if settings.get('show_equipo_menu', '0') == '1' %}checked{% endif %}>
                    <span class="slider"></span>
                </label>
                El Equipo, La Historia
            </label>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
            <div><label style="font-size: 0.8rem; color: #aaa;">Título</label><input type="text" name="title_equipo" value="{{ settings.get('title_equipo', 'El Equipo, La Historia') }}" style="background: #222; padding: 8px; border-radius: 4px; border: 1px solid #444; width: 100%; color: #fff;"></div>
            <div><label style="font-size: 0.8rem; color: #aaa;">Ícono (Imagen)</label><input type="file" name="icon_equipo" accept="image/*" style="background: #222; padding: 6px; border-radius: 4px; border: 1px solid #444; width: 100%; color: #fff; font-size: 0.8rem;"></div>
        </div>
    </div>

    <!-- Servicios (NUEVO) -->
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
            <div><label style="font-size: 0.8rem; color: #aaa;">Título</label><input type="text" name="title_servicios" value="{{ settings.get('title_servicios', 'Servicios') }}" style="background: #222; padding: 8px; border-radius: 4px; border: 1px solid #444; width: 100%; color: #fff;"></div>
            <div><label style="font-size: 0.8rem; color: #aaa;">Ícono (Imagen)</label><input type="file" name="icon_servicios" accept="image/*" style="background: #222; padding: 6px; border-radius: 4px; border: 1px solid #444; width: 100%; color: #fff; font-size: 0.8rem;"></div>
        </div>
    </div>

    <!-- Contáctanos -->
    <div style="background: #1a1a1a; padding: 15px; border-radius: 8px; border: 1px solid #333; margin-bottom: 15px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <label style="display: flex; align-items: center; gap: 10px; cursor: pointer; font-weight: bold; margin: 0; color: var(--accent-color);">
                Contáctanos
            </label>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
            <div><label style="font-size: 0.8rem; color: #aaa;">Título</label><input type="text" name="title_contacto" value="{{ settings.get('title_contacto', 'Contáctanos') }}" style="background: #222; padding: 8px; border-radius: 4px; border: 1px solid #444; width: 100%; color: #fff;"></div>
            <div><label style="font-size: 0.8rem; color: #aaa;">Ícono (Imagen)</label><input type="file" name="icon_contacto" accept="image/*" style="background: #222; padding: 6px; border-radius: 4px; border: 1px solid #444; width: 100%; color: #fff; font-size: 0.8rem;"></div>
        </div>
    </div>
</div>

<!-- HIDDEN FIELDS PARA MANTENER LA VISIBILIDAD DE LAS SECCIONES EN LA PÁGINA (Si apagamos el toggle del menú, cómo controlamos la página? El usuario no pidió apagarlos de la página, por ahora los dejaremos siempre activos en la pagina si antes estaban, o usamos hidden inputs) -->
<!-- De hecho, es mejor poner los toggles para las secciones dentro de sus propias tarjetas de look and feel debajo, o dejarlos como hidden si el admin ya no los usa -->
<input type="hidden" name="show_galeria_nocturna" value="1">
<input type="hidden" name="show_metalpulse" value="1">
<input type="hidden" name="show_interviews" value="1">
<input type="hidden" name="show_reviews" value="1">
<input type="hidden" name="show_agenda" value="1">

\n""" + end_str

    content = content[:start_idx] + new_html + content[end_idx + len(end_str):]

    with open('templates/admin_dashboard.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Admin dashboard menu config updated!")
else:
    print("Tags not found in admin_dashboard.html")

