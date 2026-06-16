import re

# 1. Update index.html
with open("templates/index.html", "r") as f:
    content = f.read()

old_header_index = """                    <h2 class="notranslate" style="color: var(--accent-color); font-size: 2.5rem; margin-bottom: 5px; text-align: center; font-family: 'Oswald', sans-serif; text-transform: uppercase;">{{ evento.titulo_articulo }}</h2>
                    <h3 style="text-align: center; color: #fff; font-size: 1.5rem; margin-bottom: 10px;">{{ evento.nombre_evento }}</h3>
                    <p style="text-align: center; color: #888; font-size: 1.1rem; margin-bottom: 30px;">
                        <i class="fa-solid fa-location-dot"></i> {{ evento.ciudad }}, {{ evento.pais }} | 
                        <i class="fa-solid fa-calendar-days"></i> {{ evento.fecha_evento }}<br>
                        <i class="fa-solid fa-bullhorn"></i> Promotor: {{ evento.promotor }}
                    </p>
                    <div style="text-align: center; margin-bottom: 30px;">
                        <img loading="lazy" src="{{ evento.img_video_path }}" style="width: 100%; max-width: 600px; height: auto; border-radius: 8px;">
                    </div>"""

new_header_index = """                    <h2 class="notranslate" style="color: var(--accent-color); font-size: 3rem; margin-bottom: 5px; text-align: center; font-family: 'Oswald', sans-serif; text-transform: uppercase;">{{ evento.titulo_articulo }}</h2>
                    <h3 style="text-align: center; color: #fff; font-size: 1.5rem; margin-bottom: 10px;">{{ evento.nombre_evento }}</h3>
                    <p style="text-align: center; color: #888; font-size: 1.1rem; margin-bottom: 30px;">
                        <i class="fa-solid fa-location-dot"></i> {{ evento.ciudad }}, {{ evento.pais }} | <i class="fa-solid fa-calendar-days"></i> {{ evento.fecha_evento }}
                    </p>
                    <div style="text-align: center; margin-bottom: 30px;">
                        <img loading="lazy" src="{{ evento.img_video_path }}" style="width: 100%; max-width: 600px; height: auto; border-radius: 8px;">
                    </div>
                    
                    <div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 8px; margin-bottom: 30px; text-align: center; border-left: 3px solid var(--accent-color);">
                        <p style="margin: 0; color: #ccc; font-size: 1rem;"><strong><i class="fa-solid fa-bullhorn"></i> Presentado por:</strong> {{ evento.promotor }}</p>
                    </div>"""

content = content.replace(old_header_index, new_header_index)

with open("templates/index.html", "w") as f:
    f.write(content)


# 2. Update evento.html
with open("templates/evento.html", "r") as f:
    content_ev = f.read()

old_header_ev = """            <h2 class="notranslate" style="color: var(--accent-color); font-size: 2.5rem; margin-bottom: 5px; text-align: center; font-family: 'Oswald', sans-serif; text-transform: uppercase;">{{ evento.titulo_articulo }}</h2>
            <h3 style="text-align: center; color: #fff; font-size: 1.5rem; margin-bottom: 10px;">{{ evento.nombre_evento }}</h3>
            <p style="text-align: center; color: #888; font-size: 1.1rem; margin-bottom: 30px;">
                <i class="fa-solid fa-location-dot"></i> {{ evento.ciudad }}, {{ evento.pais }} | 
                <i class="fa-solid fa-calendar-days"></i> {{ evento.fecha_evento }}<br>
                <i class="fa-solid fa-bullhorn"></i> Promotor: {{ evento.promotor }}
            </p>

            <div style="text-align: center; margin-bottom: 30px;">
                <img loading="lazy" src="/{{ evento.img_video_path }}" style="width: 100%; max-width: 600px; height: auto; border-radius: 8px;">
            </div>"""

new_header_ev = """            <h2 class="notranslate" style="color: var(--accent-color); font-size: 3rem; margin-bottom: 5px; text-align: center; font-family: 'Oswald', sans-serif; text-transform: uppercase;">{{ evento.titulo_articulo }}</h2>
            <h3 style="text-align: center; color: #fff; font-size: 1.5rem; margin-bottom: 10px;">{{ evento.nombre_evento }}</h3>
            <p style="text-align: center; color: #888; font-size: 1.1rem; margin-bottom: 30px;">
                <i class="fa-solid fa-location-dot"></i> {{ evento.ciudad }}, {{ evento.pais }} | <i class="fa-solid fa-calendar-days"></i> {{ evento.fecha_evento }}
            </p>

            <div style="text-align: center; margin-bottom: 30px;">
                <img loading="lazy" src="/{{ evento.img_video_path }}" style="width: 100%; max-width: 600px; height: auto; border-radius: 8px;">
            </div>
            
            <div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 8px; margin-bottom: 30px; text-align: center; border-left: 3px solid var(--accent-color);">
                <p style="margin: 0; color: #ccc; font-size: 1rem;"><strong><i class="fa-solid fa-bullhorn"></i> Presentado por:</strong> {{ evento.promotor }}</p>
            </div>"""

content_ev = content_ev.replace(old_header_ev, new_header_ev)

with open("templates/evento.html", "w") as f:
    f.write(content_ev)

print("Style homologated successfully")
