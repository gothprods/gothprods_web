/* WARNING: Script requires that SQLITE_DBCONFIG_DEFENSIVE be disabled */
PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE section_permissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            section_name TEXT,
            can_create INTEGER DEFAULT 0,
            can_edit INTEGER DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
CREATE TABLE settings (key TEXT PRIMARY KEY, value TEXT);
INSERT INTO settings VALUES('hide_past_metalpulse','1');
INSERT INTO settings VALUES('hamburger_active','1');
INSERT INTO settings VALUES('logo_aliado_1','updates/logo_aliado_1_75da8ad2_Mexa.webp');
INSERT INTO settings VALUES('logo_aliado_2','updates/logo_aliado_2_e5af4573_Brutal.webp');
INSERT INTO settings VALUES('logo_aliado_3','updates/logo_aliado_3_962dbab4_JM.webp');
INSERT INTO settings VALUES('logo_aliado_4','updates/logo_aliado_4_2fcbfbac_Metal_Memes.webp');
INSERT INTO settings VALUES('logo_aliado_5','updates/logo_aliado_5_57d03b2f_metal_morfosis_verde_.webp');
INSERT INTO settings VALUES('team_img_1','updates/team_img_1_b49e2003_25.webp');
INSERT INTO settings VALUES('team_img_2','updates/team_img_2_5d16098f_24.webp');
INSERT INTO settings VALUES('team_img_3','updates/team_img_3_7753d69c_26.webp');
INSERT INTO settings VALUES('icon_equipo','updates/icon_equipo_20244e19_09_El_Equipo_La_Historia.webp');
INSERT INTO settings VALUES('agenda_poster','updates/agenda_poster_9d09cb6f_Agenda_Sep_Oct.webp');
INSERT INTO settings VALUES('title_mexapedia','Colectivo Mexapedia');
INSERT INTO settings VALUES('mexapedia_desc',unistr('MEXAPEDIA: AMPLIFICACIÓN TÁCTICA PARA LA LEGIÓN DEL METAL\u000d\u000a\u000d\u000a¿De qué sirve el concierto más brutal si la legión no se entera? En el Colectivo Mexapedia somos el motor de difusión más feroz del planeta, diseñado específicamente para el género que odia los algoritmos genéricos.\u000d\u000a\u000d\u000aNuestra misión es estratégica: asegurar la divulgación absoluta de tu evento. No vendemos boletos ni garantizamos venues llenos; activamos una red de difusión multiplataforma que penetra directamente en el subsuelo del metal.\u000d\u000a\u000d\u000aCon un solo impacto táctico, alcanzamos a una base de datos validada de más de 3 millones de metaleros verificados y hambrientos de volumen. No hay desperdicio de audiencia ni ''likes'' vacíos. Entregamos tu mensaje a un público 100% metalero, una comunidad profundamente comprometida que no solo escucha, sino que responde y propaga la señal.\u000d\u000a\u000d\u000aEsto no es alcance pasivo; es la fuerza estratégica y la frecuencia necesarias para que el género más intenso de la tierra sea escuchado con claridad aplastante.\u000d\u000a\u000d\u000aDeja de gritar en el vacío. Hazte escuchar con la precisión de Mexapedia. Tu frecuencia de amplificación metalera.'));
INSERT INTO settings VALUES('mexapedia_art','updates/mexapedia_art_5fffcd46_WhatsApp_Image_2026-07-27_at_15.24.51.webp');
INSERT INTO settings VALUES('show_mexapedia','1');
INSERT INTO settings VALUES('logo_aliado_6','updates/logo_aliado_6_heavy_mextal.webp');
INSERT INTO settings VALUES('caos_episode','21');
INSERT INTO settings VALUES('caos_date','2026-09-24');
INSERT INTO settings VALUES('caos_time','21:00');
INSERT INTO settings VALUES('caos_guests','');
INSERT INTO settings VALUES('header_logo','updates/header_logo_8134a4c1_Sep_2026.webp');
INSERT INTO settings VALUES('hero_title','');
INSERT INTO settings VALUES('hero_subtitle','');
INSERT INTO settings VALUES('show_reviews','1');
INSERT INTO settings VALUES('show_news','1');
INSERT INTO settings VALUES('show_interviews','1');
INSERT INTO settings VALUES('show_metalpulse','1');
INSERT INTO settings VALUES('show_agenda','1');
INSERT INTO settings VALUES('show_banda_semana','1');
INSERT INTO settings VALUES('show_el_pit','1');
INSERT INTO settings VALUES('show_galeria_nocturna','1');
INSERT INTO settings VALUES('show_contactanos','0');
INSERT INTO settings VALUES('show_medios_aliados','1');
INSERT INTO settings VALUES('show_el_equipo','1');
INSERT INTO settings VALUES('show_equipo_menu','1');
INSERT INTO settings VALUES('agenda_desc','<p style="text-align: justify;"><span style="color: rgb(113, 109, 74);"><span style="color: rgb(113, 109, 74); font-weight: bold;">¡Berserkers!</span></span></p><p><br></p><p>¿Pensaban que el año se iba a calmar? ¡Para nada! Preparen el cuello y la cartera porque Agosto y Septiembre vienen cargados de puro poder y distorsión.</p>');
INSERT INTO settings VALUES('title_destacados','Radar del Caos');
INSERT INTO settings VALUES('title_el_pit','El Pit');
INSERT INTO settings VALUES('title_galeria','La Galería Nocturna');
INSERT INTO settings VALUES('title_metalpulse','Metal Pulse');
INSERT INTO settings VALUES('title_reviews','Reseñas de Conciertos');
INSERT INTO settings VALUES('title_news','El Noticiero Nocturno');
INSERT INTO settings VALUES('title_interviews','Entrevistas Under');
INSERT INTO settings VALUES('title_agenda','Agenda Metalera');
INSERT INTO settings VALUES('title_contacto','Contáctanos');
INSERT INTO settings VALUES('title_equipo','El Equipo, La Historia');
INSERT INTO settings VALUES('hero_bg','updates/hero_bg_9d765c58_Banner_YOutube.webp');
INSERT INTO settings VALUES('icon_home','updates/icon_home_74d4147e_Sep_2026.webp');
INSERT INTO settings VALUES('team_name_1','JC');
INSERT INTO settings VALUES('team_role_1','Host y Co-Fundador');
INSERT INTO settings VALUES('team_bio_1','');
INSERT INTO settings VALUES('team_name_2','Perry');
INSERT INTO settings VALUES('team_role_2','Host y Co-fundador');
INSERT INTO settings VALUES('team_bio_2','');
INSERT INTO settings VALUES('team_name_3','LORNA');
INSERT INTO settings VALUES('team_role_3','Tejedora de Leyendas Creativas');
INSERT INTO settings VALUES('team_bio_3','');
INSERT INTO settings VALUES('team_name_4','');
INSERT INTO settings VALUES('team_role_4','');
INSERT INTO settings VALUES('team_bio_4','');
INSERT INTO settings VALUES('team_name_5','');
INSERT INTO settings VALUES('team_role_5','');
INSERT INTO settings VALUES('team_bio_5','');
INSERT INTO settings VALUES('team_history_2021','<p><b><span style="color: rgb(113, 109, 74);">El Despertar desde las Sombras</span></b></p><p><br></p><div style="text-align: justify;"><p>En el año en que el mundo se detuvo, el ruido no pudo ser silenciado. Entre las grietas de una crisis global, los hermanos José y Juan Carlos Espinosa fundaron Goth Productions. Lo que nació en el confinamiento como una necesidad de expresión, tomó forma a través de La Galería Nocturna, un podcast que se convirtió en el latido de la productora.</p><p>Desde el inicio, nos dedicamos a desmenuzar la ferocidad del metal: álbumes, unboxings y colecciones que celebran nuestra obsesión por el género. Fue un año de experimentación pura, donde incluso lanzamos el primer álbum de Algos (nuestra banda de casa), marcando el inicio de nuestra faceta como impulsores de talento.</p></div><p></p><p></p><p></p>');
INSERT INTO settings VALUES('team_history_2022',unistr('<span style="color: rgb(113, 109, 74);"><b>La Expansión del Rugido.</b></span>\u000d\u000a<div style="text-align: justify;"><br></div><div style="text-align: justify;">\u000d\u000aCuando las puertas se abrieron, Goth Prods salió a las calles. En 2022, dejamos de ser solo voces detrás de un micrófono para convertirnos en testigos de la brutalidad en vivo. Comenzamos a cubrir festivales y conciertos tanto en México como en el extranjero, capturando la energía del moshpit.\u000d\u000a\u000d\u000aNuestra autenticidad resonó; las bandas empezaron a buscarnos, reconociendo en nosotros un medio confiable. Cerramos el año consolidando nuestra identidad con el lanzamiento del álbum de The Folly Three, reafirmando nuestro compromiso con la creación musical.</div>'));
INSERT INTO settings VALUES('team_history_2023',unistr('<b><span style="color: rgb(113, 109, 74);">Cruzando Fronteras y Uniendo Sangre.</span></b>\u000d\u000a<div style="text-align: justify;"><br></div><div style="text-align: justify;">\u000d\u000aEl 2023 fue el año de la consolidación. Nos convertimos en un puente internacional, realizando entrevistas exclusivas con bandas de Estados Unidos, Europa y toda Latinoamérica. En junio, pisamos suelo europeo para cubrir el Download Festival, trayendo la experiencia de los grandes escenarios a nuestra comunidad.\u000d\u000a\u000d\u000aNo conformes con un solo frente, lanzamos Metal Pulse, un podcast dedicado a las noticias y lanzamientos que mantienen vivo al género. La colaboración se volvió nuestra bandera, uniendo fuerzas con otros medios locales para fortalecer la escena desde la raíz.</div>'));
INSERT INTO settings VALUES('team_history_2024',unistr('<b><span style="color: rgb(113, 109, 74);"></span></b><div style="text-align: justify;"><b><span style="color: rgb(113, 109, 74);">El Renacimiento del Festival y el Poder de la Comunidad.</span></b>\u000d\u000a<br></div><div style="text-align: justify;"><br></div><div style="text-align: justify;">\u000d\u000aEl hito que marcó este año fue el regreso triunfal del GothFest. Tras siete años de silencio desde su primera edición en 2017, el festival volvió con una fuerza renovada, uniendo a músicos, artistas visuales y medios en un solo grito.\u000d\u000a\u000d\u000aNuestra voz llegó a más de 36,000 metalheads. No somos solo un medio; somos un colectivo que trabaja incansablemente para expandir la cultura del metal en la región, colaborando hombro a hombro con los protagonistas de la escena.</div>'));
INSERT INTO settings VALUES('team_history_2025',unistr('<div style="text-align: justify;"><b><span style="color: rgb(113, 109, 74);">Cuatro Años de Caos y Hermandad.</span></b>\u000d\u000a<br></div><div style="text-align: justify;"><br></div><div style="text-align: justify;">\u000d\u000aLlegamos al 2025 celebrando el cuarto aniversario de La Galería Nocturna Live de la única forma que sabemos: con un show en vivo rodeados de la élite de los medios y bandas demoledoras. La batalla continuó en escenarios internacionales como el Sonic Temple, donde vivimos cuatro días de intensidad pura con más de 100 bandas.\u000d\u000a\u000d\u000aEl año arrancó con un golpe de autoridad: el nacimiento de Caos Sonoro, una alianza estratégica con Brutal Revista Digital y Mexapedia.</div>'));
INSERT INTO settings VALUES('team_history_2026',unistr('<span style="color: rgb(113, 109, 74);"><b></b></span><div style="text-align: justify;"><span style="color: rgb(113, 109, 74);"><b>El Referente del Metal: Sin Filtros y Sin Fronteras.</b></span>\u000d\u000a<br></div><div style="text-align: justify;">\u000d\u000aEl 2026 nos encuentra en el punto más alto de nuestra ofensiva. Seguimos siendo testigos de la locura y la ferocidad del género más poderoso del planeta, manteniendo un pie en el underground global y otro en el mainstream, porque antes que productores, seguimos siendo fans devotos de esta música.\u000d\u000a<span style="color: rgb(113, 109, 74);">\u000d\u000aLa Evolución Digital: De Podcast a Medio Total.</span>\u000d\u000a\u000d\u000aEste año, nuestra misión ha dado un salto evolutivo definitivo. Con la liberación de nuestro sitio web oficial, gothprods.com, marcamos un antes y un después: dejamos de ser únicamente un podcast con difusión en redes sociales para transformarnos en un medio de comunicación en su totalidad.\u000d\u000a\u000d\u000aYa no solo cubrimos eventos en México, Europa y Estados Unidos para compartir la energía del escenario; ahora somos importadores de conocimiento. Al ser testigos de las áreas donde la escena metalera ha fallado, hemos asumido la responsabilidad de compartir las buenas prácticas del mundo con nuestro país. Queremos que nuestra escena crezca con orden, profesionalismo y la fuerza que se merece.\u000d\u000a<span style="color: rgb(113, 109, 74);">\u000d\u000aAlianzas de Acero y Caos Sonoro.</span>\u000d\u000a\u000d\u000aLas colaboraciones con otros medios crecen día con día, fortaleciendo una red de difusión sin precedentes en la región. En este camino, hemos concretado una alianza estratégica con Mexapedia, Metal Memes, Brutal Revista, Johny Metal y Metalmorfosis, uniendo fuerzas para formar un colectivo sólido y blindado para la difusión del género.\u000d\u000a\u000d\u000aDentro de esta sinergia, nuestro espacio de "Caos Sonoro" cada vez se pone más macizo, contando con invitados especiales que aportan una perspectiva de la escena bastante real, cruda y ejecutada de una forma magistral.\u000d\u000a<span style="color: rgb(113, 109, 74);">\u000d\u000aCrecimiento Interno y Crítica Sin Filtros. </span>\u000d\u000a\u000d\u000aPara sostener esta maquinaria en constante expansión, el equipo se refuerza desde la raíz: Lorna se integra a las filas de Goth Prods como la mente creativa, encargada de darle dirección visual e identitaria a esta nueva era del proyecto.\u000d\u000a\u000d\u000aSin embargo, nuestro crecimiento no nos ha ablandado: nos hemos consolidado como duros críticos de nuestra propia industria. Cuando las cosas no van bien en la escena, en Goth Productions lo decimos sin filtros y sin tiento. Nuestra lealtad no es con las apariencias, sino con el Metal. Somos el espejo de la escena: celebramos sus victorias y señalamos sus vicios, siempre con el objetivo de forjar un futuro más sólido para todos los que vivimos por y para el ruido.\u000d\u000a\u000d\u000aEn Goth Productions no solo difundimos metal; construimos el legado de la escena underground. La hermandad sigue creciendo, y el caos apenas comienza.</div>'));
INSERT INTO settings VALUES('poster_views','2');
CREATE TABLE colectivo_mexapedia (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        descripcion TEXT,
        img_path TEXT,
        is_active INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
INSERT INTO colectivo_mexapedia VALUES(1,'Colectivo Mexapedia: Amplificación Táctica para la Legión del Metal','<p><b><span style="color: rgb(113, 109, 74);"></span></b></p><div style="text-align: justify;"><p><b><span style="color: rgb(113, 109, 74);">¿De qué sirve el concierto más brutal si la legión no se entera?</span></b> En el Colectivo Mexapedia no somos el motor de difusión más feroz del planeta, diseñado específicamente para el género que odia los algoritmos genéricos.</p><p><br></p><p><b><span style="color: rgb(113, 109, 74);">Nuestra misión es estratégica: </span></b>asegurar la divulgación absoluta de tu evento. Activamos una red de difusión multiplataforma que penetra directamente en el subsuelo del metal.</p><p><br></p><p><b><span style="color: rgb(113, 109, 74);">Con un solo impacto táctico, alcanzamos a una base de datos validada de más de 3 millones de metaleros</span></b> sedientosde volumen. No hay desperdicio de audiencia ni ''likes'' vacíos. Entregamos tu mensaje a un público 100% metalero, una comunidad profundamente comprometida que no solo escucha, sino que responde y propaga la señal.</p><p><br></p><p>Esto no es alcance pasivo; <b><span style="color: rgb(113, 109, 74);">es la fuerza estratégica y la frecuencia necesarias para que el género más intenso de la tierra </span></b>sea escuchado con claridad aplastante.</p><p><br></p><p>Deja de gritar en el vacío. <b><span style="color: rgb(113, 109, 74);">Hazte escuchar con la precisión del Colectivo Mexapedia.</span></b> Tu frecuencia de amplificación metalera.</p></div><p></p>','updates/mexapedia_96588650_WhatsApp_Image_2026-07-27_at_15.24.51.webp',1,'2026-07-28 17:22:09');
INSERT INTO colectivo_mexapedia VALUES(2,'¡Tu proyecto merece la escena más feroz del planeta! Goth Prods y Colectivo Mexapedia unen fuerzas para tu lanzamiento masivo','<p>En<span style="color: rgb(113, 109, 74);"> Goth Prods</span> entendemos que la creación artística es solo la mitad del camino. La otra mitad, y a menudo la más desafiante, es lograr que esa creación sea vista y escuchada por la audiencia correcta.</p><p><br></p><p><span style="color: rgb(113, 109, 74);">La escena mexicana del metal y la música dura es, sin duda,</span> <span style="color: rgb(113, 109, 74);">«una de las más feroces del planeta»</span>. Es un ecosistema vibrante, apasionado y exigente; por eso, nos enorgullece anunciar una alianza estratégica para ofrecerte una oportunidad única de visibilidad masiva.</p><p><br></p><p><b></b></p><span style="color: rgb(113, 109, 74);"><p><b>Alcance masivo: más de 3 millones de personas a tu alcance</b></p><p></p></span><p><br></p><p>¿Te imaginas que tu música, tu arte o tu evento lleguen a una audiencia de más de 3 millones de personas? Esto ya no es un sueño lejano ni una campaña genérica: es una estrategia dirigida al corazón de la comunidad metalera y artística.</p><p><br></p><p>Si eres músico, integrante de una banda, promotor de eventos, tatuador que busca mostrar su arte o artista visual, esta es la plataforma que estabas esperando. Tu talento merece este escenario.</p><p><br></p><p><b><span style="color: rgb(113, 109, 74);">El motor: Colectivo Mexapedia</span></b></p><p><br></p><p>Esta visibilidad sin precedentes se logra a través del Colectivo Mexapedia, consolidado como la plataforma de divulgación líder en la escena. Mexapedia no es solo un nombre; es el punto de encuentro de una comunidad vasta y activa que vive y respira metal. Al integrar tu proyecto a este ecosistema, garantizas un espacio en el radar de los fanáticos más dedicados.</p><p><br></p><p><b><span style="color: rgb(113, 109, 74);">La red de poder: medios asociados</span></b></p><p><br></p><p>Esta alianza no se limita a una sola plataforma. Tu proyecto será divulgado a través de una poderosa red de medios asociados, cada uno con su propia base de seguidores leales, cubriendo todos los nichos y subgéneros de la escena.</p><p><br></p><p>Al solicitar tu estrategia de campaña digital, tu proyecto será impulsado por:</p><p></p><span style="color: rgb(113, 109, 74);"><p>- Mexapedia</p><p>- Goth Prods</p><p>- Heavy Mextal</p><p>- Metal Memes</p><p>- Metalmorfosis</p><p>- Brutal Revista</p><p>- Johny Metal</p></span><p></p><p><br></p><p><b><span style="color: rgb(113, 109, 74);">Tu momento es ahora</span></b></p><p><br></p><p>En <span style="color: rgb(113, 109, 74);">Goth Prods </span>no solo producimos: proyectamos. No dejes que tu trabajo se pierda en el ruido; la escena feroz está lista para recibirte.</p><p><br></p><p>Solicita tu estrategia de campaña digital hoy. No pierdas la oportunidad de ser parte de esta nueva era de difusión masiva. <span style="color: rgb(113, 109, 74);">Ponte en contacto con nosotros y prepárate para conquistar la escena más feroz del planeta con el respaldo de Goth Prods y Colectivo Mexapedia.</span></p>','updates/mexapedia_3a9fef19_Promo.webp',1,'2026-08-22 19:13:30');
COMMIT;
