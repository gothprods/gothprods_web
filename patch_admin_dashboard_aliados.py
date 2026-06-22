import re

html_to_add = """
<h4 style="color: var(--accent-color); margin-top: 30px; margin-bottom: 15px; border-bottom: 1px solid #333; padding-bottom: 5px;"><i class="fa-solid fa-handshake"></i> Medios Aliados</h4>
<div style="background: #1a1a1a; padding: 15px; border-radius: 8px; border: 1px solid #333; margin-bottom: 15px;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
        <label style="display: flex; align-items: center; gap: 10px; cursor: pointer; font-weight: bold; margin: 0; color: var(--accent-color);">
            <label class="switch" style="margin: 0;">
                <input type="checkbox" name="show_medios_aliados" value="1" {% if settings.get('show_medios_aliados', '0') == '1' %}checked{% endif %}>
                <span class="slider"></span>
            </label>
            Mostrar Sección: Medios Aliados
        </label>
    </div>
    <p style="font-size: 0.8rem; color: #888; margin-bottom: 15px;">Sube hasta 10 logos. La página ajustará y centrará automáticamente la cantidad que subas. Deja en blanco los que no uses.</p>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
"""
for i in range(1, 11):
    html_to_add += f"""        <div>
            <label style="font-size: 0.8rem; color: #aaa;">Logo Aliado {i}</label>
            <input type="file" name="logo_aliado_{i}" accept="image/*" style="background: #222; padding: 6px; border-radius: 4px; border: 1px solid #444; width: 100%; color: #fff; font-size: 0.8rem;">
        </div>\n"""

html_to_add += """    </div>
</div>
"""

with open("templates/admin_dashboard.html", "r") as f:
    content = f.read()

content = content.replace('<button type="submit" style="margin-top: 30px;"><i class="fa-solid fa-save"></i> Guardar Cambios</button>', html_to_add + '\n            <button type="submit" style="margin-top: 30px;"><i class="fa-solid fa-save"></i> Guardar Cambios</button>')

with open("templates/admin_dashboard.html", "w") as f:
    f.write(content)

print("Admin dashboard patched with Medios Aliados.")
