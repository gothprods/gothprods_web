import re

html_path = 'index.html'
css_path = 'index.css'

with open(html_path, 'r') as f:
    html = f.read()
    
with open(css_path, 'r') as f:
    css = f.read()

# 1. Update Caos Sonoro #16 to #17
html = html.replace('<h3>CAOS SONORO #16</h3>', '<h3>CAOS SONORO #17</h3>')

# 2. Add clickable links to highlights list for Ultimas Noticias
old_news_list = """                        <ul class="highlight-list">
                            <li>Korn es oficialmente funado y cancela su gira en México.</li>
                            <li>El Knotfest confirma sede y preventa para Diciembre.</li>
                            <li>Black Label Society y Ill Nino cancelan presentaciones en CDMX.</li>
                        </ul>"""

new_news_list = """                        <ul class="highlight-list">
                            <li><a href="javascript:void(0);" data-target="newsModal1" class="open-review-modal" style="color: var(--text-main);">Korn es oficialmente funado y cancela su gira en México.</a></li>
                            <li><a href="javascript:void(0);" data-target="newsModal2" class="open-review-modal" style="color: var(--text-main);">El Knotfest confirma sede y preventa para Diciembre.</a></li>
                            <li><a href="javascript:void(0);" data-target="newsModal3" class="open-review-modal" style="color: var(--text-main);">Black Label Society y Ill Nino cancelan presentaciones en CDMX.</a></li>
                        </ul>"""

html = html.replace(old_news_list, new_news_list)

# 3. Add modals for news
news_modals = """
    <!-- News Modals -->
    <div id="newsModal1" class="modal">
        <div class="modal-content">
            <span class="close-modal">&times;</span>
            <div class="modal-body">
                <h2>KORN ES OFICIALMENTE FUNADO Y CANCELA SU GIRA EN MÉXICO</h2>
                <p>Las recientes controversias y declaraciones han llevado a la cancelación total de la gira de Korn por territorio mexicano. Los organizadores emitieron un comunicado explicando la devolución de entradas y cómo este suceso marca un precedente en la escena nu-metal.</p>
            </div>
        </div>
    </div>
    
    <div id="newsModal2" class="modal">
        <div class="modal-content">
            <span class="close-modal">&times;</span>
            <div class="modal-body">
                <h2>EL KNOTFEST CONFIRMA SEDE Y PREVENTA PARA DICIEMBRE</h2>
                <p>El festival más esperado del año finalmente ha revelado su locación para esta edición de diciembre. Se esperan cabezas de cartel brutales, incluyendo a Bad Omens, Lamb of God y Sylosis. La preventa comenzará la próxima semana.</p>
            </div>
        </div>
    </div>
    
    <div id="newsModal3" class="modal">
        <div class="modal-content">
            <span class="close-modal">&times;</span>
            <div class="modal-body">
                <h2>BLACK LABEL SOCIETY Y ILL NINO CANCELAN PRESENTACIONES EN CDMX</h2>
                <p>Debido a problemas logísticos de última hora y la reestructuración de sus giras mundiales, ambas bandas han anunciado la cancelación de sus fechas en la Ciudad de México. Los promotores aseguran que buscarán reagendar para el 2027.</p>
            </div>
        </div>
    </div>
"""
html = html.replace('</body>', news_modals + '\n</body>')

# 4. Insert new sections between #reviews and #agenda
new_sections = """
        <section id="news" class="section news-section">
            <div class="section-header">
                <h2>Últimas Noticias <span>Del Mes</span></h2>
            </div>
            <div class="news-rail">
                <!-- 10 Noticias -->
                <div class="news-card">
                    <h3>Korn Cancelado</h3>
                    <p>Tras las recientes funas, la banda cancela su visita a México.</p>
                </div>
                <div class="news-card">
                    <h3>Knotfest 2026</h3>
                    <p>Preventa de boletos e información de sede revelada para diciembre.</p>
                </div>
                <div class="news-card">
                    <h3>Black Label Society</h3>
                    <p>Zakk Wylde pospone presentaciones por problemas de logística.</p>
                </div>
                <div class="news-card">
                    <h3>Ill Niño se baja</h3>
                    <p>La banda de nu-metal no pisará la CDMX este año.</p>
                </div>
                <div class="news-card">
                    <h3>Mike Portnoy vuelve</h3>
                    <p>Dream Theater arrasa con su alineación clásica.</p>
                </div>
                <div class="news-card">
                    <h3>Avenged Sevenfold</h3>
                    <p>Nuevo récord de asistencia en el Estadio GNP.</p>
                </div>
                <div class="news-card">
                    <h3>Megadeth en México</h3>
                    <p>Dave Mustaine promete un setlist old-school para mayo.</p>
                </div>
                <div class="news-card">
                    <h3>San Luís Metal Fest</h3>
                    <p>Cartel completo anunciado con bandas nacionales e internacionales.</p>
                </div>
                <div class="news-card">
                    <h3>System Of A Down</h3>
                    <p>La locura armenia regresará con nueva producción escénica.</p>
                </div>
                <div class="news-card">
                    <h3>Candelabrum V</h3>
                    <p>León se prepara para el festival de metal extremo más oscuro del país.</p>
                </div>
            </div>
        </section>

        <section id="under-interviews" class="section interviews-section">
            <div class="section-header">
                <h2>Entrevistas <span>Under</span></h2>
            </div>
            <div class="grid-container">
                <div class="card">
                    <div class="card-image" style="background-image: url('assets/vader_review.jpeg'); background-position: center;"></div>
                    <div class="card-content">
                        <h3>Vader</h3>
                        <p>Hablamos sobre el futuro del death metal polaco y su legado de más de 30 años triturando cráneos.</p>
                        <a href="#live" class="btn-secondary">Leer Entrevista</a>
                    </div>
                </div>
                <div class="card">
                    <div class="card-image" style="background-image: url('assets/dogma_review.jpg'); background-position: top;"></div>
                    <div class="card-content">
                        <h3>Dogma</h3>
                        <p>El misterio, el ocultismo detrás de sus máscaras y el polémico mensaje religioso en su nueva música.</p>
                        <a href="#live" class="btn-secondary">Leer Entrevista</a>
                    </div>
                </div>
                <div class="card">
                    <div class="card-image" style="background-image: url('assets/gutalax_review.jpg'); background-position: center;"></div>
                    <div class="card-content">
                        <h3>Gutalax</h3>
                        <p>Goregrind, toneladas de diversión escatológica, papel higiénico y por qué son la fiesta más brutal.</p>
                        <a href="#live" class="btn-secondary">Leer Entrevista</a>
                    </div>
                </div>
            </div>
        </section>
"""
html = html.replace('<section id="agenda" class="section agenda-section">', new_sections + '\n        <section id="agenda" class="section agenda-section">')

# 5. Append CSS for news-rail
if '.news-rail' not in css:
    css_append = """
/* News Rail Custom Styles */
.news-rail {
    display: flex;
    overflow-x: auto;
    gap: 1.5rem;
    padding-bottom: 1.5rem;
    list-style: none;
    scroll-snap-type: x mandatory;
}

.news-rail::-webkit-scrollbar {
    height: 8px;
}
.news-rail::-webkit-scrollbar-track {
    background: var(--bg-secondary);
    border-radius: 4px;
}
.news-rail::-webkit-scrollbar-thumb {
    background: var(--accent-color);
    border-radius: 4px;
}

.news-card {
    flex: 0 0 300px;
    background-color: var(--bg-secondary);
    border-radius: 8px;
    padding: 1.5rem;
    border-top: 4px solid var(--text-muted);
    scroll-snap-align: start;
    transition: transform 0.3s ease, border-color 0.3s ease;
}

.news-card:hover {
    transform: translateY(-5px);
    border-color: var(--accent-color);
}

.news-card h3 {
    font-size: 1.4rem;
    margin-bottom: 1rem;
    color: var(--text-main);
    font-family: var(--font-heading);
    text-transform: uppercase;
}

.news-card p {
    color: var(--text-muted);
    font-size: 1.1rem;
}
"""
    css += css_append

with open(html_path, 'w') as f:
    f.write(html)
    
with open(css_path, 'w') as f:
    f.write(css)

print("Modifications done!")
