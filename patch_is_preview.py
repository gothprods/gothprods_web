import re

with open("app.py", "r") as f:
    content = f.read()

# Update render_template calls to include is_preview=is_preview
content = content.replace("eventos_semana=eventos_semana)", "eventos_semana=eventos_semana, is_preview=is_preview)")
content = content.replace("render_template('banda.html', banda=banda, settings=settings)", "render_template('banda.html', banda=banda, settings=settings, is_preview=is_preview)")
content = content.replace("render_template('evento.html', evento=evento, settings=settings)", "render_template('evento.html', evento=evento, settings=settings, is_preview=is_preview)")
content = content.replace("render_template('articulo.html', item=item, settings=settings)", "render_template('articulo.html', item=item, settings=settings, is_preview=is_preview)")

with open("app.py", "w") as f:
    f.write(content)

print("app.py updated with is_preview")
