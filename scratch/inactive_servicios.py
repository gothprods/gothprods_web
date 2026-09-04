with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_link = '<a href="#servicios"><img src="{{ settings.get(\'icon_servicios\', \'updates/servicios_icon.jpg\') }}" alt="{{ settings.get(\'title_servicios\', \'Servicios\') }}" ><span class="dock-text">{{ settings.get(\'title_servicios\', \'Servicios\') }}</span></a>'
new_link = '<a href="#servicios" style="opacity: 0.3; pointer-events: none; filter: grayscale(100%);"><img src="{{ settings.get(\'icon_servicios\', \'updates/servicios_icon.jpg\') }}" alt="{{ settings.get(\'title_servicios\', \'Servicios\') }}" ><span class="dock-text">{{ settings.get(\'title_servicios\', \'Servicios\') }}</span></a>'

content = content.replace(old_link, new_link)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Servicios icon set to inactive")
