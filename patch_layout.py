import re

with open("templates/index.html", "r") as f:
    content = f.read()

# 1. Change the flex wrapper from side-by-side to stacked
old_wrapper = """        <section id="banda-eventos-semana" class="section highlights-section" style="background: linear-gradient(to right, #111, #000); border-bottom: 2px solid var(--accent-color); padding: 3.5rem 5%;">
            <div style="display: flex; flex-wrap: wrap; gap: 40px;">"""
new_wrapper = """        <section id="banda-eventos-semana" class="section highlights-section" style="background: linear-gradient(to right, #111, #000); border-bottom: 2px solid var(--accent-color); padding: 3.5rem 5%;">
            <div style="display: flex; flex-direction: column; gap: 60px;">"""

content = content.replace(old_wrapper, new_wrapper)

# 2. Re-structure the Evento slide to match Banda slide (image left, info right)
old_evento_slide = """                    <div class="evento-slide fade" style="animation: fadeEffect 1s; {% if loop.index != 1 %}display: none;{% endif %}">
                        <div style="display: flex; flex-direction: column; gap: 15px;">
                            <div style="max-width: 400px; margin: 0 auto; width: 100%;">
                                <img loading="lazy" src="{{ evento.img_video_path }}" alt="{{ evento.nombre_evento }}" style="width: 100%; height: auto; border-radius: 12px; box-shadow: 0 10px 20px rgba(0,0,0,0.8);">
                            </div>
                            <h3 class="notranslate" style="font-size: 1.8rem; color: var(--accent-color); margin-bottom: 0px; font-family: 'Oswald', sans-serif; text-transform: uppercase;">{{ evento.titulo_articulo }}</h3>
                            <p style="font-size: 1.2rem; color: #fff; font-weight: bold; margin-bottom: 5px;">{{ evento.nombre_evento }}</p>
                            <p style="font-size: 0.95rem; color: #888; margin-bottom: 10px;"><i class="fa-solid fa-calendar-day"></i> {{ evento.fecha_evento }} | <i class="fa-solid fa-location-dot"></i> {{ evento.ciudad }}, {{ evento.pais }}</p>
                            <div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 8px; border: 1px solid #333;">
                                <p style="font-size: 0.95rem; line-height: 1.4; margin-bottom: 15px; color: #ccc;">{{ evento.bio_corta }}</p>
                                <button onclick="openEventoModal({{ evento.id }})" style="background: transparent; color: var(--accent-color); border: 1px solid var(--accent-color); padding: 5px 12px; font-size: 0.85rem; border-radius: 4px; cursor: pointer; text-transform: uppercase; font-family: 'Oswald', sans-serif; letter-spacing: 1px; transition: all 0.3s;"><i class="fa-solid fa-book-open"></i> Leer más</button>
                            </div>
                        </div>
                    </div>"""

new_evento_slide = """                    <div class="evento-slide fade" style="animation: fadeEffect 1s; {% if loop.index != 1 %}display: none;{% endif %}">
                        <div class="grid-container" style="display: flex; flex-wrap: wrap; align-items: center; gap: 20px;">
                            <div style="flex: 1; min-width: 300px; max-width: 400px; margin: 0 auto;">
                                <img loading="lazy" src="{{ evento.img_video_path }}" alt="{{ evento.nombre_evento }}" style="width: 100%; height: auto; border-radius: 12px; box-shadow: 0 10px 20px rgba(0,0,0,0.8);">
                            </div>
                            <div style="flex: 1; min-width: 300px; color: #ddd;">
                                <h3 class="notranslate" style="font-size: 2rem; color: var(--accent-color); margin-bottom: 0px; font-family: 'Oswald', sans-serif; text-transform: uppercase;">{{ evento.titulo_articulo }}</h3>
                                <p style="font-size: 1.2rem; color: #fff; font-weight: bold; margin-bottom: 5px;">{{ evento.nombre_evento }}</p>
                                <p style="font-size: 1rem; color: #888; margin-bottom: 10px;"><i class="fa-solid fa-calendar-day"></i> {{ evento.fecha_evento }} | <i class="fa-solid fa-location-dot"></i> {{ evento.ciudad }}, {{ evento.pais }}</p>
                                <div style="display: grid; grid-template-columns: 1fr; gap: 20px; margin-top: 15px; background: rgba(0,0,0,0.3); padding: 20px; border-radius: 8px; border: 1px solid #333;">
                                    <div>
                                        <h4 style="color: var(--accent-color); font-family: 'Oswald', sans-serif; font-size: 1.1rem; text-transform: uppercase; margin-bottom: 10px; border-bottom: 1px solid #444; padding-bottom: 5px;"><i class="fa-solid fa-align-left"></i> Resumen</h4>
                                        <p style="font-size: 0.95rem; line-height: 1.4; margin-bottom: 15px; color: #ccc;">{{ evento.bio_corta }}</p>
                                        <button onclick="openEventoModal({{ evento.id }})" style="background: transparent; color: var(--accent-color); border: 1px solid var(--accent-color); padding: 5px 12px; font-size: 0.85rem; border-radius: 4px; cursor: pointer; text-transform: uppercase; font-family: 'Oswald', sans-serif; letter-spacing: 1px; transition: all 0.3s;"><i class="fa-solid fa-book-open"></i> Leer más del evento</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>"""

content = content.replace(old_evento_slide, new_evento_slide)

with open("templates/index.html", "w") as f:
    f.write(content)

print("Layout updated!")
