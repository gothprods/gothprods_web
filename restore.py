import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find the start of the reviews section
match = re.search(r'<section id="reviews" class="section reviews-section">', html)
if match:
    # Keep everything before the reviews section
    html = html[:match.start()]

# Now append the fully dynamic sections!
dynamic_sections = """        <section id="reviews" class="section reviews-section">
            <div class="section-header">
                <h2>Reseñas de <span>Conciertos</span></h2>
            </div>
            <div class="news-rail">
                {% for item in reseñas_items %}
                <div class="news-card">
                    <img src="{{ item.image_filename if item.image_filename.startswith('http') or item.image_filename.startswith('assets') else 'updates/' + item.image_filename }}" style="width: 100%; border-radius: 8px; margin-bottom: 10px; height: 140px; object-fit: cover; object-position: center;">
                    <h3 style="font-size: 1rem; line-height: 1.2;">{{ item.title }}</h3>
                    <p style="font-size: 0.85rem; margin-bottom: 10px;">{{ item.short_desc }}</p>
                    <a href="javascript:void(0);" data-target="dynNewsModal{{ item.id }}" class="open-review-modal" style="color: var(--accent-color); font-weight: bold; font-size: 0.85rem;">Leer reseña completa &rarr;</a>
                </div>
                {% endfor %}
            </div>
        </section>

        <section id="news" class="section news-section">
            <div class="section-header">
                <h2>El Noticiero <span>Nocturno</span></h2>
            </div>
            <div class="news-rail">
                {% for item in noticiero_items %}
                <div class="news-card">
                    <img src="{{ item.image_filename if item.image_filename.startswith('http') or item.image_filename.startswith('assets') else 'updates/' + item.image_filename }}" style="width: 100%; border-radius: 8px; margin-bottom: 10px; height: 140px; object-fit: cover; object-position: center;">
                    <h3 style="font-size: 1rem; line-height: 1.2;">{{ item.title }}</h3>
                    <p style="font-size: 0.85rem; margin-bottom: 10px;">{{ item.short_desc }}</p>
                    <a href="javascript:void(0);" data-target="dynNewsModal{{ item.id }}" class="open-review-modal" style="color: var(--accent-color); font-weight: bold; font-size: 0.85rem;">Leer más &rarr;</a>
                </div>
                {% endfor %}
            </div>
        </section>

        <section id="under-interviews" class="section interviews-section">
            <div class="section-header">
                <h2>Entrevistas <span>Under</span></h2>
            </div>
            <div class="news-rail">
                {% for item in entrevistas_items %}
                <div class="news-card">
                    <img src="{{ item.image_filename if item.image_filename.startswith('http') or item.image_filename.startswith('assets') else 'updates/' + item.image_filename }}" style="width: 100%; border-radius: 8px; margin-bottom: 10px; height: 140px; object-fit: cover; object-position: center;">
                    <h3 style="font-size: 1rem; line-height: 1.2;">{{ item.title }}</h3>
                    <p style="font-size: 0.85rem; margin-bottom: 10px;">{{ item.short_desc }}</p>
                    <a href="javascript:void(0);" data-target="dynNewsModal{{ item.id }}" class="open-review-modal" style="color: var(--accent-color); font-weight: bold; font-size: 0.85rem;">Ver entrevista &rarr;</a>
                </div>
                {% endfor %}
            </div>
        </section>

        <section id="agenda" class="section agenda-section">
            <div class="section-header">
                <h2>Agenda <span>Metalera 2026</span></h2>
            </div>
            <div class="agenda-month">
                <ul class="agenda-list">
                    {% for item in agenda_items %}
                    <li class="agenda-item">
                        <img src="assets/viking.jpg" alt="Goth Prods Crew" class="agenda-viking-badge" title="El Crew de Goth Prods asistirá">
                        <img src="{{ item.image_filename if item.image_filename.startswith('http') or item.image_filename.startswith('assets') else 'updates/' + item.image_filename }}" alt="Logo" class="agenda-logo" style="width: 50px; height: 50px; object-fit: contain;">
                        <div class="agenda-date"><span class="month" style="font-size: 0.8rem;">{{ item.full_desc }}</span></div>
                        <div class="agenda-details">
                            <h3>{{ item.title }}</h3>
                            <p>{{ item.short_desc }}</p>
                        </div>
                    </li>
                    {% endfor %}
                </ul>
            </div>
        </section>

        <section id="contact" class="section contact-section">
            <div class="section-header">
                <h2>Únete al <span>Culto</span></h2>
            </div>
            <form class="contact-form">
                <input type="text" placeholder="Nombre (o apodo en el pit)" required>
                <input type="email" placeholder="Correo Electrónico" required>
                <textarea placeholder="¿Qué banda deberíamos reseñar? ¿Tienes un proyecto under? Escríbenos..." rows="5" required></textarea>
                <button type="submit" class="btn-primary">ENVIAR MENSAJE</button>
            </form>
        </section>
    </main>

    <footer>
        <div class="footer-content">
            <img src="assets/logo.png" alt="Goth Prods Logo" class="footer-logo">
            <p>Goth Productions es una productora y creadora de contenidos enfocados al género más feroz del planeta.</p>
            <div class="footer-socials">
                <a href="https://www.tiktok.com/@goth_prods" target="_blank"><i class="fa-brands fa-tiktok"></i></a>
                <a href="https://www.facebook.com/Goth-Prods-104237088306624/" target="_blank"><i class="fa-brands fa-facebook-f"></i></a>
                <a href="https://www.instagram.com/goth_prods/" target="_blank"><i class="fa-brands fa-instagram"></i></a>
                <a href="https://www.youtube.com/@gothprods44" target="_blank"><i class="fa-brands fa-youtube"></i></a>
                <a href="https://podcasts.apple.com/mx/podcast/goth-prods/id1606324255?l=en" target="_blank"><i class="fa-solid fa-podcast"></i></a>
                <a href="https://open.spotify.com/show/2hnlgkcGNl9GOAPa0WT9HW?si=7e9b95f203464fe6" target="_blank"><i class="fa-brands fa-spotify"></i></a>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2026 Goth Productions. Todos los derechos reservados.</p>
        </div>
    </footer>

    {% for items_list in [noticiero_items, reseñas_items, entrevistas_items, agenda_items] %}
    {% for item in items_list %}
    <!-- Modal Dinámico -->
    <div id="dynNewsModal{{ item.id }}" class="modal">
        <div class="modal-content">
            <span class="close-modal">&times;</span>
            <h2 style="color: var(--accent-color); margin-bottom: 20px;">{{ item.title }}</h2>
            <img src="{{ item.image_filename if item.image_filename.startswith('http') or item.image_filename.startswith('assets') else 'updates/' + item.image_filename }}" style="width: 100%; border-radius: 8px; margin-bottom: 20px;">
            <div style="color: #ccc; line-height: 1.6; white-space: pre-line;">
                {{ item.full_desc }}
                
                <br><br>
                {% if item.yt_link %}<a href="{{ item.yt_link }}" target="_blank" style="color:#ff0000; margin-right:15px;"><i class="fa-brands fa-youtube"></i> YouTube</a>{% endif %}
                {% if item.sp_link %}<a href="{{ item.sp_link }}" target="_blank" style="color:#1DB954; margin-right:15px;"><i class="fa-brands fa-spotify"></i> Spotify</a>{% endif %}
                {% if item.ap_link %}<a href="{{ item.ap_link }}" target="_blank" style="color:#aa00ff;"><i class="fa-solid fa-podcast"></i> Apple Podcast</a>{% endif %}
                {% if item.author %}<p style="margin-top: 15px; font-size: 0.8rem; color: #888;">Por: {{ item.author }}</p>{% endif %}
            </div>
        </div>
    </div>
    {% endfor %}
    {% endfor %}

    <script src="app.js"></script>
</body>
</html>
"""

html += dynamic_sections

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("done")
