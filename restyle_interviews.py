import re

# 1. Update CSS
css_path = 'index.css'
with open(css_path, 'r') as f:
    css = f.read()

new_css = """
/* Horizontal Interview Card Styles */
.interview-card-horizontal {
    display: grid;
    grid-template-columns: 250px 1fr;
    background-color: var(--bg-secondary);
    border-radius: 8px;
    overflow: hidden;
    border-left: 4px solid var(--accent-color);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
    margin-bottom: 1.5rem;
    transition: transform 0.3s ease;
}

.interview-card-horizontal:hover {
    transform: translateY(-5px);
}

.interview-card-horizontal .interview-left {
    position: relative;
    display: flex;
    flex-direction: column;
}

.interview-card-horizontal .card-image {
    height: 180px;
    background-size: cover;
    background-position: center;
}

.interview-card-horizontal .interview-meta {
    padding: 1rem;
    background: rgba(0, 0, 0, 0.6);
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.interview-card-horizontal h3 {
    margin: 0;
    font-size: 1.5rem;
    color: var(--accent-color);
    text-transform: uppercase;
}

.interview-card-horizontal .badge {
    margin-bottom: 0.5rem;
    display: inline-block;
    align-self: flex-start;
}

.interview-card-horizontal .interview-right {
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.interview-card-horizontal p {
    font-size: 1rem;
    line-height: 1.6;
    color: var(--text-muted);
    margin: 0 0 1rem 0;
}

@media (max-width: 768px) {
    .interview-card-horizontal {
        grid-template-columns: 1fr;
    }
}
"""

if "interview-card-horizontal" not in css:
    with open(css_path, 'a') as f:
        f.write("\n" + new_css)

# 2. Update HTML
html_path = 'index.html'
with open(html_path, 'r') as f:
    html = f.read()

old_grid_pattern = re.compile(r'<div class="grid-container">(.*?)</div>\s*</section>', re.DOTALL)

# Let's write the new HTML directly:
new_html_content = """
            <div class="interviews-list">
                <!-- Ominum -->
                <div class="interview-card-horizontal">
                    <div class="interview-left">
                        <div class="card-image" style="background-image: url('https://img.youtube.com/vi/ZxZ2Uht40bA/maxresdefault.jpg');"></div>
                        <div class="interview-meta">
                            <span class="badge">19 Feb 2026</span>
                            <h3>Ominum</h3>
                        </div>
                    </div>
                    <div class="interview-right">
                        <p>🇸🇪 This Galeria Nocturna episode explores the history and discography of Ominum, a thrash metal band from Gothenburg, Sweden. Founded in 2018 by core members Erik Lindstrand and Bernard Jozic.</p>
                        <div class="episode-actions" style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
                            <a href="https://open.spotify.com/episode/2PS8JA3xPQFe8U2N71vb4R?si=aa133476aac3499b" target="_blank" class="platform-btn spotify-btn" style="padding: 0.4rem 0.8rem; font-size: 0.9rem;"><i class="fa-brands fa-spotify"></i></a>
                            <a href="https://podcasts.apple.com/mx/podcast/la-galeria-nocturna-podcast/id1606324255?l=en-GB&i=1000750459376" target="_blank" class="platform-btn apple-btn" style="padding: 0.4rem 0.8rem; font-size: 0.9rem;"><i class="fa-solid fa-podcast"></i></a>
                            <a href="https://youtu.be/ZxZ2Uht40bA?si=olJlpFeGqLNfdkUW" target="_blank" class="platform-btn" style="padding: 0.4rem 0.8rem; font-size: 0.9rem;"><i class="fa-brands fa-youtube"></i></a>
                        </div>
                    </div>
                </div>

                <!-- Athica -->
                <div class="interview-card-horizontal">
                    <div class="interview-left">
                        <div class="card-image" style="background-image: url('https://img.youtube.com/vi/RjHD5Jtx4sM/maxresdefault.jpg');"></div>
                        <div class="interview-meta">
                            <span class="badge">30 Ene 2026</span>
                            <h3>Athica</h3>
                        </div>
                    </div>
                    <div class="interview-right">
                        <p>Nos adentramos en la historia de Athica, poderosa banda de metal originaria de Panamá desde 2003. Exploramos su evolución creativa plasmada en sus tres álbumes de estudio.</p>
                        <div class="episode-actions" style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
                            <a href="https://open.spotify.com/episode/00w9KH6dmibQB6h6GczWva?si=198b529a67e14627" target="_blank" class="platform-btn spotify-btn" style="padding: 0.4rem 0.8rem; font-size: 0.9rem;"><i class="fa-brands fa-spotify"></i></a>
                            <a href="https://podcasts.apple.com/mx/podcast/la-galeria-nocturna-podcast/id1606324255?l=en-GB&i=1000747281379" target="_blank" class="platform-btn apple-btn" style="padding: 0.4rem 0.8rem; font-size: 0.9rem;"><i class="fa-solid fa-podcast"></i></a>
                            <a href="https://youtu.be/RjHD5Jtx4sM?si=2H7izSgIEQWLlTBB" target="_blank" class="platform-btn" style="padding: 0.4rem 0.8rem; font-size: 0.9rem;"><i class="fa-brands fa-youtube"></i></a>
                        </div>
                    </div>
                </div>

                <!-- Stay Design -->
                <div class="interview-card-horizontal">
                    <div class="interview-left">
                        <div class="card-image" style="background-image: url('https://img.youtube.com/vi/RjHD5Jtx4sM/maxresdefault.jpg');"></div>
                        <div class="interview-meta">
                            <span class="badge">11 Ene 2026</span>
                            <h3>Stay Design</h3>
                        </div>
                    </div>
                    <div class="interview-right">
                        <p>Conversamos sobre los hitos que han definido su carrera, destacando su histórica participación en el Wacken Open Air en 2019, donde se consagraron como la primera agrupación panameña.</p>
                        <div class="episode-actions" style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
                            <a href="https://open.spotify.com/episode/1GCf4eU2rpnZrvdpwtlYvz?si=4946680075df47e4" target="_blank" class="platform-btn spotify-btn" style="padding: 0.4rem 0.8rem; font-size: 0.9rem;"><i class="fa-brands fa-spotify"></i></a>
                            <a href="https://podcasts.apple.com/mx/podcast/la-galeria-nocturna-podcast/id1606324255?l=en-GB&i=1000744664082" target="_blank" class="platform-btn apple-btn" style="padding: 0.4rem 0.8rem; font-size: 0.9rem;"><i class="fa-solid fa-podcast"></i></a>
                            <a href="https://youtu.be/RjHD5Jtx4sM?si=BhmmGOLS7WL6-MR5" target="_blank" class="platform-btn" style="padding: 0.4rem 0.8rem; font-size: 0.9rem;"><i class="fa-brands fa-youtube"></i></a>
                        </div>
                    </div>
                </div>

                <!-- Entrevista 4 (Próximamente) -->
                <div class="interview-card-horizontal">
                    <div class="interview-left">
                        <div class="card-image" style="background-image: url('assets/vader_review.jpeg');"></div>
                        <div class="interview-meta">
                            <span class="badge">Próximamente</span>
                            <h3>Banda Under</h3>
                        </div>
                    </div>
                    <div class="interview-right">
                        <p>Espacio reservado para la próxima gran entrevista de La Galería Nocturna. ¡Mantente atento a nuestras redes sociales para descubrir quién será nuestro siguiente invitado de la escena underground mundial!</p>
                        <div class="episode-actions" style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
                            <a href="#" class="platform-btn spotify-btn" style="padding: 0.4rem 0.8rem; font-size: 0.9rem; opacity: 0.5; pointer-events: none;"><i class="fa-brands fa-spotify"></i></a>
                            <a href="#" class="platform-btn apple-btn" style="padding: 0.4rem 0.8rem; font-size: 0.9rem; opacity: 0.5; pointer-events: none;"><i class="fa-solid fa-podcast"></i></a>
                            <a href="#" class="platform-btn" style="padding: 0.4rem 0.8rem; font-size: 0.9rem; opacity: 0.5; pointer-events: none;"><i class="fa-brands fa-youtube"></i></a>
                        </div>
                    </div>
                </div>
            </div>
"""

# Now replace <div class="grid-container">...</div> with the new content
new_html = html.replace(old_grid_pattern.search(html).group(0), new_html_content + "\n        </section>")

with open(html_path, 'w') as f:
    f.write(new_html)

print("Done")
