with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    "{% if settings.get('show_servicios', '1') == '1' %}\n        <section id=\"servicios\"",
    "{% if settings.get('show_servicios', '1') == '1' and servicios_items %}\n        <section id=\"servicios\""
)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("done")
