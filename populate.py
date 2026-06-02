import sqlite3

def init_db_data():
    conn = sqlite3.connect('gothprods.db')
    c = conn.cursor()
    
    # 1. Reseñas
    reviews = [
        ("Reseñas de Conciertos", "BRUTAL CORONACIÓN DE ARCHITECTS EN EL VELÓDROMO", "La oscuridad capitalina fue testigo de una liturgia brutal donde el asfalto retumbó...", "assets/architects_review.jpg"),
        ("Reseñas de Conciertos", "EL REGRESO DE DREAM THEATER A MÉXICO", "Los titanes indiscutibles del metal progresivo nos volaron el cráneo...", "assets/dream_theater_horizontal.jpg"),
        ("Reseñas de Conciertos", "EL ÚLTIMO TRUENO DE AC/DC", "Una auténtica exhumación del viejo, puro y crudo heavy metal...", "assets/acdc_review.jpg")
    ]
    
    # 2. Entrevistas
    interviews = [
        ("Entrevistas Under", "Ominum", "This Galeria Nocturna episode explores the history and discography of Ominum...", "https://img.youtube.com/vi/ZxZ2Uht40bA/maxresdefault.jpg"),
        ("Entrevistas Under", "Athica", "Nos adentramos en la historia de Athica, poderosa banda de metal originaria de Panamá...", "https://img.youtube.com/vi/RjHD5Jtx4sM/maxresdefault.jpg"),
        ("Entrevistas Under", "Stay Design", "Conversamos sobre los hitos que han definido su carrera, destacando su histórica participación...", "https://img.youtube.com/vi/G4Z3MhWUzdA/maxresdefault.jpg")
    ]
    
    # 3. Agenda
    # Note: Agenda has specific fields. Let's map it roughly to content_items.
    # We can use 'short_desc' for the venue/date, and 'author' for the exact date.
    agenda = [
        ("Agenda Metalera", "Megadeth", "Arena CDMX", "assets/logos/megadeth.png", "2026-05-10"),
        ("Agenda Metalera", "San Luís Metal Fest", "San Luís Potosí", "assets/viking.jpg", "2026-05-16"),
        ("Agenda Metalera", "Metallica (Gojira)", "Estadio GNP", "assets/logos/metallica.png", "2026-05-22")
    ]
    
    for r in reviews:
        c.execute("INSERT INTO content_items (section, title, short_desc, image_filename) VALUES (?, ?, ?, ?)", r)
        
    for i in interviews:
        c.execute("INSERT INTO content_items (section, title, short_desc, image_filename) VALUES (?, ?, ?, ?)", i)
        
    for a in agenda:
        c.execute("INSERT INTO content_items (section, title, short_desc, image_filename, full_desc) VALUES (?, ?, ?, ?, ?)", (a[0], a[1], a[2], a[3], a[4]))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db_data()
    print("Database populated with legacy items.")
