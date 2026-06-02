import sqlite3

def add_legacy_podcasts():
    conn = sqlite3.connect('gothprods.db')
    c = conn.cursor()

    # We will just insert the most recent ones so they aren't empty, if they don't exist
    podcasts = [
        # La Galería Nocturna
        ("La Galería Nocturna", "Especial | AC/DC en Mexico | Estadio GNP Abril 7 2026", "Nuevo episodio analizando las controversias y cancelaciones recientes: Korn es funado, las sedes del Knotfest 2026...", "assets/Caos_Sonoro.jpg", "https://www.youtube.com/@gothprods44", "https://open.spotify.com/episode/0vXGPs6T7GNQgK9oNRQWXd", "https://podcasts.apple.com/mx/podcast/goth-prods/id1606324255?l=en"),
        ("La Galería Nocturna", "Caos Sonoro | Episodio 15", "Colaboración con Mexapedia y Brutal Revista. Perry y JC reciben a Ángel para hablar sobre el Metal Chingón.", "https://i.scdn.co/image/ab6765630000ba8a529c8b4d867e229bf615e57b", "https://www.youtube.com/watch?v=Tvr20W_ON74", "https://open.spotify.com/show/2hnlgkcGNl9GOAPa0WT9HW?si=7e9b95f203464fe6", ""),
        
        # Metal Pulse
        ("Metal Pulse", "Metal Pulse | Episodio 30 | Enero 2026", "Bandas revisadas: Kreator (Krushers Of The World), I Promised The World, Solely Veil...", "https://i.scdn.co/image/ab6765630000ba8a4550ecc3d9f7c63602acc85f", "", "https://open.spotify.com/episode/01bOT7VzGAwkaU54plxUli", "https://podcasts.apple.com/mx/podcast/metal-pulse/id1694587762?l=en-GB"),
        ("Metal Pulse", "Metal Pulse | Episodio 28 | Sep - Octubre 2025", "Bandas revisadas: Avatar, Last Retch, Paradox, From Fall to Spring, Henret...", "https://i.scdn.co/image/ab6765630000ba8a6f136538823fb5032726e6e6", "", "https://open.spotify.com/episode/23WeJ3Y1nuqwPbgSCHxeLc", "https://podcasts.apple.com/mx/podcast/metal-pulse/id1694587762?l=en-GB"),

        # Caos Sonoro
        ("Caos Sonoro", "🔥 LIVE Caos Sonoro | Episodio 16 | Abril 29, 2026 🔥", "🇲🇽¡Bienvenidos al Capítulo 16 de Caos Sonoro! En esta entrega, la mesa se pone intensa para analizar los hilos que mueven la industria musical...", "https://img.youtube.com/vi/JVst0FCaW04/maxresdefault.jpg", "https://www.youtube.com/watch?v=JVst0FCaW04", "https://open.spotify.com/show/2hnlgkcGNl9GOAPa0WT9HW?si=7e9b95f203464fe6", "https://podcasts.apple.com/mx/podcast/goth-prods/id1606324255?l=en"),
        ("Caos Sonoro", "Caos Sonoro | Episodio 15", "Colaboración con Mexapedia y Brutal Revista. Perry y JC reciben a Ángel para hablar sobre el Metal Chingón.", "https://img.youtube.com/vi/Tvr20W_ON74/maxresdefault.jpg", "https://www.youtube.com/watch?v=Tvr20W_ON74", "https://open.spotify.com/show/2hnlgkcGNl9GOAPa0WT9HW?si=7e9b95f203464fe6", "https://podcasts.apple.com/mx/podcast/goth-prods/id1606324255?l=en")
    ]

    for p in podcasts:
        c.execute("SELECT 1 FROM content_items WHERE title = ?", (p[1],))
        if not c.fetchone():
            c.execute("INSERT INTO content_items (section, title, short_desc, image_filename, yt_link, sp_link, ap_link) VALUES (?, ?, ?, ?, ?, ?, ?)", p)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    add_legacy_podcasts()
    print("Legacy podcasts added to DB.")
