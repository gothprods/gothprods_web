import sqlite3
import csv
import io
import re

data = """Evento,Ciudad,Venue,Fecha,GP
Tankard,CDMX,Foro Alicia,1 de mayo,N
Beyond Creation y Felluja,CDMX,Circo Volador,3 de mayo,N
Vader,CDMX,Foro Alicia,3 de mayo,N
In Flames,CDMX,Circo Volador,2 de Mayo,N
Megadeth,Monterrey,Arena Monterrey,8 de Mayo,Y
Megadeth,CDMX,Arena Ciudad de México,10 y 11 de Mayo,N
Megadetn,Guadalajara,Arena Guadalajara,13 de Mayo,N
Gutalax,CDMX,Foro 28,16 de mayo,N
Dogma,CDMX,Circo Volador,16 de Mayo,N
San Luis Metal Fest,San Luis Potosi,Teatro del Pueblo de la Feria Nacional Potosina (FENAPO),16 y 17 de mayo,N
Korn,CDMX,Palacio de los Deportes,19 de mayo - Funado,N
Metallica - Gojira y Knocked Loose,Frankfurt,Deutsche Bank Park,22 de mayo,Y
Metallica - Pantera y Avatar,Frankfurt,Deutsche Bank Park,24 de mayo,Y
System Of A Down,CDMX,Estadio GNP Seguros,27 y 28 de mayo,Y
Turilli / Lione Rhapsody,CDMX,Pepsi Center,6 de junio,N
Rush,CDMX,Palacio de los Deportes,18 y 20 de junio,N
Havok,CDMX,F*ck off Room,3 de Julio,Y
Lacrimosa,CDMX,Arena Ciudad de México,22 y 23 de agosto,N
Helloween,CDMX,Arena Ciudad de México,29 de agosto,N
Ladrones,CDMX,Pabellon Oeste,29 de Agosto,Y
Candelabrum Metal Fest V,Leon,La Velaria de la Feria,12 y 13 de septiembre,Y
Sonata Arctica,CDMX,"Foro Teambro Ciudad de México, CDMX",14 de septiembre,N
Iron Maiden,San Antonio,Alamo Dome,29 de Septiembre,Y
AfterShock - Putero de Bandas,Sacramento,Discovery Park,"1,2,3 y 4 de octubre",Y
Amorphis,CDMX,Circo Volador,1 de Octubre,N
Iron Maiden / Anthrax,CDMX,Estadio GNP Seguros,2 de octubre,Y
Between The Buried and Me,CDMX,Circo Volador,8 de Octubre,Y
Six Feet Under,CDMX,Circo Volador,15 de Octubre,N
Obscura,CDMX,Foro 28,16 de Octubre,N
Fit For a King,CDMX,Circo Volador,16 de Octubre,N
Metallica,Las Vegas,The Sphere,5 y 7 de Noviembre,Y
Opeth,CDMX,Arena Ciudad de México,11 de noviembre,N
ZZtop,CDMX,Auditorio Nacional,11 de noviembre,N
"Knotfest - Bad Omens, Lamb of God, Poppy, The Ghost Inside, Blood Incantation, Sylosis, Vana, y Versailles",CDMX,Estadio Fray Nano - Cdmx,5 de diciembre,Y
Babymetal,CDMX,Estadio Fray Nano - Cdmx,12 de diciembre,N
Deep Purple,CDMX,Estadio Fray Nano - Cdmx,19 de diciembre,Y
Heavy Metal X'Mas 2026 - Fear Factory,CDMX,Circo Volador,19 de diciembre,N"""

months_map = {
    'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
}

conn = sqlite3.connect('gothprods.db')
c = conn.cursor()

# Remove old agenda
c.execute("DELETE FROM content_items WHERE section = 'Agenda Metalera'")

reader = csv.DictReader(io.StringIO(data))
for row in reader:
    evento = row['Evento'].strip()
    ciudad = row['Ciudad'].strip()
    venue = row['Venue'].strip()
    fecha_raw = row['Fecha'].strip()
    gp = row['GP'].strip()
    
    # Extract month and day for sorting
    # e.g., "16 y 17 de mayo" -> month=5, day=16
    month = 12
    for m_name, m_num in months_map.items():
        if m_name in fecha_raw.lower():
            month = m_num
            break
            
    day_match = re.search(r'\d+', fecha_raw)
    day = int(day_match.group(0)) if day_match else 1
    
    # We will store the sortable date in `created_at` or a new field.
    # Let's use `author` to store a sortable string like "2026-05-16"
    sort_date = f"2026-{month:02d}-{day:02d}"
    
    # Construct logo path (just a guess, html will handle error)
    logo_filename = f"assets/logos/{evento.lower().replace(' ', '').replace('/', '')}.png"
    
    # We map:
    # title = Evento
    # short_desc = Ciudad + Venue
    # full_desc = Fecha Raw
    # image_filename = logo path
    # yt_link = GP (Y/N)
    # author = sortable date
    
    c.execute('''
        INSERT INTO content_items (section, title, short_desc, full_desc, image_filename, yt_link, author)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', ("Agenda Metalera", evento, f"{venue} | {ciudad}", fecha_raw, logo_filename, gp, sort_date))

conn.commit()
conn.close()
