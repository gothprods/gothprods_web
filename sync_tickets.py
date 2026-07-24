import csv
import sqlite3
import re

def sync():
    conn = sqlite3.connect('gothprods.db')
    c = conn.cursor()
    
    with open('sheet.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        for row in reader:
            if len(row) < 5: continue
            evento = row[0].strip()
            ciudad = row[1].strip()
            # Clean up newlines or extra quotes that might be around the event name
            evento = evento.replace('\n', ' ')
            evento = re.sub(r'^"|"$', '', evento).strip()
            
            tickets = row[4].strip()
            
            if not tickets:
                continue
                
            db_items = c.execute("SELECT id, short_desc FROM content_items WHERE section = 'Agenda Metalera' AND title LIKE ?", ('%' + evento + '%',)).fetchall()
            
            for item_id, short_desc in db_items:
                if not ciudad or ciudad.lower() in short_desc.lower() or 'cdmx' in ciudad.lower() and 'cdmx' in short_desc.lower() or 'cdxm' in ciudad.lower() and 'cdmx' in short_desc.lower():
                    c.execute("UPDATE content_items SET sp_link = ? WHERE id = ?", (tickets, item_id))
                    print(f"Updated: {evento} | {ciudad} -> {tickets}")
                    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    sync()
