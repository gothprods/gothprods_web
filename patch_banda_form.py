import re

with open("templates/admin_dashboard.html", "r") as f:
    content = f.read()

# 1. Add inputs to form
old_form = """            <label>Título de la Reseña</label>
            <input type="text" name="titulo_resena" placeholder="Ej. Una obra maestra del Death Metal" required style="margin-bottom: 15px;">

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div>
                    <label>Nombre de la Banda</label>"""
new_form = """            <label>Título de la Reseña</label>
            <input type="text" name="titulo_resena" placeholder="Ej. Una obra maestra del Death Metal" required style="margin-bottom: 15px;">

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 15px;">
                <div>
                    <label>Fecha de Inicio <small>(Opcional)</small></label>
                    <input type="date" name="fecha_inicio">
                </div>
                <div>
                    <label>Fecha de Fin <small>(Opcional)</small></label>
                    <input type="date" name="fecha_fin">
                </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div>
                    <label>Nombre de la Banda</label>"""
content = content.replace(old_form, new_form)

# 2. Add header
old_th = """                        <th style="padding: 10px;">Origen</th>
                        <th style="padding: 10px;">Fecha Agregada</th>
                        <th style="padding: 10px; text-align: center;">Activo (Inicio)</th>"""
new_th = """                        <th style="padding: 10px;">Origen</th>
                        <th style="padding: 10px;">Vigencia</th>
                        <th style="padding: 10px; text-align: center;">Activo (Inicio)</th>"""
content = content.replace(old_th, new_th)

# 3. Add data
old_td = """                        <td style="padding: 10px; color: #fff;">{{ b.nombre }}</td>
                        <td style="padding: 10px; color: #aaa;">{{ b.ciudad }}, {{ b.pais }}</td>
                        <td style="padding: 10px; color: #888;">{{ b.created_at.split()[0] if b.created_at else '' }}</td>
                        <td style="padding: 10px; text-align: center;">"""
new_td = """                        <td style="padding: 10px; color: #fff;">{{ b.nombre }}</td>
                        <td style="padding: 10px; color: #aaa;">{{ b.ciudad }}, {{ b.pais }}</td>
                        <td style="padding: 10px; color: #888; font-size: 0.8rem; line-height: 1.2;">
                            {% if b.fecha_inicio and b.fecha_fin %}
                                {{ b.fecha_inicio }} <br>al {{ b.fecha_fin }}
                            {% elif b.fecha_inicio %}
                                Desde {{ b.fecha_inicio }}
                            {% elif b.fecha_fin %}
                                Hasta {{ b.fecha_fin }}
                            {% else %}
                                Siempre
                            {% endif %}
                        </td>
                        <td style="padding: 10px; text-align: center;">"""
content = content.replace(old_td, new_td)

# 4. Add data attributes to button
old_btn = """                                data-id="{{ b.id }}"
                                data-nombre="{{ b.nombre | default('', true) }}"
                                data-pais="{{ b.pais | default('', true) }}"
                                data-ciudad="{{ b.ciudad | default('', true) }}"
                                data-biocorta="{{ b.bio_corta | default('', true) }}"
"""
new_btn = """                                data-id="{{ b.id }}"
                                data-nombre="{{ b.nombre | default('', true) }}"
                                data-fechainicio="{{ b.fecha_inicio | default('', true) }}"
                                data-fechafin="{{ b.fecha_fin | default('', true) }}"
                                data-pais="{{ b.pais | default('', true) }}"
                                data-ciudad="{{ b.ciudad | default('', true) }}"
                                data-biocorta="{{ b.bio_corta | default('', true) }}"
"""
content = content.replace(old_btn, new_btn)

# 5. Add to editBandaRecord JS
old_js = """    document.querySelector('#banda-form input[name="nombre"]').value = btn.getAttribute('data-nombre') || '';
    document.querySelector('#banda-form input[name="pais"]').value = btn.getAttribute('data-pais') || '';"""
new_js = """    document.querySelector('#banda-form input[name="nombre"]').value = btn.getAttribute('data-nombre') || '';
    document.querySelector('#banda-form input[name="fecha_inicio"]').value = btn.getAttribute('data-fechainicio') || '';
    document.querySelector('#banda-form input[name="fecha_fin"]').value = btn.getAttribute('data-fechafin') || '';
    document.querySelector('#banda-form input[name="pais"]').value = btn.getAttribute('data-pais') || '';"""
content = content.replace(old_js, new_js)

with open("templates/admin_dashboard.html", "w") as f:
    f.write(content)

print("HTML patched successfully")
