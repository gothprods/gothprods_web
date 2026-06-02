import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Jinja template for podcasts
def get_jinja(variable_name):
    return f"""            <div class="news-rail">
                {{% for item in {variable_name} %}}
                <div class="news-card">
                    <img src="{{{{ item.image_filename if item.image_filename.startswith('http') or item.image_filename.startswith('assets') else 'updates/' + item.image_filename }}}}" style="width: 100%; border-radius: 8px; margin-bottom: 10px; height: 140px; object-fit: cover; object-position: center;">
                    <div class="card-content">
                        <h3 style="font-size: 1rem; line-height: 1.2;">{{{{ item.title }}}}</h3>
                        <p style="font-size: 0.85rem; margin-bottom: 10px;">{{{{ item.short_desc[:120] }}}}...</p>
                        <div class="episode-actions" style="margin-top: 15px;">
                            {{% if item.sp_link %}}<a href="{{{{ item.sp_link }}}}" target="_blank" class="platform-btn spotify-btn"><i class="fa-brands fa-spotify"></i> Spotify</a>{{% endif %}}
                            {{% if item.ap_link %}}<a href="{{{{ item.ap_link }}}}" target="_blank" class="platform-btn apple-btn"><i class="fa-solid fa-podcast"></i> Apple</a>{{% endif %}}
                            {{% if item.yt_link %}}<a href="{{{{ item.yt_link }}}}" target="_blank" class="platform-btn"><i class="fa-brands fa-youtube"></i> YouTube</a>{{% endif %}}
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
              get_jinja('galeria_items'), html, flags=re.DOTALL)

# Replace Metal Pulse
html = re.sub(r'<section id="metal-pulse" class="section shows-section">.*?</section>', 
              r'<section id="metal-pulse" class="section shows-section">\n' + 
              re.search(r'<section id="metal-pulse" class="section shows-section">(.*?)<div class="news-rail">', html, re.DOTALL).group(1) + 
              get_jinja('metalpulse_items'), html, flags=re.DOTALL)

# Replace Caos Sonoro
html = re.sub(r'<section id="live" class="section shows-section">.*?</section>', 
              r'<section id="live" class="section shows-section">\n' + 
              re.search(r'<section id="live" class="section shows-section">(.*?)<div class="news-rail">', html, re.DOTALL).group(1) + 
              get_jinja('caossonoro_items'), html, flags=re.DOTALL)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("done")
