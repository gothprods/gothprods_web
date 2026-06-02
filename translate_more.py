import re

html_path = 'index_en.html'
with open(html_path, 'r') as f:
    html = f.read()

translations = {
    'Ver de nuevo a este ícono destrozando un monstruoso kit de percusiones (que': 'Seeing this icon again destroying a monstrous drum kit (which',
    'escenario. Ver a Angus Young, a sus más de setenta años, reventando su Gibson SG, brincando,': 'stage. Seeing Angus Young, in his seventies, destroying his Gibson SG, jumping,',
    'Afortunadamente, el legado ya está escrito con fuego. Ver a nuevas generaciones de "chavitos"': 'Fortunately, the legacy is already written in fire. Seeing new generations of "kids"',
    'To All tomó sus instrumentos y todo cambió. Ver en acción a estos verdaderos arquitectos del metal': 'To All took their instruments and everything changed. Seeing these true architects of metal in action',
    'Especial | ': 'Special | ',
    'Episodio': 'Episode',
    'Enero': 'January',
    'Febrero': 'February',
    'Marzo': 'March',
    'Abril': 'April',
    'Mayo': 'May',
    'Junio': 'June',
    'Julio': 'July',
    'Agosto': 'August',
    'Septiembre': 'September',
    'Octubre': 'October',
    'Noviembre': 'November',
    'Diciembre': 'December',
    'Reseñas Recientes': 'Recent Reviews',
    'Leer reseña completa &rarr;': 'Read full review &rarr;',
    'Ver Agenda Completa &rarr;': 'View Full Agenda &rarr;',
    'Nuevo': 'New',
    'Ver Caos Sonoro &rarr;': 'View Sonic Chaos &rarr;',
    'Ver Entrevistas &rarr;': 'View Interviews &rarr;',
    'Agenda': 'Agenda',
    'El Crew de Goth Prods asistirá': 'The Goth Prods Crew will attend',
    'Cancelado': 'Cancelled',
    'Evento Pasado': 'Past Event',
    'Finalizado': 'Finished',
    'Reseñas de <span>Conciertos</span>': '<span>Concert</span> Reviews',
    'La Galería Nocturna <span>Podcast</span>': 'La Galería Nocturna <span>Podcast</span>', # Keep name
    'Metal <span>Agenda 2026</span>': 'Metal <span>Agenda 2026</span>',
    'Destacados': 'Highlights',
    'Lo último en Metal': 'Latest in Metal',
    'Últimas Noticias': 'Latest News',
    'Entrevistas Under': 'Underground Interviews',
    'Contáctanos': 'Contact Us',
    'Envíanos un mensaje para contrataciones, reseñas de tu banda o colaboraciones.': 'Send us a message for bookings, band reviews or collaborations.',
    'Nombre': 'Name',
    'Correo Electrónico': 'Email',
    'Mensaje': 'Message',
    'Enviar Mensaje': 'Send Message',
    'Síguenos': 'Follow Us',
    'Derechos Reservados': 'All Rights Reserved',
    'Diseñado por': 'Designed by',
    '¡Bienvenidos al Capítulo 16 de Caos Sonoro! En esta entrega, la mesa se pone intensa para analizar los hilos que mueven la industria musical, la nostalgia tecnológica y las recomendaciones que están tronando en nuestros reproductores este mes. En esta sesión, nos acompaña Yussel para platicarnos a fondo sobre el concepto y la labor detrás de Heavy Mextal, una pieza clave en la difusión de nuestra escena. Además, nos metemos de lleno en el debate: ¿Son los hologramas el futuro de los shows en vivo o solo un truco de marketing? Analizamos también el "monopolio" de Live Nation y Ticketmaster que tiene a todos de cabeza.': 'Welcome to Chapter 16 of Sonic Chaos! In this installment, the table gets intense to analyze the strings that move the music industry, technological nostalgia, and the recommendations that are blasting in our players this month. In this session, Yussel joins us to talk in depth about the concept and work behind Heavy Mextal, a key piece in the dissemination of our scene. In addition, we dive right into the debate: Are holograms the future of live shows or just a marketing gimmick? We also analyze the Live Nation and Ticketmaster "monopoly" that has everyone upside down.',
}

for es, en in translations.items():
    html = html.replace(es, en)

with open(html_path, 'w') as f:
    f.write(html)

print("Translated more content.")
