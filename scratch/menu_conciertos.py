import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Current dock structure from "Reseñas" to "Agenda"
dock_old = """            {% if settings.get('show_reviews', '1') == '1' %}
            <li class="dock-item" data-title="{{ settings.get('title_reviews', 'Reseñas de Conciertos') }}">
                <a href="#reviews"><img src="{{ settings.get('icon_reviews', '/assets/resenas_icon.png') }}" alt="{{ settings.get('title_reviews', 'Reseñas de Conciertos') }}" ><span class="dock-text">{{ settings.get('title_reviews', 'Reseñas de Conciertos') }}</span></a>
            </li>
            {% endif %}
            {% if settings.get('show_noticiero', '1') == '1' %}
            <li class="dock-item" data-title="{{ settings.get('title_news', 'El Noticiero Nocturno') }}">
                <a href="#news"><img src="{{ settings.get('icon_news', '/assets/noticiero_icon.png') }}" alt="{{ settings.get('title_news', 'El Noticiero Nocturno') }}" ><span class="dock-text">{{ settings.get('title_news', 'El Noticiero Nocturno') }}</span></a>
            </li>
            {% endif %}
            <li class="dock-item" data-title="{{ settings.get('title_agenda', 'Agenda Metalera') }}">
                <a href="#agenda"><img src="{{ settings.get('icon_agenda', '/assets/agenda_icon.png') }}" alt="{{ settings.get('title_agenda', 'Agenda Metalera') }}" ><span class="dock-text">{{ settings.get('title_agenda', 'Agenda Metalera') }}</span></a>
            </li>"""

dock_new = """            {% if settings.get('show_noticiero', '1') == '1' %}
            <li class="dock-item" data-title="{{ settings.get('title_news', 'El Noticiero Nocturno') }}">
                <a href="#news"><img src="{{ settings.get('icon_news', '/assets/noticiero_icon.png') }}" alt="{{ settings.get('title_news', 'El Noticiero Nocturno') }}" ><span class="dock-text">{{ settings.get('title_news', 'El Noticiero Nocturno') }}</span></a>
            </li>
            {% endif %}
            {% if settings.get('show_reviews', '1') == '1' or settings.get('show_agenda', '1') == '1' %}
            <li class="dock-item" data-title="Conciertos">
                <a href="#conciertos"><img src="{{ settings.get('icon_agenda', '/assets/agenda_icon.png') }}" alt="Conciertos"><span class="dock-text">Conciertos</span></a>
            </li>
            {% endif %}"""

content = content.replace(dock_old, dock_new)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Dock menu updated!")
