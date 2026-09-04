with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_dock = """            {% if settings.get('show_equipo_menu', '0') == '1' %}
            <li class="dock-item" data-title="{{ settings.get('title_equipo', 'El Equipo, La Historia') }}">
                <a href="#equipo"><img src="{{ settings.get('icon_equipo', '/assets/equipo_icon.png') }}" alt="{{ settings.get('title_equipo', 'El Equipo, La Historia') }}" ><span class="dock-text">{{ settings.get('title_equipo', 'El Equipo, La Historia') }}</span></a>
            </li>
            {% endif %}
            <li class="dock-item" data-title="{{ settings.get('title_contacto', 'Contáctanos') }}">"""

new_dock = """            {% if settings.get('show_equipo_menu', '0') == '1' %}
            <li class="dock-item" data-title="{{ settings.get('title_equipo', 'El Equipo, La Historia') }}">
                <a href="#equipo"><img src="{{ settings.get('icon_equipo', '/assets/equipo_icon.png') }}" alt="{{ settings.get('title_equipo', 'El Equipo, La Historia') }}" ><span class="dock-text">{{ settings.get('title_equipo', 'El Equipo, La Historia') }}</span></a>
            </li>
            {% endif %}
            {% if settings.get('show_servicios', '1') == '1' %}
            <li class="dock-item" data-title="{{ settings.get('title_servicios', 'Servicios') }}">
                <a href="#servicios"><img src="{{ settings.get('icon_servicios', 'updates/servicios_icon.jpg') }}" alt="{{ settings.get('title_servicios', 'Servicios') }}" ><span class="dock-text">{{ settings.get('title_servicios', 'Servicios') }}</span></a>
            </li>
            {% endif %}
            <li class="dock-item" data-title="{{ settings.get('title_contacto', 'Contáctanos') }}">"""

content = content.replace(old_dock, new_dock)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Servicios added to dock")
