import re

with open("templates/index.html", "r") as f:
    content = f.read()

# 1. Update Banda slide flex alignment and image height
old_banda = """                    <div class="grid-container" style="display: flex; flex-wrap: wrap; align-items: center; gap: 20px;">
                <div style="flex: 1; min-width: 200px; max-width: 350px; margin: 0 auto;">
                    <img loading="lazy" src="{{ banda_semana.img_video_path }}" alt="{{ banda_semana.nombre }}" style="width: 100%; height: auto; border-radius: 12px; box-shadow: 0 10px 20px rgba(0,0,0,0.8);">
                </div>"""

new_banda = """                    <div class="grid-container" style="display: flex; flex-wrap: wrap; align-items: flex-start; gap: 20px;">
                <div style="flex: 1; min-width: 200px; max-width: 350px; margin: 0 auto;">
                    <img loading="lazy" src="{{ banda_semana.img_video_path }}" alt="{{ banda_semana.nombre }}" style="width: 100%; height: 350px; object-fit: cover; border-radius: 12px; box-shadow: 0 10px 20px rgba(0,0,0,0.8);">
                </div>"""
content = content.replace(old_banda, new_banda)

# 2. Update Evento slide flex alignment and image height
old_evento = """                        <div class="grid-container" style="display: flex; flex-wrap: wrap; align-items: center; gap: 20px;">
                            <div style="flex: 1; min-width: 200px; max-width: 350px; margin: 0 auto;">
                                <img loading="lazy" src="{{ evento.img_video_path }}" alt="{{ evento.nombre_evento }}" style="width: 100%; height: auto; border-radius: 12px; box-shadow: 0 10px 20px rgba(0,0,0,0.8);">
                            </div>"""

new_evento = """                        <div class="grid-container" style="display: flex; flex-wrap: wrap; align-items: flex-start; gap: 20px;">
                            <div style="flex: 1; min-width: 200px; max-width: 350px; margin: 0 auto;">
                                <img loading="lazy" src="{{ evento.img_video_path }}" alt="{{ evento.nombre_evento }}" style="width: 100%; height: 350px; object-fit: cover; border-radius: 12px; box-shadow: 0 10px 20px rgba(0,0,0,0.8);">
                            </div>"""
content = content.replace(old_evento, new_evento)

# 3. Update the players flex container
old_players = """                            <!-- Reproductor Iframe y Botones Apareados -->
                            <div style="display: flex; flex-direction: column; gap: 15px;">
                                {% if banda_semana.ultimo_lanzamiento_sp_link %}
                                <div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">"""

new_players = """                            <!-- Reproductor Iframe y Botones Apareados -->
                            <div style="display: flex; flex-direction: row; flex-wrap: wrap; gap: 15px;">
                                {% if banda_semana.ultimo_lanzamiento_sp_link %}
                                <div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap; flex: 1; min-width: 200px;">"""
content = content.replace(old_players, new_players)

# Update Apple player wrapper too
old_apple_player = """                                {% if banda_semana.ultimo_lanzamiento_ap_link %}
                                <div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">"""

new_apple_player = """                                {% if banda_semana.ultimo_lanzamiento_ap_link %}
                                <div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap; flex: 1; min-width: 200px;">"""
content = content.replace(old_apple_player, new_apple_player)

# Hide the Apple and Spotify buttons that are right next to the iframes to save more space, since the iframe itself is the player!
# Actually, the user just said "colocar los reproductores a la misma altura para ahorrar espacio". 
# The buttons are already part of that flex wrapper. 
# Let's change the buttons to be 100% width under the iframe to save horizontal space inside the 200px min-width column.
old_sp_btn = """<a href="{{ banda_semana.ultimo_lanzamiento_sp_link | replace('open.spotify.com/embed/', 'open.spotify.com/') }}" target="_blank" class="platform-btn spotify-btn" style="display: flex; align-items: center; justify-content: center; padding: 6px 10px; font-size: 0.8rem; border-radius: 6px; gap: 5px; min-width: 80px;"><i class="fa-brands fa-spotify"></i> Spotify</a>"""
new_sp_btn = """<a href="{{ banda_semana.ultimo_lanzamiento_sp_link | replace('open.spotify.com/embed/', 'open.spotify.com/') }}" target="_blank" class="platform-btn spotify-btn" style="display: flex; align-items: center; justify-content: center; padding: 6px 10px; font-size: 0.8rem; border-radius: 6px; gap: 5px; width: 100%;"><i class="fa-brands fa-spotify"></i> Abrir en Spotify</a>"""
content = content.replace(old_sp_btn, new_sp_btn)

old_ap_btn = """<a href="{{ banda_semana.ultimo_lanzamiento_ap_link | replace('embed.', '') }}" target="_blank" class="platform-btn apple-btn" style="display: flex; align-items: center; justify-content: center; padding: 6px 10px; font-size: 0.8rem; border-radius: 6px; gap: 5px; min-width: 80px;"><i class="fa-brands fa-apple"></i> Apple</a>"""
new_ap_btn = """<a href="{{ banda_semana.ultimo_lanzamiento_ap_link | replace('embed.', '') }}" target="_blank" class="platform-btn apple-btn" style="display: flex; align-items: center; justify-content: center; padding: 6px 10px; font-size: 0.8rem; border-radius: 6px; gap: 5px; width: 100%;"><i class="fa-brands fa-apple"></i> Abrir en Apple</a>"""
content = content.replace(old_ap_btn, new_ap_btn)


with open("templates/index.html", "w") as f:
    f.write(content)

print("Alignment and players patched successfully")
