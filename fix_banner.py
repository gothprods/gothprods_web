import re

html_path = 'index.html'
with open(html_path, 'r') as f:
    html = f.read()

# 1. Remove the floating-countdown from the bottom
floating_pattern = re.compile(r'<div class="floating-countdown">.*?</div>\s*<script src="app.js"></script>', re.DOTALL)
html = floating_pattern.sub('<script src="app.js"></script>', html)

# 2. Insert the horizontal banner in the #live section
live_header_pattern = re.compile(r'(<section id="live" class="section shows-section">\s*<div class="section-header">)\s*(<div class="header-titles">.*?</div>)\s*(<div class="header-actions">.*?</div>)', re.DOTALL)

horizontal_banner = """
                <div class="header-titles" style="display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; width: 100%; gap: 2rem;">
                    <div style="display: flex; align-items: center; gap: 1rem;">
                        <img src="assets/Caos_Sonoro.jpg" alt="Caos Sonoro Logo" class="section-logo"
                            style="border-radius: 8px;">
                        <div class="header-text-group">
                            <h2>Caos <span>Sonoro</span></h2>
                            <p class="section-slogan">Aqui hablamos de la industria musical y un poco de metal.</p>
                        </div>
                    </div>
                    
                    <div class="caos-horizontal-banner">
                        <div class="caos-info">
                            <span class="live-badge" style="font-size: 0.7em; padding: 0.3em 0.6em; margin-bottom: 0.2em; display: inline-block;">Próximo En Vivo</span>
                            <h3 style="margin: 0; font-family: 'Oswald', sans-serif; font-size: 1.2rem; text-transform: uppercase;">CAOS SONORO #17</h3>
                            <p style="margin: 0; font-size: 0.85rem; color: var(--text-muted);">29 May | 9:00 PM CST</p>
                        </div>
                        <div class="countdown small-countdown" id="countdown" style="display: flex; gap: 0.5rem; text-align: center;">
                            <div style="background: rgba(255, 255, 255, 0.05); padding: 0.5rem; border-radius: 6px; min-width: 45px; font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase;"><span id="days" style="display: block; font-size: 1.2rem; font-weight: 700; color: var(--accent-color); font-family: 'Oswald', sans-serif;">00</span>d</div>
                            <div style="background: rgba(255, 255, 255, 0.05); padding: 0.5rem; border-radius: 6px; min-width: 45px; font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase;"><span id="hours" style="display: block; font-size: 1.2rem; font-weight: 700; color: var(--accent-color); font-family: 'Oswald', sans-serif;">00</span>h</div>
                            <div style="background: rgba(255, 255, 255, 0.05); padding: 0.5rem; border-radius: 6px; min-width: 45px; font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase;"><span id="minutes" style="display: block; font-size: 1.2rem; font-weight: 700; color: var(--accent-color); font-family: 'Oswald', sans-serif;">00</span>m</div>
                        </div>
                        <a href="https://www.youtube.com/@gothprods" target="_blank" class="btn-primary small-btn" style="padding: 0.6rem 1rem; font-size: 0.8rem; white-space: nowrap;">Activar Recordatorio</a>
                    </div>
                </div>
                <div class="header-actions">
                    <a href="https://open.spotify.com/show/2hnlgkcGNl9GOAPa0WT9HW?si=7e9b95f203464fe6" target="_blank"
                        class="platform-btn spotify-btn"><i class="fa-brands fa-spotify"></i> Spotify</a>
                    <a href="https://podcasts.apple.com/mx/podcast/goth-prods/id1606324255?l=en"
                        target="_blank" class="platform-btn apple-btn"><i class="fa-solid fa-podcast"></i>
                        Apple</a>
                </div>
"""

# Apply the substitution
html = live_header_pattern.sub(r'\1\n' + horizontal_banner, html)

with open(html_path, 'w') as f:
    f.write(html)


# Now fix index.css
css_path = 'index.css'
with open(css_path, 'r') as f:
    css = f.read()

new_css = """
.caos-horizontal-banner {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    background: rgba(10, 10, 10, 0.95);
    border: 1px solid var(--accent-color);
    box-shadow: 0 0 20px rgba(165, 155, 93, 0.2);
    border-radius: 12px;
    padding: 1rem 1.5rem;
    backdrop-filter: blur(10px);
}

@media (max-width: 768px) {
    .caos-horizontal-banner {
        flex-direction: column;
        align-items: flex-start;
        width: 100%;
        gap: 1rem;
    }
    .caos-horizontal-banner .small-btn {
        width: 100%;
        text-align: center;
    }
}
"""

css += new_css

with open(css_path, 'w') as f:
    f.write(css)

print("Horizontal banner implemented successfully.")
