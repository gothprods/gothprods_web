import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Update the highlight list in El Pit
highlight_pattern = re.compile(r'<ul class="highlight-list">.*?</ul>\s*<a href="#news"', re.DOTALL)
new_highlight = """<ul class="highlight-list">
                            <li><a href="javascript:void(0);" data-target="newsModal1" class="open-review-modal"
                                    style="color: var(--text-main);"><strong>Metallica:</strong> ¡Épico Box Set Remasterizado de 'ReLoad'!</a></li>
                            <li><a href="javascript:void(0);" data-target="newsModal2" class="open-review-modal"
                                    style="color: var(--text-main);"><strong>Dimebag Darrell:</strong> Actualización en la batalla legal contra Dean Guitars.</a></li>
                            <li><a href="javascript:void(0);" data-target="newsModal3" class="open-review-modal"
                                    style="color: var(--text-main);"><strong>Immortal:</strong> ¡El invierno eterno regresa con su 11º álbum!</a></li>
                        </ul>
                        <a href="#news\""""
html = highlight_pattern.sub(new_highlight, html)

# 2. Rewrite the news-rail
rail_pattern = re.compile(r'<div class="news-rail">.*?</div>\s*</section>', re.DOTALL)
new_rail = """<div class="news-rail">
                <div class="news-card">
                    <img src="assets/reload_2.jpg" alt="Metallica ReLoad" style="width: 100%; border-radius: 8px; margin-bottom: 10px; height: 140px; object-fit: cover; object-position: center;">
                    <h3 style="font-size: 1rem; line-height: 1.2;">¡METALLICA ANUNCIA EL ÉPICO BOX SET REMASTERIZADO DE 'RELOAD'!</h3>
                    <p style="font-size: 0.85rem; margin-bottom: 10px;">Metallica ha confirmado el lanzamiento de la edición definitiva y remasterizada de su séptimo álbum...</p>
                    <a href="javascript:void(0);" data-target="newsModal1" class="open-review-modal" style="color: var(--accent-color); font-weight: bold; font-size: 0.85rem;">Leer más &rarr;</a>
                </div>
                <div class="news-card">
                    <img src="assets/dimebag_dean.jpg" alt="Dimebag Dean Guitars" style="width: 100%; border-radius: 8px; margin-bottom: 10px; height: 140px; object-fit: cover; object-position: top center; background: #222;">
                    <h3 style="font-size: 1rem; line-height: 1.2;">¡ACTUALIZACIÓN EN LA BATALLA LEGAL: DIMEBAG DARRELL VS. DEAN GUITARS!</h3>
                    <p style="font-size: 0.85rem; margin-bottom: 10px;">La larga disputa legal sobre el legado de una de las leyendas más grandes del metal ha tomado un giro decisivo...</p>
                    <a href="javascript:void(0);" data-target="newsModal2" class="open-review-modal" style="color: var(--accent-color); font-weight: bold; font-size: 0.85rem;">Leer más &rarr;</a>
                </div>
                <div class="news-card">
                    <img src="assets/Immortal_New_Album.png" alt="Immortal New Album" style="width: 100%; border-radius: 8px; margin-bottom: 10px; height: 140px; object-fit: cover; object-position: center;">
                    <h3 style="font-size: 1rem; line-height: 1.2;">¡EL INVIERNO ETERNO REGRESA!</h3>
                    <p style="font-size: 0.85rem; margin-bottom: 10px;">La espera en los reinos de Blashyrkh está por terminar con el 11º álbum de Immortal...</p>
                    <a href="javascript:void(0);" data-target="newsModal3" class="open-review-modal" style="color: var(--accent-color); font-weight: bold; font-size: 0.85rem;">Leer más &rarr;</a>
                </div>
                <div class="news-card">
                    <img src="assets/Black_Sabbath_Archives.png" alt="Black Sabbath Archives" style="width: 100%; border-radius: 8px; margin-bottom: 10px; height: 140px; object-fit: cover; object-position: top center;">
                    <h3 style="font-size: 1rem; line-height: 1.2;">¡EL BAÚL DE SABBATH SE ABRE DE NUEVO!</h3>
                    <p style="font-size: 0.85rem; margin-bottom: 10px;">Sharon Osbourne y el antiguo manager llegan a un acuerdo por los demos originales...</p>
                    <a href="javascript:void(0);" data-target="newsModal4" class="open-review-modal" style="color: var(--accent-color); font-weight: bold; font-size: 0.85rem;">Leer más &rarr;</a>
                </div>
                <div class="news-card">
                    <img src="assets/Blood Incatatation_All Gates Open.png" alt="Blood Incantation All Gates Open" style="width: 100%; border-radius: 8px; margin-bottom: 10px; height: 140px; object-fit: cover; object-position: top center;">
                    <h3 style="font-size: 1rem; line-height: 1.2;">EL COSMOS SE EXPANDE: All Gates Open</h3>
                    <p style="font-size: 0.85rem; margin-bottom: 10px;">La banda más innovadora del death metal psicodélico ha anunciado un lanzamiento doble...</p>
                    <a href="javascript:void(0);" data-target="newsModal5" class="open-review-modal" style="color: var(--accent-color); font-weight: bold; font-size: 0.85rem;">Leer más &rarr;</a>
                </div>
            </div>
        </section>"""
html = rail_pattern.sub(new_rail, html)

# 3. Replace all existing news modals with the new set of 5
# I will find everything from <script src="app.js"></script> to the end, and rewrite it.
end_pattern = re.compile(r'<script src="app.js"></script>.*', re.DOTALL)
new_end = """<script src="app.js"></script>

    <!-- News Modals -->
    <div id="newsModal1" class="modal">
        <div class="modal-content">
            <span class="close-modal">&times;</span>
            <img src="assets/reload_2.jpg" alt="Metallica ReLoad" class="modal-banner" style="object-position: center;">
            <div class="modal-body">
                <h2>¡METALLICA ANUNCIA EL ÉPICO BOX SET REMASTERIZADO DE 'RELOAD'!</h2>
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

    <div id="newsModal2" class="modal">
        <div class="modal-content">
            <span class="close-modal">&times;</span>
            <img src="assets/dimebag_dean.jpg" alt="Dimebag Dean Guitars" class="modal-banner" style="object-position: top center;">
            <div class="modal-body">
                <h2>¡ACTUALIZACIÓN EN LA BATALLA LEGAL: DIMEBAG DARRELL VS. DEAN GUITARS!</h2>
                <p>La larga disputa legal sobre el legado de una de las leyendas más grandes del metal ha tomado un giro decisivo. Un tribunal de Florida acaba de emitir un fallo mayoritariamente a favor de Armadillo Distribution Enterprises, la compañía matriz de Dean Guitars.</p>
                <p>Tras una demanda que inició en 2021 por parte del fideicomiso del guitarrista de Pantera ("In Dime We Trust"), el juez ha desestimado la mayoría de los cargos de fraude, incumplimiento de contrato y disputas de marcas registradas presentados en contra de la marca de instrumentos.</p>
                <p>¿El resultado más importante? Dean Guitars mantiene legalmente el control y la propiedad sobre los derechos, marcas comerciales y diseños de las icónicas guitarras "Stealth" y "Razorback". La corte determinó que la compañía obtuvo estos derechos a través de años de uso previo y actividad comercial de buena fe.</p>
                <p>Pero la pelea no ha terminado por completo... El juez determinó que aún deben resolverse en la corte los reclamos de la herencia de Dimebag sobre una presunta infracción de derechos de autor del gráfico de la guitarra "Dean From Hell" y una acusación de publicidad engañosa por supuestas ventas posteriores al vencimiento de su contrato.</p>
                <p>¿Qué opinas de esta resolución judicial y del futuro del legado de Dimebag? ¡Te leemos en los comentarios!</p>
            </div>
        </div>
    </div>

    <div id="newsModal3" class="modal">
        <div class="modal-content">
            <span class="close-modal">&times;</span>
            <img src="assets/Immortal_New_Album.png" alt="Immortal New Album" class="modal-banner" style="object-position: center;">
            <div class="modal-body">
                <h2>¡EL INVIERNO ETERNO REGRESA!</h2>
                <p>La espera en los reinos de Blashyrkh está por terminar. @immortalofficial confirmó que el proceso de composición de su 11º álbum de estudio ha finalizado.</p>
                <p>Tras el demoledor War Against All, Demonaz promete un nuevo asalto de metal gélido y riffs veloces. Aunque el misterio sobre quiénes acompañarán a Demonaz en la ejecución sigue en el aire, una cosa es segura: la tormenta se acerca.</p>
                <p>Esperemos un poco mas hacia finales de 2026 o quiza inicios del 2027.</p>
            </div>
        </div>
    </div>

    <div id="newsModal4" class="modal">
        <div class="modal-content">
            <span class="close-modal">&times;</span>
            <img src="assets/Black_Sabbath_Archives.png" alt="Black Sabbath Archives" class="modal-banner" style="object-position: top center;">
            <div class="modal-body">
                <h2>¡EL BAÚL DE SABBATH SE ABRE DE NUEVO!</h2>
                <p>Después de años de batallas legales, Sharon Osbourne y el antiguo manager de Black Sabbath han llegado a un acuerdo por los derechos de algunos de sus demos originales. ¿Qué significa esto para nosotros?</p>
                <p>No son simples remasterizaciones; estamos hablando de las grabaciones más primitivas y puras de la banda, ¡el material con el que inventaron el Heavy Metal! ✨</p>
                <p>Prepárate!!! quizá en algun momentos podamos escuchar la génesis de La historia del rock acaba de recuperar una pieza clave de su rompecabezas.</p>
            </div>
        </div>
    </div>

    <div id="newsModal5" class="modal">
        <div class="modal-content">
            <span class="close-modal">&times;</span>
            <img src="assets/Blood Incatatation_All Gates Open.png" alt="Blood Incantation All Gates Open" class="modal-banner" style="object-position: top center;">
            <div class="modal-body">
                <h2>EL COSMOS SE EXPANDE: All Gates Open</h2>
                <p>Si pensabas que habías visto todo el universo de @bloodincantationofficial , prepárate para ir más allá. La banda más innovadora del death metal psicodélico ha anunciado "All Gates Open", un lanzamiento doble que incluye:</p>
                <p>🎥 Un documental: Una mirada profunda a su proceso creativo y evolución sonora.</p>
                <p>🎹 Banda sonora original: Nueva música para acompañar tu viaje astral. Esperalo el 5 de Junio de 2026</p>
                <p>El portal está listo. ¿Te atreves a cruzarlo?</p>
            </div>
        </div>
    </div>

</body>
</html>"""
html = end_pattern.sub(new_end, html)

with open('index.html', 'w') as f:
    f.write(html)

print("Done reordering and finalizing news.")
