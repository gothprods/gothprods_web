with open('app.py', 'r') as f:
    content = f.read()

content = content.replace('t.get("sp_link")', 't["sp_link"]')
content = content.replace('b.get("titulo_resena")', 'b["titulo_resena"]')
content = content.replace('e.get("titulo_articulo")', 'e["titulo_articulo"]')
content = content.replace("e.get('titulo_articulo')", "e['titulo_articulo']")

with open('app.py', 'w') as f:
    f.write(content)
