import re

html_path = 'index.html'
with open(html_path, 'r') as f:
    html = f.read()

# 1. Insert new cards in news-rail
news_cards = """
                <div class="news-card">
                    <img src="assets/reload_2.jpg" alt="Metallica ReLoad" style="width: 100%; border-radius: 8px; margin-bottom: 10px; height: 140px; object-fit: cover;">
                    <h3 style="font-size: 1rem; line-height: 1.2;">🎸🔥 ¡METALLICA ANUNCIA EL ÉPICO BOX SET REMASTERIZADO DE 'RELOAD'! 🔥🎸</h3>
                    <p style="font-size: 0.85rem; margin-bottom: 10px;">Metallica ha confirmado el lanzamiento de la edición definitiva y remasterizada de su séptimo álbum...</p>
                    <a href="javascript:void(0);" data-target="newsModal4" class="open-review-modal" style="color: var(--accent-color); font-weight: bold; font-size: 0.85rem;">Leer más &rarr;</a>
                </div>
                <div class="news-card">
                    <img src="assets/dimebag_dean.jpg" alt="Dimebag Dean Guitars" style="width: 100%; border-radius: 8px; margin-bottom: 10px; height: 140px; object-fit: cover; background: #222;">
                    <h3 style="font-size: 1rem; line-height: 1.2;">🚨 ¡ACTUALIZACIÓN EN LA BATALLA LEGAL: DIMEBAG DARRELL VS. DEAN GUITARS!</h3>
                    <p style="font-size: 0.85rem; margin-bottom: 10px;">La larga disputa legal sobre el legado de una de las leyendas más grandes del metal ha tomado un giro decisivo...</p>
                    <a href="javascript:void(0);" data-target="newsModal5" class="open-review-modal" style="color: var(--accent-color); font-weight: bold; font-size: 0.85rem;">Leer más &rarr;</a>
                </div>"""

html = html.replace('<div class="news-rail">\n                <!-- 10 Noticias -->', '<div class="news-rail">\n                <!-- 10 Noticias -->\n' + news_cards)

# 2. Append missing review modals and new news modals before </body>
modals_html = """
    <!-- Missing Review Modals Restored -->
    <div id="reviewModal1" class="modal">
        <div class="modal-content">
            <span class="close-modal">&times;</span>
            <img src="assets/dream_theater_horizontal.jpg" alt="Dream Theater Banner" class="modal-banner">
            <div class="modal-body">
                <h2>EL REGRESO DE DREAM THEATER A MÉXICO</h2>
                <p>Los titanes indiscutibles del metal progresivo nos volaron el cráneo con un espectáculo monumental en la Arena Ciudad de México. La alineación clásica de Portnoy volvió con toda su gloria.</p>
            </div>
        </div>
    </div>
    <div id="reviewModal2" class="modal">
        <div class="modal-content">
            <span class="close-modal">&times;</span>
            <img src="assets/acdc_review.jpg" alt="AC/DC Banner" class="modal-banner">
            <div class="modal-body">
                <h2>EL ÚLTIMO TRUENO DE LOS DIOSES: AC/DC Y EL CREPÚSCULO DE LOS TITANES EN EL ESTADIO GNP</h2>
                <p>¡Hermanos y hermanas del headbanging! Lo que vivimos el pasado 7 de abril de 2026 en el Estadio GNP no fue un simple concierto, fue una auténtica exhumación del viejo, puro y crudo heavy metal. Con el inicio de su brutal gira Power Up en México, AC/DC congregó a 60,000 almas para demostrarnos por qué siguen siendo los amos indiscutibles del alto voltaje.</p>
            </div>
        </div>
    </div>
    <div id="reviewModal3" class="modal">
        <div class="modal-content">
            <span class="close-modal">&times;</span>
            <img src="assets/death_to_all_review.jpg" alt="Death To All Banner" class="modal-banner">
            <div class="modal-body">
                <h2>EL LEGADO INMORTAL DE CHUCK SCHULDINER: DEATH TO ALL ARROLLA EL CIRCO VOLADOR</h2>
                <p>¡Saludos, engendros del death metal! Ayer fuimos testigos de una noche que quedará grabada con sangre y distorsión en la historia del metal extremo en México. El legendario Circo Volador obró un absoluto milagro sonoro para recibir a Death To All.</p>
            </div>
        </div>
    </div>
    <div id="reviewModal4" class="modal">
        <div class="modal-content">
            <span class="close-modal">&times;</span>
            <img src="assets/avenged_sevenfold_review.jpg" alt="Avenged Sevenfold Banner" class="modal-banner">
            <div class="modal-body">
                <h2>EL BANDERAZO DEL CAOS: AVENGED SEVENFOLD DEVORA EL ESTADIO GNP</h2>
                <p>¡Hermanos y hermanas del headbanging! El 2026 arrancó escupiendo fuego, y los encargados de dar el banderazo de salida para la demencial agenda de conciertos de este año fueron nada más y nada menos que Avenged Sevenfold.</p>
            </div>
        </div>
    </div>

    <!-- New News Modals -->
    <div id="newsModal4" class="modal">
        <div class="modal-content">
            <span class="close-modal">&times;</span>
            <img src="assets/reload_2.jpg" alt="Metallica ReLoad" class="modal-banner">
            <div class="modal-body">
                <h2>🎸🔥 ¡METALLICA ANUNCIA EL ÉPICO BOX SET REMASTERIZADO DE 'RELOAD'! 🔥🎸</h2>
                <p>Metallica ha confirmado el lanzamiento de la edición definitiva y remasterizada de su séptimo álbum de estudio, "ReLoad". Esta monstruosa caja de lujo de edición limitada estará disponible a partir del 26 de junio a través de su sello Blackened Recordings.</p>
                <p>¿Qué incluye este enorme lanzamiento? Prepárate para casi 29 horas de material con lo siguiente:</p>
                <ul>
                    <li>15 CDs que incluyen el disco remasterizado, más de 70 pistas con riffs y demos inéditos, rarezas, shows acústicos y múltiples conciertos en vivo alrededor del mundo (incluyendo Norteamérica, Europa, Australia y Japón).</li>
                    <li>4 DVDs con actuaciones completas en vivo (como el famoso show "Banned in Philly" y material de la gira asiática), apariciones en televisión y grabaciones en el estudio.</li>
                    <li>El álbum original remasterizado en doble vinilo de 180 gramos.</li>
                    <li>Un vinilo triple con el concierto "Live at Ministry Of Sound 97" en Londres.</li>
                    <li>Un sencillo en vinilo de 7 pulgadas del tema "The Memory Remains".</li>
                </ul>
                <p>Para los verdaderos coleccionistas, la caja es un tesoro repleto de memorabilia física: un libro de tapa dura de 128 páginas con fotos e historias nunca antes vistas, un paquete de 13 tarjetas del test de Rorschach, un póster de "Gimme Fuel", una lámina de arte de Pushead, 10 púas de guitarra y bajo, hojas con letras de las canciones y tres pases de gira laminados.</p>
                <p>Además, para celebrar este lanzamiento, la banda ha iniciado el concurso GetTheReLoadOut, invitando a los fans, músicos y artistas visuales a enviar sus propias interpretaciones o covers de los temas del disco. ¡Los afortunados ganadores se llevarán un box set autografiado por la banda!</p>
            </div>
        </div>
    </div>

    <div id="newsModal5" class="modal">
        <div class="modal-content">
            <span class="close-modal">&times;</span>
            <div class="modal-body">
                <h2>🚨 ¡ACTUALIZACIÓN EN LA BATALLA LEGAL: DIMEBAG DARRELL VS. DEAN GUITARS!</h2>
                <p>La larga disputa legal sobre el legado de una de las leyendas más grandes del metal ha tomado un giro decisivo. Un tribunal de Florida acaba de emitir un fallo mayoritariamente a favor de Armadillo Distribution Enterprises, la compañía matriz de Dean Guitars.</p>
                <p>Tras una demanda que inició en 2021 por parte del fideicomiso del guitarrista de Pantera ("In Dime We Trust"), el juez ha desestimado la mayoría de los cargos de fraude, incumplimiento de contrato y disputas de marcas registradas presentados en contra de la marca de instrumentos.</p>
                <p>¿El resultado más importante? Dean Guitars mantiene legalmente el control y la propiedad sobre los derechos, marcas comerciales y diseños de las icónicas guitarras "Stealth" y "Razorback". La corte determinó que la compañía obtuvo estos derechos a través de años de uso previo y actividad comercial de buena fe.</p>
                <p>Pero la pelea no ha terminado por completo... El juez determinó que aún deben resolverse en la corte los reclamos de la herencia de Dimebag sobre una presunta infracción de derechos de autor del gráfico de la guitarra "Dean From Hell" y una acusación de publicidad engañosa por supuestas ventas posteriores al vencimiento de su contrato.</p>
                <p>¿Qué opinas de esta resolución judicial y del futuro del legado de Dimebag? ¡Te leemos en los comentarios!</p>
            </div>
        </div>
    </div>
"""

html = html.replace('</body>', modals_html + '\n</body>')

with open(html_path, 'w') as f:
    f.write(html)

print("News updated and modals restored!")
