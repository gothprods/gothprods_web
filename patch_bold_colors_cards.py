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
    
    # --- Modals ---
    content = content.replace(
        '<h2 class="notranslate" style="color: var(--accent-color); font-size: 2.5rem;',
        '<h2 class="notranslate" style="color: var(--accent-color); font-weight: bold; font-size: 2.5rem;'
    )
    # Bandas y Eventos modales (por si acaso faltó alguno)
    content = content.replace(
        '<h2 class="notranslate" style="color: var(--accent-color); font-size: 3rem;',
        '<h2 class="notranslate" style="color: var(--accent-color); font-weight: bold; font-size: 3rem;'
    )
    
    # --- Cards Main Page ---
    content = content.replace(
        '<h3 class="notranslate" style="font-size: 2rem; color: var(--accent-color);',
        '<h3 class="notranslate" style="font-size: 2rem; color: var(--accent-color); font-weight: bold;'
    )
    content = content.replace(
        '<h3 class="notranslate" style="color: var(--accent-color); font-family: \'Oswald\', sans-serif; font-size: 1.5rem;',
        '<h3 class="notranslate" style="color: var(--accent-color); font-weight: bold; font-family: \'Oswald\', sans-serif; font-size: 1.5rem;'
    )
    
    # Nombres de eventos en las cards (que antes estaban en blanco #fff)
    content = content.replace(
        '<p style="font-size: 1.2rem; color: #fff; font-weight: bold; margin-bottom: 5px;">{{ evento.nombre_evento }}</p>',
        '<p style="font-size: 1.2rem; color: var(--accent-color); font-weight: bold; margin-bottom: 5px;">{{ evento.nombre_evento }}</p>'
    )
    
    # Detalles de Evento (fecha, etc) en modals / cards
    content = content.replace(
        '<p style="font-size: 1rem; color: #888; margin-bottom: 10px;">',
        '<p style="font-size: 1rem; color: var(--accent-color); font-weight: bold; margin-bottom: 10px;">'
    )
    
    # Detalles de Banda en modals
    content = content.replace(
        '<p style="text-align: center; color: #888; font-size: 1.1rem; margin-bottom: 30px;">',
        '<p style="text-align: center; color: var(--accent-color); font-weight: bold; font-size: 1.1rem; margin-bottom: 30px;">'
    )
    
    # Autor en modales de articulos
    content = content.replace(
        '<p style="text-align: center; color: #888; margin-bottom: 20px; font-size: 0.95rem;">',
        '<p style="text-align: center; color: var(--accent-color); font-weight: bold; margin-bottom: 20px; font-size: 0.95rem;">'
    )

    with open(filepath, "w") as f:
        f.write(content)

print("Card and modal styles updated successfully.")
