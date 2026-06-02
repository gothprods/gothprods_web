import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

def get_jinja(variable_name, yt_fallback):
    sp_fallback = "https://open.spotify.com/show/2hnlgkcGNl9GOAPa0WT9HW?si=7e9b95f203464fe6"
    ap_fallback = "https://podcasts.apple.com/mx/podcast/goth-prods/id1606324255?l=en"
    
    return f"""            <div class="news-rail">
                {{% for item in {variable_name} %}}
                <div class="news-card">
                    <img src="{{{{ item.image_filename if item.image_filename and (item.image_filename.startswith('http') or item.image_filename.startswith('assets')) else 'updates/' + item.image_filename if item.image_filename else 'assets/logo.png' }}}}" style="width: 100%; border-radius: 8px; margin-bottom: 10px; height: 140px; object-fit: cover; object-position: center;">
                    <div class="card-content">
                        <h3 style="font-size: 1rem; line-height: 1.2;">{{{{ item.title }}}}</h3>
                        <p style="font-size: 0.85rem; margin-bottom: 10px;">{{{{ item.short_desc[:120] if item.short_desc else '' }}}}...</p>
                        <div class="episode-actions" style="margin-top: 15px;">
                            <a href="{{{{ item.sp_link if item.sp_link else '{sp_fallback}' }}}}" target="_blank" class="platform-btn spotify-btn"><i class="fa-brands fa-spotify"></i> Spotify</a>
                            <a href="{{{{ item.ap_link if item.ap_link else '{ap_fallback}' }}}}" target="_blank" class="platform-btn apple-btn"><i class="fa-solid fa-podcast"></i> Apple</a>
                            <a href="{{{{ item.yt_link if item.yt_link else '{yt_fallback}' }}}}" target="_blank" class="platform-btn"><i class="fa-brands fa-youtube"></i> YouTube</a>
                        </div>
                    </div>
                </div>
                {{% endfor %}}
            </div>
        </section>"""

# Replace La Galeria Nocturna
html = re.sub(r'<section id="shows" class="section shows-section">.*?</section>', 
              r'<section id="shows" class="section shows-section">\n' + 
              re.search(r'<section id="shows" class="section shows-section">(.*?)<div class="news-rail">', html, re.DOTALL).group(1) + 
              get_jinja('galeria_items', 'https://www.youtube.com/@gothprods44'), html, flags=re.DOTALL)

# Replace Metal Pulse
html = re.sub(r'<section id="metal-pulse" class="section shows-section">.*?</section>', 
              r'<section id="metal-pulse" class="section shows-section">\n' + 
              re.search(r'<section id="metal-pulse" class="section shows-section">(.*?)<div class="news-rail">', html, re.DOTALL).group(1) + 
              get_jinja('metalpulse_items', 'https://www.youtube.com/@gothprods44'), html, flags=re.DOTALL)

# Replace Caos Sonoro
html = re.sub(r'<section id="live" class="section shows-section">.*?</section>', 
              r'<section id="live" class="section shows-section">\n' + 
              re.search(r'<section id="live" class="section shows-section">(.*?)<div class="news-rail">', html, re.DOTALL).group(1) + 
              get_jinja('caossonoro_items', 'https://www.youtube.com/@gothprods44/streams'), html, flags=re.DOTALL)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("done")
