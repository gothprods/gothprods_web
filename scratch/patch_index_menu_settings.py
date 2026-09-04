with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Podcasts
old_podcasts = """            {% if settings.get('show_galeria_nocturna', '1') == '1' or settings.get('show_metalpulse', '1') == '1' or settings.get('show_entrevistas', '1') == '1' %}
            <li class="dock-item" data-title="Nuestros Podcasts">
                <a href="#nuestros-podcasts">
                    <img src="{{ settings.get('icon_interviews', '/assets/entrevistas_icon.png') }}" alt="Nuestros Podcasts">
                    <span class="dock-text">Nuestros Podcasts</span>
                </a>
            </li>
            {% endif %}"""

new_podcasts = """            {% if settings.get('show_galeria_nocturna', '1') == '1' or settings.get('show_metalpulse', '1') == '1' or settings.get('show_interviews', '1') == '1' %}
            <li class="dock-item" data-title="{{ settings.get('title_podcasts', 'Nuestros Podcasts') }}">
                <a href="#nuestros-podcasts">
                    <img src="{{ settings.get('icon_podcasts', settings.get('icon_interviews', '/assets/entrevistas_icon.png')) }}" alt="{{ settings.get('title_podcasts', 'Nuestros Podcasts') }}">
                    <span class="dock-text">{{ settings.get('title_podcasts', 'Nuestros Podcasts') }}</span>
                </a>
            </li>
            {% endif %}"""
content = content.replace(old_podcasts, new_podcasts)

# 2. Conciertos
old_conciertos = """            {% if settings.get('show_reviews', '1') == '1' or settings.get('show_agenda', '1') == '1' %}
            <li class="dock-item" data-title="Conciertos">
                <a href="#conciertos"><img src="{{ settings.get('icon_agenda', '/assets/agenda_icon.png') }}" alt="Conciertos"><span class="dock-text">Conciertos</span></a>
            </li>
            {% endif %}"""

new_conciertos = """            {% if settings.get('show_reviews', '1') == '1' or settings.get('show_agenda', '1') == '1' %}
            <li class="dock-item" data-title="{{ settings.get('title_conciertos', 'Conciertos') }}">
                <a href="#conciertos">
                    <img src="{{ settings.get('icon_conciertos', settings.get('icon_agenda', '/assets/agenda_icon.png')) }}" alt="{{ settings.get('title_conciertos', 'Conciertos') }}">
                    <span class="dock-text">{{ settings.get('title_conciertos', 'Conciertos') }}</span>
                </a>
            </li>
            {% endif %}"""
content = content.replace(old_conciertos, new_conciertos)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("index.html menu settings updated")
