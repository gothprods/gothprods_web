import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update El Pit (Highlights)
pit_content = """        <section id="highlights" class="section highlights-section">
            <div class="section-header">
                <h2>El <span>Pit</span></h2>
            </div>
            <div class="grid-container highlights-grid">

                <!-- Agenda del mes -->
                <div class="card highlight-card">
                    <img src="assets/banner_new.jpg" style="width: 100%; border-radius: 8px; margin-bottom: 10px; height: 140px; object-fit: cover; object-position: center;">
                    <h3><i class="fa-solid fa-calendar-days"></i> Agenda Reciente</h3>
                    <ul class="highlight-list">
                        {% for item in agenda_items[:5] %}
                        <li><strong>{{ item.title }}:</strong> {{ item.short_desc }}</li>
                        {% endfor %}
                    </ul>
                    <a href="#agenda" class="read-more" style="color: var(--accent-color); font-weight: bold; margin-top:1rem; display:block;">Ver Agenda Completa &rarr;</a>
                </div>

                <!-- Últimas Noticias / Noticiero Nocturno -->
                <div class="card highlight-card">
                    <img src="assets/reload_2.jpg" style="width: 100%; border-radius: 8px; margin-bottom: 10px; height: 140px; object-fit: cover; object-position: center;">
                    <h3><i class="fa-solid fa-newspaper"></i> El Noticiero Nocturno</h3>
                    <ul class="highlight-list">
                        {% for item in noticiero_items[:3] %}
                        <li><a href="javascript:void(0);" data-target="dynNewsModal{{ item.id }}" class="open-review-modal" style="color: var(--text-main);"><strong>{{ item.title }}:</strong> {{ item.short_desc[:40] }}...</a></li>
                        {% endfor %}
                    </ul>
                    <a href="#news" class="read-more" style="color: var(--accent-color); font-weight: bold; margin-top:1rem; display:block;">Ir al Noticiero &rarr;</a>
                </div>

                <!-- Reviews Recientes -->
                <div class="card highlight-card">
                    <img src="assets/dream_theater_horizontal.jpg" style="width: 100%; border-radius: 8px; margin-bottom: 10px; height: 140px; object-fit: cover; object-position: center;">
                    <h3><i class="fa-solid fa-pen-to-square"></i> Reseñas Recientes</h3>
                    <ul class="highlight-list">
                        {% for item in reseñas_items[:3] %}
                        <li><a href="javascript:void(0);" data-target="dynNewsModal{{ item.id }}" class="open-review-modal" style="color: var(--text-main);"><strong>{{ item.title }}</strong></a></li>
                        {% endfor %}
                    </ul>
                    <a href="#reviews" class="read-more" style="color: var(--accent-color); font-weight: bold; margin-top:1rem; display:block;">Leer Reseñas &rarr;</a>
                </div>

                <!-- Entrevistas Under -->
                <div class="card highlight-card">
                    <img src="https://img.youtube.com/vi/2GDTVHHIRI8/maxresdefault.jpg" style="width: 100%; border-radius: 8px; margin-bottom: 10px; height: 140px; object-fit: cover; object-position: center;">
                    <h3><i class="fa-solid fa-microphone"></i> Entrevistas Under</h3>
                    <ul class="highlight-list">
                        {% for item in entrevistas_items[:3] %}
                        <li><a href="javascript:void(0);" data-target="dynNewsModal{{ item.id }}" class="open-review-modal" style="color: var(--text-main);"><strong>{{ item.title }}</strong></a></li>
                        {% endfor %}
                    </ul>
                    <a href="#under-interviews" class="read-more" style="color: var(--accent-color); font-weight: bold; margin-top:1rem; display:block;">Ver Entrevistas &rarr;</a>
                </div>

            </div>
        </section>"""

html = re.sub(r'<section id="highlights" class="section highlights-section">.*?</section>', pit_content, html, flags=re.DOTALL)

# 2. Update Reseñas Carousel
reseñas_content = """            <div class="news-rail">
                {% for item in reseñas_items %}
                <div class="news-card">
                    <img src="{{ item.image_filename if item.image_filename.startswith('http') or item.image_filename.startswith('assets') else 'updates/' + item.image_filename }}" style="width: 100%; border-radius: 8px; margin-bottom: 10px; height: 140px; object-fit: cover; object-position: center;">
                    <h3 style="font-size: 1rem; line-height: 1.2;">{{ item.title }}</h3>
                    <p style="font-size: 0.85rem; margin-bottom: 10px;">{{ item.short_desc }}</p>
                    <a href="javascript:void(0);" data-target="dynNewsModal{{ item.id }}" class="open-review-modal" style="color: var(--accent-color); font-weight: bold; font-size: 0.85rem;">Leer más &rarr;</a>
                </div>
                {% endfor %}
"""
html = re.sub(r'<div class="news-rail">\s*<img src="assets/architects_review.jpg"', reseñas_content + r'                <img src="assets/architects_review.jpg"', html, count=1)

# 3. Update Entrevistas Carousel
entrevistas_content = """            <div class="news-rail">
                {% for item in entrevistas_items %}
                <div class="news-card">
                    <img src="{{ item.image_filename if item.image_filename.startswith('http') or item.image_filename.startswith('assets') else 'updates/' + item.image_filename }}" style="width: 100%; border-radius: 8px; margin-bottom: 10px; height: 140px; object-fit: cover; object-position: center;">
                    <h3 style="font-size: 1rem; line-height: 1.2;">{{ item.title }}</h3>
                    <p style="font-size: 0.85rem; margin-bottom: 10px;">{{ item.short_desc }}</p>
                    <a href="javascript:void(0);" data-target="dynNewsModal{{ item.id }}" class="open-review-modal" style="color: var(--accent-color); font-weight: bold; font-size: 0.85rem;">Leer más &rarr;</a>
                </div>
                {% endfor %}
"""
html = re.sub(r'<div class="news-rail">\s*<!-- Ominum -->', entrevistas_content + r'                <!-- Ominum -->', html, count=1)

# 4. Modals for everything!
# We'll just loop over ALL items from all sections for simplicity at the bottom
modals_replacement = """    {% for items_list in [noticiero_items, reseñas_items, entrevistas_items, agenda_items] %}
    {% for item in items_list %}
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
                <p style="margin-top: 15px; font-size: 0.8rem; color: #888;">Por: {{ item.author }}</p>
            </div>
        </div>
    </div>
    {% endfor %}
    {% endfor %}
    </body>"""

html = re.sub(r'{% for item in noticiero_items %}.*?{% endfor %}\s*</body>', modals_replacement, html, flags=re.DOTALL)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("done")
