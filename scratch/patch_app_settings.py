import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# ADD GETTERS
old_getters = """    title_agenda = request.form.get('title_agenda')
    title_contacto = request.form.get('title_contacto')
    agenda_desc = request.form.get('agenda_desc')
    
    title_equipo = request.form.get('title_equipo')
    show_equipo_menu = request.form.get('show_equipo_menu', '0')"""

new_getters = """    title_agenda = request.form.get('title_agenda')
    title_contacto = request.form.get('title_contacto')
    agenda_desc = request.form.get('agenda_desc')
    
    title_equipo = request.form.get('title_equipo')
    show_equipo_menu = request.form.get('show_equipo_menu', '0')
    
    show_servicios = request.form.get('show_servicios', '0')
    title_servicios = request.form.get('title_servicios')
    title_podcasts = request.form.get('title_podcasts')
    title_conciertos = request.form.get('title_conciertos')"""

content = content.replace(old_getters, new_getters)

# ADD QUERIES
old_queries = """        ("INSERT OR REPLACE INTO settings (key, value) VALUES ('show_el_equipo', ?)", (show_el_equipo,)),
        ("INSERT OR REPLACE INTO settings (key, value) VALUES ('title_equipo', ?)", (title_equipo,)),
        ("INSERT OR REPLACE INTO settings (key, value) VALUES ('show_equipo_menu', ?)", (show_equipo_menu,)),
    ]"""

new_queries = """        ("INSERT OR REPLACE INTO settings (key, value) VALUES ('show_el_equipo', ?)", (show_el_equipo,)),
        ("INSERT OR REPLACE INTO settings (key, value) VALUES ('title_equipo', ?)", (title_equipo,)),
        ("INSERT OR REPLACE INTO settings (key, value) VALUES ('show_equipo_menu', ?)", (show_equipo_menu,)),
        ("INSERT OR REPLACE INTO settings (key, value) VALUES ('show_servicios', ?)", (show_servicios,)),
        ("INSERT OR REPLACE INTO settings (key, value) VALUES ('title_servicios', ?)", (title_servicios,)),
        ("INSERT OR REPLACE INTO settings (key, value) VALUES ('title_podcasts', ?)", (title_podcasts,)),
        ("INSERT OR REPLACE INTO settings (key, value) VALUES ('title_conciertos', ?)", (title_conciertos,)),
    ]"""

content = content.replace(old_queries, new_queries)

# ADD FILES
old_files = """    for icon_field in ['icon_destacados', 'icon_el_pit', 'icon_galeria', 'icon_metalpulse', 'icon_reviews', 'icon_news', 'icon_interviews', 'icon_agenda', 'icon_contacto', 'icon_equipo']:"""

new_files = """    for icon_field in ['icon_destacados', 'icon_el_pit', 'icon_galeria', 'icon_metalpulse', 'icon_reviews', 'icon_news', 'icon_interviews', 'icon_agenda', 'icon_contacto', 'icon_equipo', 'icon_servicios', 'icon_podcasts', 'icon_conciertos']:"""

content = content.replace(old_files, new_files)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("app.py settings updated!")
