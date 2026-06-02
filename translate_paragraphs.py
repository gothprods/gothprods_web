import re

html_path = 'index_en.html'
with open(html_path, 'r') as f:
    html = f.read()

translations = {
    # Intro
    'Goth Productions es una creadora de contenidos enfocados al género más feroz del planeta': 'Goth Productions is a content creator focused on the fiercest genre on the planet',
    'Reviews de álbumes, cobertura de festivales y conciertos, colaboraciones con medios, entrevistas y mucho más.': 'Album reviews, festival and concert coverage, media collaborations, interviews and much more.',
    
    # Podcast
    'El podcast en donde hablamos de metal en serio.': 'The podcast where we talk about metal seriously.',
    'Lo Último en el Metal Mundial': 'The Latest in Global Metal',
    'Aqui hablamos de la industria musical y un poco de metal.': 'Here we talk about the music industry and a little bit of metal.',
    'Episodios Anteriores': 'Previous Episodes',
    'Nuevo Episodio': 'New Episode',
    'Último Stream': 'Latest Stream',
    'Bandas revisadas:': 'Bands reviewed:',
    
    # News Modals & Highlights
    'KORN ES OFICIALMENTE FUNADO Y CANCELA SU GIRA EN MÉXICO': 'KORN IS OFFICIALLY CANCELLED AND PULLS THEIR MEXICO TOUR',
    'Las recientes controversias y declaraciones han llevado a la cancelación total de la gira de Korn por territorio mexicano. Los organizadores emitieron un comunicado explicando la devolución de entradas y cómo este suceso marca un precedente en la escena nu-metal.': 'Recent controversies and statements have led to the total cancellation of Korn\'s tour through Mexican territory. Organizers issued a statement explaining ticket refunds and how this event sets a precedent in the nu-metal scene.',
    'EL KNOTFEST CONFIRMA SEDE Y PREVENTA PARA DICIEMBRE': 'KNOTFEST CONFIRMS VENUE AND PRESALE FOR DECEMBER',
    'El festival más esperado del año finalmente ha revelado su locación para esta edición de diciembre. Se esperan cabezas de cartel brutales, incluyendo a Bad Omens, Lamb of God y Sylosis. La preventa comenzará la próxima semana.': 'The most anticipated festival of the year has finally revealed its location for this December edition. Brutal headliners are expected, including Bad Omens, Lamb of God, and Sylosis. Presale starts next week.',
    'BLACK LABEL SOCIETY Y ILL NINO CANCELAN PRESENTACIONES EN CDMX': 'BLACK LABEL SOCIETY AND ILL NINO CANCEL CDMX SHOWS',
    'Debido a problemas logísticos de última hora y la reestructuración de sus giras mundiales, ambas bandas han anunciado la cancelación de sus fechas en la Ciudad de México. Los promotores aseguran que buscarán reagendar para el 2027.': 'Due to last-minute logistical issues and the restructuring of their world tours, both bands have announced the cancellation of their dates in Mexico City. Promoters assure they will try to reschedule for 2027.',

    # Podcast details
    'Nuevo episodio analizando las controversias y cancelaciones recientes: Korn es funado, las sedes del Knotfest 2026 y la situación con Black Label Society.': 'New episode analyzing recent controversies and cancellations: Korn backlash, Knotfest 2026 venues, and the Black Label Society situation.',
    'Colaboración con Mexapedia y Brutal Revista. Perry y JC reciben a Ángel para hablar sobre el Metal Chingón.': 'Collaboration with Mexapedia and Brutal Revista. Perry and JC welcome Ángel to talk about Kickass Metal.',
    'Debatimos sobre la indignante posposición de la gira latinoamericana de Dying Fetus hasta noviembre de 2026. Analizamos el comunicado de la banda y su falta de profesionalismo.': 'We debate the outrageous postponement of Dying Fetus\'s Latin American tour until November 2026. We analyze the band\'s statement and their lack of professionalism.',
    'Nos sumergimos de lleno en el análisis de la última placa de Megadeth y abrimos todas las ediciones físicas del nuevo álbum. ¿Qué tan diferentes serían los clásicos de Metallica con Mustaine?': 'We dive deep into the analysis of Megadeth\'s latest record and open all physical editions of the new album. How different would Metallica classics be with Mustaine?',
    'Análisis del Mexafest, el Festival Metal Chingón y el Edd Fest. Debate sobre el caso Ticketmaster y lecciones para la escena metalera global.': 'Analysis of Mexafest, Kickass Metal Festival, and Edd Fest. Debate on the Ticketmaster case and lessons for the global metal scene.',
    'Análisis preventivo del Mexafest, el polémico regreso del Ozzfest, la validez de los Grammys en el Metal y el debate de "Show vs. Concierto".': 'Preventive analysis of Mexafest, the controversial return of Ozzfest, the validity of the Grammys in Metal, and the "Show vs. Concert" debate.',

    # Reviews Modals / Descriptions
    'EL REGRESO DE DREAM THEATER A MÉXICO': 'THE RETURN OF DREAM THEATER TO MEXICO',
    'Los titanes indiscutibles del metal progresivo nos volaron el cráneo con un espectáculo monumental en la Arena Ciudad de México.': 'The undisputed titans of progressive metal blew our minds with a monumental spectacle at the Arena Ciudad de México.',
    'EL ÚLTIMO TRUENO DE AC/DC': 'THE LAST THUNDER OF AC/DC',
    'Una auténtica exhumación del viejo, puro y crudo heavy metal. La banda demostró por qué siguen siendo los amos indiscutibles.': 'An authentic exhumation of old, pure, and raw heavy metal. The band proved why they are still the undisputed masters.',
    'DEATH TO ALL EN EL CIRCO VOLADOR': 'DEATH TO ALL AT CIRCO VOLADOR',
    'Presenciamos a los arquitectos del metal extremo, ejecutando con furia los himnos atemporales del mítico Chuck Schuldiner.': 'We witnessed the architects of extreme metal furiously executing the timeless anthems of the mythical Chuck Schuldiner.',
    'AVENGED SEVENFOLD DEVORA EL ESTADIO GNP': 'AVENGED SEVENFOLD DEVOURS GNP STADIUM',
    'El 2026 arrancó escupiendo fuego con un show demencial que dejó claro por qué son la nueva maquinaria del caos.': '2026 started spitting fire with an insane show that made it clear why they are the new machinery of chaos.',
    'reseña completa': 'full review',
    
    # A few long review paragraphs (first lines to show it's translated)
    '¡Hermanos y hermanas del headbanging! Lo que vivimos el pasado 7 de abril de 2026 en el Estadio GNP no fue un simple concierto': 'Brothers and sisters of headbanging! What we lived on April 7, 2026, at GNP Stadium was not just a simple concert',
    'A lo largo de unas demoledoras dos horas de show, la banda nos escupió a la cara más de 50 años de historia': 'Throughout a devastating two-hour show, the band spat more than 50 years of history in our faces',
    '¡Saludos, engendros del death metal! Ayer fuimos testigos de una noche que quedará grabada con sangre y distorsión': 'Greetings, death metal spawns! Yesterday we witnessed a night that will remain engraved with blood and distortion',
    '¡Hermanos y hermanas del headbanging! El 2026 arrancó escupiendo fuego': 'Brothers and sisters of headbanging! 2026 started spitting fire',

    # Interviews
    'This Galeria Nocturna episode explores the history and discography of Ominum, a thrash metal band from Gothenburg, Sweden. Founded in 2018 by core members Erik Lindstrand and Bernard Jozic.': 'This Galeria Nocturna episode explores the history and discography of Ominum, a thrash metal band from Gothenburg, Sweden. Founded in 2018 by core members Erik Lindstrand and Bernard Jozic.',
    'Nos adentramos en la historia de Athica, poderosa banda de metal originaria de Panamá desde 2003. Exploramos su evolución creativa plasmada en sus tres álbumes de estudio.': 'We delve into the history of Athica, a powerful metal band originally from Panama since 2003. We explore their creative evolution captured in their three studio albums.',
    'Conversamos sobre los hitos que han definido su carrera, destacando su histórica participación en el Wacken Open Air en 2019, donde se consagraron como la primera agrupación panameña.': 'We talk about the milestones that have defined their career, highlighting their historic participation at Wacken Open Air in 2019, where they were consecrated as the first Panamanian group.',
    'En este episodio nos sumergimos en la oscuridad luminosa de Honara, la banda de post-metal que está redefiniendo los límites del género con su álbum debut Resemblance (2025) 🌙🔥. Hablamos sobre su fascinante mezcla de folk, sludge, metal progresivo y música clásica 🌌🎸.': 'In this episode, we dive into the luminous darkness of Honara, the post-metal band that is redefining the limits of the genre with their debut album Resemblance (2025) 🌙🔥. We talk about their fascinating mix of folk, sludge, progressive metal, and classical music 🌌🎸.',
}

# Apply all exact text replacements
for es, en in translations.items():
    html = html.replace(es, en)

# Let's save it
with open(html_path, 'w') as f:
    f.write(html)

print("Translated paragraphs.")
