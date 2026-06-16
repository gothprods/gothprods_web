import re

# 1. Update index.html
with open("templates/index.html", "r") as f:
    content = f.read()

old_resumen = """                                        <h4 style="color: var(--accent-color); font-family: 'Oswald', sans-serif; font-size: 1.1rem; text-transform: uppercase; margin-bottom: 10px; border-bottom: 1px solid #444; padding-bottom: 5px;"><i class="fa-solid fa-align-left"></i> Resumen</h4>"""

new_resumen = """                                        <h4 style="color: var(--accent-color); font-family: 'Oswald', sans-serif; font-size: 1.1rem; text-transform: uppercase; margin-bottom: 10px; border-bottom: 1px solid #444; padding-bottom: 5px;"><i class="fa-solid fa-align-left"></i> Sobre el Evento</h4>"""

content = content.replace(old_resumen, new_resumen)

with open("templates/index.html", "w") as f:
    f.write(content)

# 2. Update admin_dashboard.html to give a larger textarea for the short bio
with open("templates/admin_dashboard.html", "r") as f:
    admin_content = f.read()

old_label = """            <label style="margin-top: 15px;">Biografía Corta del Evento</label>
            <textarea name="bio_corta" rows="4" placeholder="Breve descripción del evento..." required></textarea>"""

new_label = """            <label style="margin-top: 15px;">Sobre el Evento (Resumen)</label>
            <textarea name="bio_corta" rows="10" placeholder="Escribe aquí toda la información necesaria para balancear el espacio con la Banda de la Semana..." required></textarea>"""

admin_content = admin_content.replace(old_label, new_label)

with open("templates/admin_dashboard.html", "w") as f:
    f.write(admin_content)

print("Text updated successfully")
