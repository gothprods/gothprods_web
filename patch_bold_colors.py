import re
import os

files_to_patch = [
    "templates/index.html",
    "templates/banda.html",
    "templates/evento.html",
    "templates/articulo.html"
]

for filepath in files_to_patch:
    if not os.path.exists(filepath): continue
    
    with open(filepath, "r") as f:
        content = f.read()
    
    # 1. Update {{ banda_semana.nombre }} and {{ banda.nombre }}
    content = content.replace(
        '<h2 class="notranslate" style="color: var(--accent-color); font-size: 3rem;',
        '<h2 class="notranslate" style="color: var(--accent-color); font-weight: bold; font-size: 3rem;'
    )
    
    # 2. Update Origen / Formacion subtitles
    content = content.replace(
        '<p style="text-align: center; color: #888; font-size: 1.1rem; margin-bottom: 30px;">',
        '<p style="text-align: center; color: var(--accent-color); font-weight: bold; font-size: 1.1rem; margin-bottom: 30px;">'
    )
    
    # 3. Update {{ evento.titulo_articulo }} (which is also font-size: 3rem, so rule #1 covers it)
    
    # 4. Update {{ evento.nombre_evento }} in reading panels (h3 with #fff)
    content = content.replace(
        '<h3 style="text-align: center; color: #fff; font-size: 1.5rem; margin-bottom: 10px;">{{ evento.nombre_evento }}</h3>',
        '<h3 style="text-align: center; color: var(--accent-color); font-weight: bold; font-size: 1.5rem; margin-bottom: 10px;">{{ evento.nombre_evento }}</h3>'
    )
    
    # 5. Update {{ item.title }} in article modals/pages
    content = content.replace(
        '<h2 class="notranslate" style="color: var(--accent-color); font-size: 2.5rem;',
        '<h2 class="notranslate" style="color: var(--accent-color); font-weight: bold; font-size: 2.5rem;'
    )
    content = content.replace(
        '<h2 style="color: var(--accent-color); font-size: 3rem;',
        '<h2 style="color: var(--accent-color); font-weight: bold; font-size: 3rem;'
    )
    
    # 6. Update "Line Up:" and "Presentado por:"
    content = content.replace(
        '<p style="margin: 0; color: #ccc; font-size: 1rem;"><strong><i class="fa-solid fa-users"></i> Line Up:</strong>',
        '<p style="margin: 0; color: var(--accent-color); font-weight: bold; font-size: 1rem;"><strong><i class="fa-solid fa-users"></i> Line Up:</strong>'
    )
    content = content.replace(
        '<p style="margin: 0; color: #ccc; font-size: 1rem;"><strong><i class="fa-solid fa-bullhorn"></i> Presentado por:</strong>',
        '<p style="margin: 0; color: var(--accent-color); font-weight: bold; font-size: 1rem;"><strong><i class="fa-solid fa-bullhorn"></i> Presentado por:</strong>'
    )
    
    with open(filepath, "w") as f:
        f.write(content)

print("Styles updated in reading panels.")
