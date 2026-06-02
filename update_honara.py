import re

# 1. Update CSS
css_path = 'index.css'
with open(css_path, 'r') as f:
    css = f.read()

# I will append .interviews-list and update .interview-card-horizontal p
new_css = """
/* Wrapper for all horizontal interviews */
.interviews-list {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem;
}
@media (max-width: 1024px) {
    .interviews-list {
        grid-template-columns: 1fr;
    }
}
"""

if ".interviews-list {" not in css:
    css += new_css

# Update word wrap
css = css.replace('.interview-card-horizontal p {\n    font-size: 1rem;', '.interview-card-horizontal p {\n    font-size: 1rem;\n    overflow-wrap: break-word;\n    word-break: break-word;')

# If the left column (image+meta) is 250px, it might be too small or too big.
# I'll let it be 40% 60%
css = css.replace('grid-template-columns: 250px 1fr;', 'grid-template-columns: minmax(200px, 40%) 1fr;')

with open(css_path, 'w') as f:
    f.write(css)


# 2. Update HTML
html_path = 'index.html'
with open(html_path, 'r') as f:
    html = f.read()

# The placeholder card starts with "<!-- Entrevista 4 (Próximamente) -->"
old_card_pattern = re.compile(r'<!-- Entrevista 4 \(Próximamente\) -->.*?</div>\s*</div>\s*</div>', re.DOTALL)

new_card = """<!-- Honara -->
                <div class="interview-card-horizontal">
                    <div class="interview-left">
                        <div class="card-image" style="background-image: url('https://img.youtube.com/vi/2GDTVHHIRI8/maxresdefault.jpg');"></div>
                        <div class="interview-meta">
                            <span class="badge">27 Nov 2025</span>
                            <h3>Honara</h3>
                        </div>
                    </div>
                    <div class="interview-right">
                        <p>🇪🇸 En este episodio nos sumergimos en la oscuridad luminosa de Honara, la banda de post-metal que está redefiniendo los límites del género con su álbum debut Resemblance (2025) 🌙🔥. Hablamos sobre su fascinante mezcla de folk, sludge, metal progresivo y música clásica 🌌🎸.</p>
                        <div class="episode-actions" style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
                            <a href="https://open.spotify.com/episode/0mYvqOfv9bFtKC9qfEUUjI?si=5a1f8df7da2f47db" target="_blank" class="platform-btn spotify-btn" style="padding: 0.4rem 0.8rem; font-size: 0.9rem;"><i class="fa-brands fa-spotify"></i></a>
                            <a href="https://podcasts.apple.com/mx/podcast/la-galeria-nocturna-podcast/id1606324255?l=en-GB&i=1000738648266" target="_blank" class="platform-btn apple-btn" style="padding: 0.4rem 0.8rem; font-size: 0.9rem;"><i class="fa-solid fa-podcast"></i></a>
                            <a href="https://youtu.be/2GDTVHHIRI8?si=8KE9RntgZXW9CWeq" target="_blank" class="platform-btn" style="padding: 0.4rem 0.8rem; font-size: 0.9rem;"><i class="fa-brands fa-youtube"></i></a>
                        </div>
                    </div>
                </div>"""

# Replace in html
new_html = html.replace(old_card_pattern.search(html).group(0), new_card + "\n            </div>")

with open(html_path, 'w') as f:
    f.write(new_html)

print("HTML and CSS Updated")
