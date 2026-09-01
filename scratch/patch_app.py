import sqlite3
import re

with open('app.py', 'r') as f:
    content = f.read()

old_query = """    # 6. Metal Pulse Tracks (Filtrado por mes objetivo)
    pulse_tracks = conn.execute("SELECT * FROM content_items WHERE section = 'Metal Pulse Tracks' AND (full_desc LIKE ? OR full_desc LIKE ?) ORDER BY id DESC", (f"%{month_name}%", f"%{target_month}%")).fetchall()"""

new_query = """    # 6. Metal Pulse Tracks (Tomar la lista activa en la pagina)
    all_tracks = conn.execute("SELECT * FROM content_items WHERE section = 'Metal Pulse Tracks' AND full_desc != '.' ORDER BY id DESC").fetchall()
    settings_rows = conn.execute('SELECT key, value FROM settings').fetchall()
    settings = {row['key']: row['value'] for row in settings_rows}
    hide_past_mp = settings.get('hide_past_metalpulse', '0') == '1'
    if hide_past_mp and all_tracks:
        months_es = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        cur_year = now_mx.year
        cur_month_idx = now_mx.month - 1
        valid_months = set()
        for i in range(24):
            m_idx = (cur_month_idx + i) % 12
            y_i = cur_year + (cur_month_idx + i) // 12
            valid_months.add(f"{months_es[m_idx]} {y_i}")
        filtered = [t for t in all_tracks if t['full_desc'] in valid_months]
        if filtered:
            pulse_tracks = filtered
        else:
            latest_month = all_tracks[0]['full_desc']
            pulse_tracks = [t for t in all_tracks if t['full_desc'] == latest_month]
    else:
        pulse_tracks = all_tracks"""

content = content.replace(old_query, new_query)

with open('app.py', 'w') as f:
    f.write(content)
print("Patched app.py!")
