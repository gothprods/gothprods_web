import re

def create_en_version():
    with open('index.html', 'r') as f:
        html = f.read()
    
    # 1. Flip the language switcher active state
    html = html.replace(
        '<a href="index.html" class="lang-btn active" style="color: var(--accent-color); font-weight: bold; text-decoration: none;">ES</a>\n                <span style="color: #666;">|</span>\n                <a href="index_en.html" class="lang-btn" style="color: var(--text-muted); text-decoration: none; transition: color 0.3s;">EN</a>',
        '<a href="index.html" class="lang-btn" style="color: var(--text-muted); text-decoration: none; transition: color 0.3s;">ES</a>\n                <span style="color: #666;">|</span>\n                <a href="index_en.html" class="lang-btn active" style="color: var(--accent-color); font-weight: bold; text-decoration: none;">EN</a>'
    )
    
    # 2. Translate common UI elements
    translations = {
        'Lo último en Metal': 'Latest in Metal',
        'Reseñas de Conciertos': 'Concert Reviews',
        'Últimas Noticias': 'Latest News',
        'Entrevistas Under': 'Underground Interviews',
        'Agenda Metalera': 'Metal Agenda',
        'Contáctanos': 'Contact Us',
        'EXPLORAR CONTENIDO': 'EXPLORE CONTENT',
        'Últimas Noticias <span>Del Mes</span>': 'Latest News <span>Of The Month</span>',
        'Reseñas de Conciertos <span>Destacadas</span>': 'Featured <span>Concert Reviews</span>',
        'Agenda <span>Metalera 2026</span>': 'Metal <span>Agenda 2026</span>',
        'Caos <span>Sonoro</span>': 'Sonic <span>Chaos</span>',
        'Entrevistas <span>Under</span>': 'Underground <span>Interviews</span>',
        'Ver Caos Sonoro &rarr;': 'Watch Sonic Chaos &rarr;',
        'Ver Entrevistas &rarr;': 'View Interviews &rarr;',
        'Ver Todas Las Noticias &rarr;': 'View All News &rarr;',
        'Leer Reseñas &rarr;': 'Read Reviews &rarr;',
        'Ver Agenda Completa &rarr;': 'View Full Agenda &rarr;',
        'Eventos Pasados': 'Past Events',
        'Evento Pasado': 'Past Event',
        'Finalizado': 'Finished',
        'Boletos': 'Tickets',
        'Únete a nuestra newsletter para recibir las últimas noticias del mundo del metal.': 'Join our newsletter to receive the latest news from the metal world.',
        'Suscribirse': 'Subscribe',
        'Derechos Reservados': 'All Rights Reserved',
        'Escucha en Spotify': 'Listen on Spotify',
        'Escucha en Apple Podcasts': 'Listen on Apple Podcasts',
        'Ver en YouTube': 'Watch on YouTube',
        'El misterio y ocultismo detrás de sus máscaras.': 'The mystery and occultism behind their masks.',
        'Hablamos sobre el futuro del death metal polaco.': 'We talk about the future of Polish death metal.',
        'Preventa de boletos e información de sede.': 'Ticket presale and venue info.',
        'Dave Mustaine promete un setlist old-school.': 'Dave Mustaine promises an old-school setlist.',
        'Cartel completo anunciado con bandas nacionales e internacionales.': 'Full lineup announced with national and international bands.',
        'La locura armenia regresará con nueva producción escénica.': 'The Armenian madness returns with new stage production.',
        'León se prepara para el festival de metal extremo más oscuro del país.': 'León prepares for the darkest extreme metal festival in the country.',
        'Tras las recientes funas, la banda cancela su visita.': 'After recent backlash, the band cancels their visit.',
        'Zakk Wylde pospone presentaciones en CDMX.': 'Zakk Wylde postpones CDMX shows.',
        'El majestuoso regreso de Mike Portnoy.': 'The majestic return of Mike Portnoy.',
        'Una devorada monumental al Estadio GNP.': 'A monumental devour at GNP Stadium.',
        'El último gran trueno del viejo metal.': 'The last great thunder of old metal.',
        'Historia y discografía de la banda de thrash sueca.': 'History and discography of the Swedish thrash band.',
        'Evolución creativa y tres álbumes de estudio.': 'Creative evolution and three studio albums.',
        'Oscuridad luminosa y post-metal redefiniendo límites.': 'Luminous darkness and post-metal redefining limits.',
        'Abril': 'April',
        'Mayo': 'May',
        'Junio': 'June',
        'Julio': 'July',
        'Agosto': 'August',
        'Septiembre': 'September',
        'Octubre': 'October',
        'Noviembre': 'November',
        'Diciembre': 'December',
        '<html lang="es">': '<html lang="en">',
    }
    
    for es, en in translations.items():
        html = html.replace(es, en)
        
    with open('index_en.html', 'w') as f:
        f.write(html)
        
    print("Created index_en.html")

create_en_version()
