from app import app, get_db_connection
from flask import render_template
with app.app_context():
    conn = get_db_connection()
    all_items = conn.execute("SELECT id, section, title, short_desc, full_desc, yt_link, sp_link, ap_link, created_at FROM content_items WHERE section IN ('El Noticiero Nocturno', 'Reseñas de Conciertos', 'Metal Pulse Tracks') ORDER BY id DESC LIMIT 5").fetchall()
    todas_bandas = conn.execute("SELECT * FROM banda_semana ORDER BY id DESC LIMIT 5").fetchall()
    settings = {}
    html = render_template('admin_dashboard.html', all_items=all_items, todas_bandas=todas_bandas, settings=settings)
    for line in html.split('\n'):
        if 'onclick' in line and ('editRecord' in line or 'editBandaRecord' in line):
            print(line.strip()[:200])
