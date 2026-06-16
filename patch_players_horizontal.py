import re

with open("templates/index.html", "r") as f:
    content = f.read()

# Make "Último Lanzamiento" span full width
old_lanzamiento_start = """                        <!-- Columna 3: Último Lanzamiento -->
                        {% if banda_semana.ultimo_lanzamiento_sp_link or banda_semana.ultimo_lanzamiento_ap_link %}
                        <div>
                            <h4 style="color: var(--accent-color); font-family: 'Oswald', sans-serif; font-size: 1.1rem; text-transform: uppercase; margin-bottom: 10px; border-bottom: 1px solid #444; padding-bottom: 5px;">
                                <i class="fa-solid fa-compact-disc"></i> Último Lanzamiento
                            </h4>"""

new_lanzamiento_start = """                        <!-- Columna 3: Último Lanzamiento -->
                        {% if banda_semana.ultimo_lanzamiento_sp_link or banda_semana.ultimo_lanzamiento_ap_link %}
                        <div style="grid-column: 1 / -1;">
                            <h4 style="color: var(--accent-color); font-family: 'Oswald', sans-serif; font-size: 1.1rem; text-transform: uppercase; margin-bottom: 10px; border-bottom: 1px solid #444; padding-bottom: 5px;">
                                <i class="fa-solid fa-compact-disc"></i> Último Lanzamiento
                            </h4>"""
content = content.replace(old_lanzamiento_start, new_lanzamiento_start)

# Force the players flex row to NOT wrap, so they always sit side by side
old_players_wrapper = """                            <!-- Reproductor Iframe y Botones Apareados -->
                            <div style="display: flex; flex-direction: row; flex-wrap: wrap; gap: 15px;">"""

new_players_wrapper = """                            <!-- Reproductor Iframe y Botones Apareados -->
                            <div style="display: flex; flex-direction: row; flex-wrap: nowrap; gap: 15px;">"""
content = content.replace(old_players_wrapper, new_players_wrapper)

with open("templates/index.html", "w") as f:
    f.write(content)

print("Players forced to horizontal row successfully")
