import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Radar del Caos Dock Item
radar_old = """            {% if settings.get('show_banda_semana', '1') == '1' %}
            <li class="dock-item" data-title="{{ settings.get('title_destacados', 'Radar del Caos') }}">
                <a href="#radar-del-caos"><img src="{{ settings.get('icon_destacados', '/assets/destacados_icon.png') }}" alt="{{ settings.get('title_destacados', 'Radar del Caos') }}" ><span class="dock-text">{{ settings.get('title_destacados', 'Radar del Caos') }}</span></a>
            </li>
            {% endif %}"""

radar_new = """            {% set has_radar = (bandas_semana or eventos_semana) %}
            {% if settings.get('show_banda_semana', '1') == '1' %}
            <li class="dock-item" data-title="{{ settings.get('title_destacados', 'Radar del Caos') }}">
                <a href="#radar-del-caos" style="{{ '' if has_radar else 'opacity: 0.3; pointer-events: none; filter: grayscale(100%);' }}">
                    <img src="{{ settings.get('icon_destacados', '/assets/destacados_icon.png') }}" alt="{{ settings.get('title_destacados', 'Radar del Caos') }}">
                    <span class="dock-text">{{ settings.get('title_destacados', 'Radar del Caos') }}</span>
                </a>
            </li>
            {% endif %}"""

content = content.replace(radar_old, radar_new)

# 2. Update Podcasts Dock Items
podcasts_old = """            {% if settings.get('show_galeria_nocturna', '1') == '1' %}
            <li class="dock-item" data-title="{{ settings.get('title_galeria', 'La Galería Nocturna') }}">
                <a href="#shows"><img src="{{ settings.get('icon_galeria', '/assets/galeria_nocturna_icon.jpg') }}" alt="{{ settings.get('title_galeria', 'La Galería Nocturna') }}" ><span class="dock-text">{{ settings.get('title_galeria', 'La Galería Nocturna') }}</span></a>
            </li>
            {% endif %}
            {% if settings.get('show_metalpulse', '1') == '1' %}
            <li class="dock-item" data-title="{{ settings.get('title_metalpulse', 'Metal Pulse') }}">
                <a href="#metal-pulse"><img src="{{ settings.get('icon_metalpulse', '/assets/metal_pulse_icon.jpg') }}" alt="{{ settings.get('title_metalpulse', 'Metal Pulse') }}" ><span class="dock-text">{{ settings.get('title_metalpulse', 'Metal Pulse') }}</span></a>
            </li>
            {% endif %}
            {% if settings.get('show_reviews', '1') == '1' %}
            <li class="dock-item" data-title="{{ settings.get('title_reviews', 'Reseñas de Conciertos') }}">
                <a href="#reviews"><img src="{{ settings.get('icon_reviews', '/assets/resenas_icon.png') }}" alt="{{ settings.get('title_reviews', 'Reseñas de Conciertos') }}" ><span class="dock-text">{{ settings.get('title_reviews', 'Reseñas de Conciertos') }}</span></a>
            </li>
            {% endif %}
            {% if settings.get('show_noticiero', '1') == '1' %}
            <li class="dock-item" data-title="{{ settings.get('title_news', 'El Noticiero Nocturno') }}">
                <a href="#news"><img src="{{ settings.get('icon_news', '/assets/noticiero_icon.png') }}" alt="{{ settings.get('title_news', 'El Noticiero Nocturno') }}" ><span class="dock-text">{{ settings.get('title_news', 'El Noticiero Nocturno') }}</span></a>
            </li>
            {% endif %}
            {% if settings.get('show_entrevistas', '1') == '1' %}
            <li class="dock-item" data-title="{{ settings.get('title_interviews', 'Entrevistas Under') }}">
                <a href="#under-interviews"><img src="{{ settings.get('icon_interviews', '/assets/entrevistas_icon.png') }}" alt="{{ settings.get('title_interviews', 'Entrevistas Under') }}" ><span class="dock-text">{{ settings.get('title_interviews', 'Entrevistas Under') }}</span></a>
            </li>
            {% endif %}"""

# Debo quitar Galeria, Metal Pulse, Entrevistas y poner "Nuestros Podcasts".
# PERO ATENCIÓN, "Reseñas" y "Noticiero" no son podcasts, deben quedarse donde están en el menú, así que debo reemplazarlos con cuidado.

content = content.replace(podcasts_old, """            {% if settings.get('show_galeria_nocturna', '1') == '1' or settings.get('show_metalpulse', '1') == '1' or settings.get('show_entrevistas', '1') == '1' %}
            <li class="dock-item" data-title="Nuestros Podcasts">
                <a href="#nuestros-podcasts">
                    <img src="{{ settings.get('icon_interviews', '/assets/entrevistas_icon.png') }}" alt="Nuestros Podcasts">
                    <span class="dock-text">Nuestros Podcasts</span>
                </a>
            </li>
            {% endif %}
            {% if settings.get('show_reviews', '1') == '1' %}
            <li class="dock-item" data-title="{{ settings.get('title_reviews', 'Reseñas de Conciertos') }}">
                <a href="#reviews"><img src="{{ settings.get('icon_reviews', '/assets/resenas_icon.png') }}" alt="{{ settings.get('title_reviews', 'Reseñas de Conciertos') }}" ><span class="dock-text">{{ settings.get('title_reviews', 'Reseñas de Conciertos') }}</span></a>
            </li>
            {% endif %}
            {% if settings.get('show_noticiero', '1') == '1' %}
            <li class="dock-item" data-title="{{ settings.get('title_news', 'El Noticiero Nocturno') }}">
                <a href="#news"><img src="{{ settings.get('icon_news', '/assets/noticiero_icon.png') }}" alt="{{ settings.get('title_news', 'El Noticiero Nocturno') }}" ><span class="dock-text">{{ settings.get('title_news', 'El Noticiero Nocturno') }}</span></a>
            </li>
            {% endif %}""")

# 3. Insert <div id="nuestros-podcasts"></div> just before <section id="shows">
shows_section = """        {% if settings.get('show_galeria_nocturna', '1') == '1' %}
        <section id="shows" class="section shows-section">"""
        
new_shows_section = """        <div id="nuestros-podcasts" style="scroll-margin-top: 100px;"></div>
        {% if settings.get('show_galeria_nocturna', '1') == '1' %}
        <section id="shows" class="section shows-section">"""

content = content.replace(shows_section, new_shows_section)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Menu replaced.")
