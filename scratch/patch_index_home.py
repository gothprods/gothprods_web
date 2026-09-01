with open('templates/index.html', 'r') as f:
    content = f.read()

old_logo = '<a href="#home"><img src="/assets/dock_header_icon.png" alt="Goth Prods Logo" class="logo-img"></a>'
new_logo = '<a href="#home"><img src="{{ settings.get(\'icon_home\', \'/assets/dock_header_icon.png\') }}" alt="Goth Prods Logo" class="logo-img"></a>'

content = content.replace(old_logo, new_logo)

with open('templates/index.html', 'w') as f:
    f.write(content)
