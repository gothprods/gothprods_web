import re

with open("templates/index.html", "r") as f:
    content = f.read()

replacements = [
    (
        r'<li class="dock-item" data-title="Bandas y Eventos Destacados">.*?<img src="assets/destacados_icon\.png\?v=\d+".*?alt="Bandas y Eventos Destacados".*?><span class="dock-text">Bandas y Eventos Destacados</span></a>\s*</li>',
        """<li class="dock-item" data-title="{{ settings.get('title_destacados', 'Bandas y Eventos Destacados') }}">
                <a href="#banda-eventos-semana"><img src="{{ settings.get('icon_destacados', 'assets/destacados_icon.png') }}" alt="{{ settings.get('title_destacados', 'Bandas y Eventos Destacados') }}" style="width: 36px; height: 36px; object-fit: contain; background: #000; border: 1px solid rgba(113, 109, 74, 0.4); filter: drop-shadow(0 0 2px rgba(113, 109, 74, 0.5)); border-radius: 50%;"><span class="dock-text">{{ settings.get('title_destacados', 'Bandas y Eventos Destacados') }}</span></a>
            </li>"""
    ),
    (
        r'<li class="dock-item" data-title="El Pit">.*?<img src="assets/el_pit_icon\.png\?v=\d+".*?alt="El Pit".*?><span class="dock-text">El Pit</span></a>\s*</li>',
        """<li class="dock-item" data-title="{{ settings.get('title_el_pit', 'El Pit') }}">
                <a href="#highlights"><img src="{{ settings.get('icon_el_pit', 'assets/el_pit_icon.png') }}" alt="{{ settings.get('title_el_pit', 'El Pit') }}" style="width: 36px; height: 36px; object-fit: contain; background: #000; border: 1px solid rgba(113, 109, 74, 0.4); filter: drop-shadow(0 0 2px rgba(113, 109, 74, 0.5)); border-radius: 50%;"><span class="dock-text">{{ settings.get('title_el_pit', 'El Pit') }}</span></a>
            </li>"""
    ),
    (
        r'<li class="dock-item" data-title="La Galería Nocturna">.*?<img src="assets/galeria_nocturna_icon\.jpg".*?alt="La Galería Nocturna".*?><span class="dock-text">La Galería Nocturna</span></a>\s*</li>',
        """<li class="dock-item" data-title="{{ settings.get('title_galeria', 'La Galería Nocturna') }}">
                <a href="#shows"><img src="{{ settings.get('icon_galeria', 'assets/galeria_nocturna_icon.jpg') }}" alt="{{ settings.get('title_galeria', 'La Galería Nocturna') }}" style="width: 36px; height: 36px; object-fit: contain; background: #000; border: 1px solid rgba(113, 109, 74, 0.4); filter: drop-shadow(0 0 2px rgba(113, 109, 74, 0.5)); border-radius: 50%;"><span class="dock-text">{{ settings.get('title_galeria', 'La Galería Nocturna') }}</span></a>
            </li>"""
    ),
    (
        r'<li class="dock-item" data-title="Metal Pulse">.*?<img src="assets/metal_pulse_icon\.jpg".*?alt="Metal Pulse".*?><span class="dock-text">Metal Pulse</span></a>\s*</li>',
        """<li class="dock-item" data-title="{{ settings.get('title_metalpulse', 'Metal Pulse') }}">
                <a href="#metal-pulse"><img src="{{ settings.get('icon_metalpulse', 'assets/metal_pulse_icon.jpg') }}" alt="{{ settings.get('title_metalpulse', 'Metal Pulse') }}" style="width: 36px; height: 36px; object-fit: contain; background: #000; border: 1px solid rgba(113, 109, 74, 0.4); filter: drop-shadow(0 0 2px rgba(113, 109, 74, 0.5)); border-radius: 50%;"><span class="dock-text">{{ settings.get('title_metalpulse', 'Metal Pulse') }}</span></a>
            </li>"""
    ),
    (
        r'<li class="dock-item" data-title="Reseñas de Conciertos">.*?<img src="assets/resenas_icon\.png\?v=\d+".*?alt="Reseñas de Conciertos".*?><span class="dock-text">Reseñas de Conciertos</span></a>\s*</li>',
        """<li class="dock-item" data-title="{{ settings.get('title_reviews', 'Reseñas de Conciertos') }}">
                <a href="#reviews"><img src="{{ settings.get('icon_reviews', 'assets/resenas_icon.png') }}" alt="{{ settings.get('title_reviews', 'Reseñas de Conciertos') }}" style="width: 36px; height: 36px; object-fit: contain; background: #000; border: 1px solid rgba(113, 109, 74, 0.4); filter: drop-shadow(0 0 2px rgba(113, 109, 74, 0.5)); border-radius: 50%;"><span class="dock-text">{{ settings.get('title_reviews', 'Reseñas de Conciertos') }}</span></a>
            </li>"""
    ),
    (
        r'<li class="dock-item" data-title="El Noticiero Nocturno">.*?<img src="assets/noticiero_icon\.png\?v=\d+".*?alt="El Noticiero Nocturno".*?><span class="dock-text">El Noticiero Nocturno</span></a>\s*</li>',
        """<li class="dock-item" data-title="{{ settings.get('title_news', 'El Noticiero Nocturno') }}">
                <a href="#news"><img src="{{ settings.get('icon_news', 'assets/noticiero_icon.png') }}" alt="{{ settings.get('title_news', 'El Noticiero Nocturno') }}" style="width: 36px; height: 36px; object-fit: contain; background: #000; border: 1px solid rgba(113, 109, 74, 0.4); filter: drop-shadow(0 0 2px rgba(113, 109, 74, 0.5)); border-radius: 50%;"><span class="dock-text">{{ settings.get('title_news', 'El Noticiero Nocturno') }}</span></a>
            </li>"""
    ),
    (
        r'<li class="dock-item" data-title="Entrevistas Under">.*?<img src="assets/entrevistas_icon\.png\?v=\d+".*?alt="Entrevistas Under".*?><span class="dock-text">Entrevistas Under</span></a>\s*</li>',
        """<li class="dock-item" data-title="{{ settings.get('title_interviews', 'Entrevistas Under') }}">
                <a href="#under-interviews"><img src="{{ settings.get('icon_interviews', 'assets/entrevistas_icon.png') }}" alt="{{ settings.get('title_interviews', 'Entrevistas Under') }}" style="width: 36px; height: 36px; object-fit: contain; background: #000; border: 1px solid rgba(113, 109, 74, 0.4); filter: drop-shadow(0 0 2px rgba(113, 109, 74, 0.5)); border-radius: 50%;"><span class="dock-text">{{ settings.get('title_interviews', 'Entrevistas Under') }}</span></a>
            </li>"""
    ),
    (
        r'<li class="dock-item" data-title="Agenda Metalera">.*?<img src="assets/agenda_icon\.png\?v=\d+".*?alt="Agenda Metalera".*?><span class="dock-text">Agenda Metalera</span></a>\s*</li>',
        """<li class="dock-item" data-title="{{ settings.get('title_agenda', 'Agenda Metalera') }}">
                <a href="#agenda"><img src="{{ settings.get('icon_agenda', 'assets/agenda_icon.png') }}" alt="{{ settings.get('title_agenda', 'Agenda Metalera') }}" style="width: 36px; height: 36px; object-fit: contain; background: #000; border: 1px solid rgba(113, 109, 74, 0.4); filter: drop-shadow(0 0 2px rgba(113, 109, 74, 0.5)); border-radius: 50%;"><span class="dock-text">{{ settings.get('title_agenda', 'Agenda Metalera') }}</span></a>
            </li>"""
    ),
    (
        r'<li class="dock-item" data-title="Contáctanos">.*?<img src="assets/contacto_icon\.png\?v=\d+".*?alt="Contáctanos".*?><span class="dock-text">Contáctanos</span></a>\s*</li>',
        """<li class="dock-item" data-title="{{ settings.get('title_contacto', 'Contáctanos') }}">
                <a href="mailto:contacto@gothprods.com"><img src="{{ settings.get('icon_contacto', 'assets/contacto_icon.png') }}" alt="{{ settings.get('title_contacto', 'Contáctanos') }}" style="width: 36px; height: 36px; object-fit: contain; background: #000; border: 1px solid rgba(113, 109, 74, 0.4); filter: drop-shadow(0 0 2px rgba(113, 109, 74, 0.5)); border-radius: 50%;"><span class="dock-text">{{ settings.get('title_contacto', 'Contáctanos') }}</span></a>
            </li>"""
    )
]

for pat, repl in replacements:
    content = re.sub(pat, repl, content, flags=re.DOTALL)

with open("templates/index.html", "w") as f:
    f.write(content)

print("index.html patched.")
