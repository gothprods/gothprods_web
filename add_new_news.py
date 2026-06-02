import re

html_path = 'index.html'
with open(html_path, 'r') as f:
    html = f.read()

# 1. Update Highlight List
old_highlight = """                        <ul class="highlight-list">

                            <li><a href="javascript:void(0);" data-target="newsModal4" class="open-review-modal"
                                    style="color: var(--text-main);"><strong>Metallica:</strong> ¡Épico Box Set Remasterizado de 'ReLoad'!</a></li>
                            <li><a href="javascript:void(0);" data-target="newsModal5" class="open-review-modal"
                                    style="color: var(--text-main);"><strong>Dimebag Darrell:</strong> Actualización en la batalla legal contra Dean Guitars.</a></li>
                            <li><a href="javascript:void(0);" data-target="newsModal1" class="open-review-modal"
                                    style="color: var(--text-main);"><strong>Korn Cancelado:</strong> Tras las recientes controversias, la banda cancela su visita.</a></li>
                        </ul>"""

new_highlight = """                        <ul class="highlight-list">
                            <li><a href="javascript:void(0);" data-target="newsModal1" class="open-review-modal"
                                    style="color: var(--text-main);"><strong>Immortal:</strong> ¡El invierno eterno regresa con su 11º álbum!</a></li>
                            <li><a href="javascript:void(0);" data-target="newsModal2" class="open-review-modal"
                                    style="color: var(--text-main);"><strong>Black Sabbath:</strong> Se abre el baúl de los demos originales.</a></li>
                            <li><a href="javascript:void(0);" data-target="newsModal3" class="open-review-modal"
                                    style="color: var(--text-main);"><strong>Blood Incantation:</strong> Anuncia All Gates Open (Documental y Soundtrack).</a></li>
                        </ul>"""

html = html.replace(old_highlight, new_highlight)

# 2. Rewrite news-rail
rail_pattern = re.compile(r'<div class="news-rail">.*?</div>\s*</section>', re.DOTALL)

new_rail = """<div class="news-rail">
                <div class="news-card">
                    <img src="assets/Immortal_New_Album.png" alt="Immortal New Album" style="width: 100%; border-radius: 8px; margin-bottom: 10px; height: 140px; object-fit: cover; object-position: center;">
                    <h3 style="font-size: 1rem; line-height: 1.2;">¡EL INVIERNO ETERNO REGRESA!</h3>
                    <p style="font-size: 0.85rem; margin-bottom: 10px;">La espera en los reinos de Blashyrkh está por terminar con el 11º álbum de Immortal...</p>
                    <a href="javascript:void(0);" data-target="newsModal1" class="open-review-modal" style="color: var(--accent-color); font-weight: bold; font-size: 0.85rem;">Leer más &rarr;</a>
                </div>
                <div class="news-card">
                    <img src="assets/Black_Sabbath_Archives.png" alt="Black Sabbath Archives" style="width: 100%; border-radius: 8px; margin-bottom: 10px; height: 140px; object-fit: cover; object-position: top center;">
                    <h3 style="font-size: 1rem; line-height: 1.2;">¡EL BAÚL DE SABBATH SE ABRE DE NUEVO!</h3>
                    <p style="font-size: 0.85rem; margin-bottom: 10px;">Sharon Osbourne y el antiguo manager llegan a un acuerdo por los demos originales...</p>
                    <a href="javascript:void(0);" data-target="newsModal2" class="open-review-modal" style="color: var(--accent-color); font-weight: bold; font-size: 0.85rem;">Leer más &rarr;</a>
                </div>
                <div class="news-card">
                    <img src="assets/Blood Incatatation_All Gates Open.png" alt="Blood Incantation All Gates Open" style="width: 100%; border-radius: 8px; margin-bottom: 10px; height: 140px; object-fit: cover; object-position: top center;">
                    <h3 style="font-size: 1rem; line-height: 1.2;">EL COSMOS SE EXPANDE: All Gates Open</h3>
                    <p style="font-size: 0.85rem; margin-bottom: 10px;">La banda más innovadora del death metal psicodélico ha anunciado un lanzamiento doble...</p>
                    <a href="javascript:void(0);" data-target="newsModal3" class="open-review-modal" style="color: var(--accent-color); font-weight: bold; font-size: 0.85rem;">Leer más &rarr;</a>
                </div>
                <div class="news-card">
                    <img src="assets/reload_2.jpg" alt="Metallica ReLoad" style="width: 100%; border-radius: 8px; margin-bottom: 10px; height: 140px; object-fit: cover; object-position: center;">
                    <h3 style="font-size: 1rem; line-height: 1.2;">¡METALLICA ANUNCIA EL ÉPICO BOX SET REMASTERIZADO DE 'RELOAD'!</h3>
                    <p style="font-size: 0.85rem; margin-bottom: 10px;">Metallica ha confirmado el lanzamiento de la edición definitiva y remasterizada de su séptimo álbum...</p>
                    <a href="javascript:void(0);" data-target="newsModal4" class="open-review-modal" style="color: var(--accent-color); font-weight: bold; font-size: 0.85rem;">Leer más &rarr;</a>
                </div>
                <div class="news-card">
                    <img src="assets/dimebag_dean.jpg" alt="Dimebag Dean Guitars" style="width: 100%; border-radius: 8px; margin-bottom: 10px; height: 140px; object-fit: cover; object-position: top center; background: #222;">
                    <h3 style="font-size: 1rem; line-height: 1.2;">¡ACTUALIZACIÓN EN LA BATALLA LEGAL: DIMEBAG DARRELL VS. DEAN GUITARS!</h3>
                    <p style="font-size: 0.85rem; margin-bottom: 10px;">La larga disputa legal sobre el legado de una de las leyendas más grandes del metal ha tomado un giro decisivo...</p>
                    <a href="javascript:void(0);" data-target="newsModal5" class="open-review-modal" style="color: var(--accent-color); font-weight: bold; font-size: 0.85rem;">Leer más &rarr;</a>
                </div>
            </div>
        </section>"""

html = rail_pattern.sub(new_rail, html)

# 3. Replace old newsModal1-3 with new ones
modals_pattern = re.compile(r'<div id="newsModal1" class="modal">.*?<div id="newsModal4" class="modal">', re.DOTALL)

new_modals = """<div id="newsModal1" class="modal">
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

    <div id="newsModal2" class="modal">
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

    <div id="newsModal3" class="modal">
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

    <div id="newsModal4" class="modal">"""

html = modals_pattern.sub(new_modals, html)

with open(html_path, 'w') as f:
    f.write(html)

print("Added new news and cleared placeholders!")
