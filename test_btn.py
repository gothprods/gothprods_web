import sqlite3
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('admin_dashboard.html')

conn = sqlite3.connect('gothprods.db')
conn.row_factory = sqlite3.Row
all_items = conn.execute("SELECT id, section, title, short_desc, full_desc, yt_link, sp_link, ap_link, created_at FROM content_items WHERE section IN ('El Noticiero Nocturno', 'Reseñas de Conciertos', 'Metal Pulse Tracks') ORDER BY id DESC LIMIT 5").fetchall()
todas_bandas = conn.execute("SELECT * FROM banda_semana ORDER BY id DESC LIMIT 5").fetchall()
conn.close()

class DummySession:
    email = "test@test.com"

html = template.render(all_items=all_items, todas_bandas=todas_bandas, settings={}, session=DummySession())

for line in html.split('\n'):
    if 'onclick="editRecord' in line or 'onclick="editBandaRecord' in line:
        print(line.strip())
