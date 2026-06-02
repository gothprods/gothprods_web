import sqlite3

def add_missing_legacy():
    conn = sqlite3.connect('gothprods.db')
    c = conn.cursor()

    # 1. Noticiero Nocturno Missing Items
    news = [
        ("El Noticiero Nocturno", "LOS VENUES FAVORITOS EN US: SPHERE Y ALLEGIANT STADIUM", "Recientemente, la revista Billboard ha posicionado a estos dos recintos de Las Vegas en la cima absoluta del éxito global...", "assets/reload_2.jpg"), # fallback image since it was in updates
        ("El Noticiero Nocturno", "¡METALLICA ANUNCIA EL ÉPICO BOX SET REMASTERIZADO DE 'RELOAD'!", "Metallica ha confirmado el lanzamiento de la edición definitiva y remasterizada de su séptimo álbum...", "assets/reload_2.jpg"),
        ("El Noticiero Nocturno", "¡ACTUALIZACIÓN EN LA BATALLA LEGAL: DIMEBAG DARRELL VS. DEAN GUITARS!", "La larga disputa legal sobre el legado de una de las leyendas más grandes del metal ha tomado un giro decisivo...", "assets/dimebag_dean.jpg"),
        ("El Noticiero Nocturno", "¡EL INVIERNO ETERNO REGRESA!", "La espera en los reinos de Blashyrkh está por terminar con el 11º álbum de Immortal...", "assets/Immortal_New_Album.png"),
        ("El Noticiero Nocturno", "¡EL BAÚL DE SABBATH SE ABRE DE NUEVO!", "Sharon Osbourne y el antiguo manager llegan a un acuerdo por los demos originales...", "assets/Black_Sabbath_Archives.png"),
        ("El Noticiero Nocturno", "EL COSMOS SE EXPANDE: All Gates Open", "La banda más innovadora del death metal psicodélico ha anunciado un lanzamiento doble...", "assets/Blood Incatatation_All Gates Open.png")
    ]
    
    # 2. Agenda Metalera Missing Items
    agenda = [
        ("Agenda Metalera", "AC/DC", "Estadio GNP Seguros | 7, 11 y 15 de abril", "assets/logos/acdc.png", "ABR 07 (Finalizado)"),
        ("Agenda Metalera", "Dream Theater", "Arena Ciudad de México | 10 de abril", "assets/logos/dreamtheater.png", "ABR 10 (Finalizado)"),
        ("Agenda Metalera", "Ill Nino", "F*ck off room | Cancelado", "assets/logos/ill_nino.png", "ABR -- (Cancelado)"),
        ("Agenda Metalera", "Jinjer", "Circo Volador | 19 de abril", "assets/logos/jinjer.png", "ABR 19 (Finalizado)"),
        ("Agenda Metalera", "Black Label Society", "Pabellón Oeste | Cancelado", "assets/logos/blacklabelsociety.png", "ABR -- (Cancelado)"),
        ("Agenda Metalera", "Metallica (Pantera y Avatar)", "Estadio GNP", "assets/logos/metallica.png", "MAY 24"),
        ("Agenda Metalera", "System Of A Down", "Foro Sol", "assets/logos/soad.png", "MAY 27")
    ]

    for n in news:
        # Check if already exists to avoid duplicates
        c.execute("SELECT 1 FROM content_items WHERE title = ?", (n[1],))
        if not c.fetchone():
            c.execute("INSERT INTO content_items (section, title, short_desc, image_filename) VALUES (?, ?, ?, ?)", n)
            
    for a in agenda:
        c.execute("SELECT 1 FROM content_items WHERE title = ?", (a[1],))
        if not c.fetchone():
            c.execute("INSERT INTO content_items (section, title, short_desc, image_filename, full_desc) VALUES (?, ?, ?, ?, ?)", (a[0], a[1], a[2], a[3], a[4]))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    add_missing_legacy()
    print("Database populated with missing Noticiero and Agenda items.")
