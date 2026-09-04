with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'position: relative;"{% endif %}">',
    'position: relative;"{% endif %}>'
)

content = content.replace(
    'cancelled-event{% endif %}" {% if is_cancelled %}style="opacity: 0.7; filter: grayscale(80%); position: relative;"{% endif %}>',
    'cancelled-event{% endif %}" {% if is_cancelled %}style="opacity: 0.7; filter: grayscale(80%); position: relative;"{% endif %}>'
)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed quotes")
