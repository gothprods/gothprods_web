import re

with open("templates/admin_dashboard.html", "r") as f:
    content = f.read()

# 1. Add Tab Button
old_btn = """        <button class="tab-btn" onclick="openTab(event, 'tab-banda')"><i class="fa-solid fa-star"></i> Banda de la Semana</button>"""
new_btn = """        <button class="tab-btn" onclick="openTab(event, 'tab-banda')"><i class="fa-solid fa-star"></i> Banda de la Semana</button>
        <button class="tab-btn" onclick="openTab(event, 'tab-eventos')"><i class="fa-solid fa-calendar-star"></i> Eventos de la Semana</button>"""
content = content.replace(old_btn, new_btn)

# 2. Add Tab Content
# We'll insert it right before `<div id="tab-caos" class="tab-content">`
old_content_marker = """    <div id="tab-caos" class="tab-content">"""

new_tab_html = """
    <!-- TAB: EVENTOS DE LA SEMANA -->
    <div id="tab-eventos" class="tab-content">
        <h3 id="form-eventos-title"><i class="fa-solid fa-calendar-star"></i> Gestión Eventos de la Semana</h3>
        <p style="text-align: center; color: var(--text-muted); margin-bottom: 20px; font-size: 0.9rem;">Agrega los eventos relevantes a los cuales daremos difusión.</p>
        
        <form id="eventos-form" method="POST" action="/admin/eventos" enctype="multipart/form-data" style="max-width: 800px; margin: 0 auto; background: #111; padding: 25px; border-radius: 8px; border: 1px solid #333;">
            <label>Título del Artículo</label>
            <input type="text" name="titulo_articulo" placeholder="Ej. El Festival de Metal Más Esperado" required style="margin-bottom: 15px;">

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 15px;">
                <div>
                    <label>Fecha de Inicio Publicación <small>(Opcional)</small></label>
                    <input type="date" name="fecha_inicio_pub">
                </div>
                <div>
                    <label>Fecha de Fin Publicación <small>(Opcional)</small></label>
                    <input type="date" name="fecha_fin_pub">
                </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div>
                    <label>Nombre del Evento o Banda</label>
                    <input type="text" name="nombre_evento" required>
                </div>
                <div>
                    <label>Imagen o Video Promocional</label>
                    <input type="file" name="img_video_path" accept="image/*, video/*" required style="background: #222; padding: 10px; border-radius: 4px; border: 1px solid #444; width: 100%; color: #fff;">
                </div>
            </div>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 15px;">
                <div>
                    <label>Nombre del Promotor</label>
                    <input type="text" name="promotor" placeholder="Ej: Cacique Entertainment" required>
                </div>
                <div>
                    <label>Fecha del Evento</label>
                    <input type="date" name="fecha_evento" required>
                </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 15px;">
                <div>
                    <label>País</label>
                    <input type="text" name="pais" placeholder="Ej: México" required>
                </div>
                <div>
                    <label>Ciudad</label>
                    <input type="text" name="ciudad" placeholder="Ej: CDMX" required>
                </div>
            </div>

            <label style="margin-top: 15px;">Biografía Corta del Evento</label>
            <textarea name="bio_corta" rows="4" placeholder="Breve descripción del evento..." required></textarea>

            <label style="margin-top: 15px;">Texto del Artículo</label>
            <textarea name="texto_articulo" rows="6" placeholder="Escribe aquí tu artículo completo sobre el evento..." required></textarea>

            <h4 style="margin-top: 25px; border-bottom: 1px solid #333; padding-bottom: 5px; color: var(--accent-color);"><i class="fa-solid fa-share-nodes"></i> Redes Sociales del Evento</h4>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                <input type="url" name="fb_link" placeholder="Facebook URL">
                <input type="url" name="ig_link" placeholder="Instagram URL">
            </div>

            <div style="display: flex; gap: 10px; margin-top: 30px;">
                <button type="submit" id="eventos-submit-btn"><i class="fa-solid fa-plus"></i> Agregar Evento de la Semana</button>
                <button type="button" id="eventos-cancel-btn" onclick="cancelEventoEdit()" style="display: none; background: #555; color: white;"><i class="fa-solid fa-xmark"></i> Cancelar</button>
            </div>
        </form>

        <h4 style="margin-top: 40px; border-bottom: 1px solid #333; padding-bottom: 10px;"><i class="fa-solid fa-list"></i> Historial de Eventos de la Semana</h4>
        <div style="overflow-x: auto;">
            <table style="width: 100%; border-collapse: collapse; font-size: 0.9rem; text-align: left;">
                <thead>
                    <tr style="border-bottom: 1px solid #444;">
                        <th style="padding: 10px;">Evento</th>
                        <th style="padding: 10px;">Promotor</th>
                        <th style="padding: 10px;">Vigencia Pub.</th>
                        <th style="padding: 10px; text-align: center;">Activo</th>
                        <th style="padding: 10px; text-align: right;">Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    {% for e in todos_eventos %}
                    <tr style="border-bottom: 1px solid #333;">
                        <td style="padding: 10px; color: #fff;">{{ e.nombre_evento }}<br><small style="color: #888;">{{ e.fecha_evento }} - {{ e.ciudad }}</small></td>
                        <td style="padding: 10px; color: #aaa;">{{ e.promotor }}</td>
                        <td style="padding: 10px; color: #888; font-size: 0.8rem; line-height: 1.2;">
                            {% if e.fecha_inicio_pub and e.fecha_fin_pub %}
                                {{ e.fecha_inicio_pub }} <br>al {{ e.fecha_fin_pub }}
                            {% elif e.fecha_inicio_pub %}
                                Desde {{ e.fecha_inicio_pub }}
                            {% elif e.fecha_fin_pub %}
                                Hasta {{ e.fecha_fin_pub }}
                            {% else %}
                                Siempre
                            {% endif %}
                        </td>
                        <td style="padding: 10px; text-align: center;">
                            <label class="switch">
                                {% set active = e.is_active if 'is_active' in e.keys() else 1 %}
                                <input type="checkbox" onchange="toggleEventoStatus({{ e.id }})" {% if active == 1 %}checked{% endif %}>
                                <span class="slider"></span>
                            </label>
                        </td>
                        <td style="padding: 10px; text-align: right; white-space: nowrap;">
                            <button type="button" class="edit-banda-btn"
                                data-id="{{ e.id }}"
                                data-titulo="{{ e.titulo_articulo | default('', true) }}"
                                data-nombre="{{ e.nombre_evento | default('', true) }}"
                                data-fechainiciopub="{{ e.fecha_inicio_pub | default('', true) }}"
                                data-fechafinpub="{{ e.fecha_fin_pub | default('', true) }}"
                                data-fechaevento="{{ e.fecha_evento | default('', true) }}"
                                data-promotor="{{ e.promotor | default('', true) }}"
                                data-pais="{{ e.pais | default('', true) }}"
                                data-ciudad="{{ e.ciudad | default('', true) }}"
                                data-biocorta="{{ e.bio_corta | default('', true) }}"
                                data-texto="{{ e.texto_articulo | default('', true) }}"
                                data-ig="{{ e.ig_link | default('', true) }}"
                                data-fb="{{ e.fb_link | default('', true) }}"
                                onclick="editEventoRecord(this)">
                                <i class="fa-solid fa-pen"></i> Editar
                            </button>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>

    <div id="tab-caos" class="tab-content">"""

content = content.replace(old_content_marker, new_tab_html)

# 3. Add JS functions
old_js_marker = """function setPreviewMode(mode) {"""

new_js = """function toggleEventoStatus(id) {
    fetch('/admin/eventos/toggle/' + id, { method: 'POST' })
    .then(r => r.json())
    .then(data => {
        if (!data.success) {
            alert('Error al cambiar el estado del evento');
            location.reload();
        }
    })
    .catch(err => {
        console.error(err);
        alert('Error de conexión');
    });
}

function editEventoRecord(btn) {
    var id = btn.getAttribute('data-id');
    
    var eventosBtn = document.querySelector(".tab-btn[onclick*='tab-eventos']");
    if(eventosBtn) openTab({currentTarget: eventosBtn}, 'tab-eventos');
    
    document.getElementById('form-eventos-title').innerHTML = '<i class="fa-solid fa-pen-nib"></i> Editar Evento #' + id;
    document.getElementById('eventos-form').action = '/admin/eventos/edit/' + id;
    document.getElementById('eventos-submit-btn').innerHTML = '<i class="fa-solid fa-save"></i> Guardar Cambios';
    document.getElementById('eventos-cancel-btn').style.display = 'block';
    
    document.querySelector('#eventos-form input[name="titulo_articulo"]').value = btn.getAttribute('data-titulo') || '';
    document.querySelector('#eventos-form input[name="nombre_evento"]').value = btn.getAttribute('data-nombre') || '';
    document.querySelector('#eventos-form input[name="fecha_inicio_pub"]').value = btn.getAttribute('data-fechainiciopub') || '';
    document.querySelector('#eventos-form input[name="fecha_fin_pub"]').value = btn.getAttribute('data-fechafinpub') || '';
    document.querySelector('#eventos-form input[name="fecha_evento"]').value = btn.getAttribute('data-fechaevento') || '';
    document.querySelector('#eventos-form input[name="promotor"]').value = btn.getAttribute('data-promotor') || '';
    document.querySelector('#eventos-form input[name="pais"]').value = btn.getAttribute('data-pais') || '';
    document.querySelector('#eventos-form input[name="ciudad"]').value = btn.getAttribute('data-ciudad') || '';
    document.querySelector('#eventos-form textarea[name="bio_corta"]').value = btn.getAttribute('data-biocorta') || '';
    document.querySelector('#eventos-form textarea[name="texto_articulo"]').value = btn.getAttribute('data-texto') || '';
    document.querySelector('#eventos-form input[name="ig_link"]').value = btn.getAttribute('data-ig') || '';
    document.querySelector('#eventos-form input[name="fb_link"]').value = btn.getAttribute('data-fb') || '';
    
    document.querySelector('#eventos-form input[name="img_video_path"]').required = false;
    
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function cancelEventoEdit() {
    document.getElementById('form-eventos-title').innerHTML = '<i class="fa-solid fa-calendar-star"></i> Gestión Eventos de la Semana';
    document.getElementById('eventos-form').action = '/admin/eventos';
    document.getElementById('eventos-submit-btn').innerHTML = '<i class="fa-solid fa-plus"></i> Agregar Evento de la Semana';
    document.getElementById('eventos-cancel-btn').style.display = 'none';
    
    document.getElementById('eventos-form').reset();
    document.querySelector('#eventos-form input[name="img_video_path"]').required = true;
}

function setPreviewMode(mode) {"""

content = content.replace(old_js_marker, new_js)

with open("templates/admin_dashboard.html", "w") as f:
    f.write(content)

print("HTML patched successfully")
