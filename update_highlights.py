import re

html_path = 'index.html'
with open(html_path, 'r') as f:
    html = f.read()

# Update Entrevistas Under Highlight Card
entrevistas_highlight_pattern = re.compile(
    r'(<!-- Entrevistas Under -->.*?<div class="card-image"[^>]*style="background-image: url\(\')[^\']+(\'.*?<h3><i class="fa-solid fa-microphone"></i> Entrevistas Under</h3>\s*<ul class="highlight-list">).*?(</ul>\s*<a href=")[^"]+(".*?</a>\s*</div>\s*</div>)',
    re.DOTALL
)

new_entrevistas_list = """
                            <li><strong>Honara:</strong> Post-metal y música clásica desde España.</li>
                            <li><strong>Athica:</strong> El poderoso metal originario de Panamá.</li>
                            <li><strong>Ominum:</strong> Historia y discografía del thrash metal sueco.</li>
"""

def replacer_entrevistas(match):
    # match.group(1) is everything up to the url start
    # match.group(2) is from the end of the url quote to the start of the <ul>
    # match.group(3) is the start of the <a href="
    # match.group(4) is the rest of the a tag
    img_url = "https://img.youtube.com/vi/2GDTVHHIRI8/maxresdefault.jpg" # Honara's image
    new_href = "#under-interviews"
    return match.group(1) + img_url + match.group(2) + '\n' + new_entrevistas_list + '                        ' + match.group(3) + new_href + match.group(4)

html = entrevistas_highlight_pattern.sub(replacer_entrevistas, html)

# Update Noticias Highlight Card
noticias_highlight_pattern = re.compile(
    r'(<!-- Últimas Noticias -->.*?<h3><i class="fa-solid fa-newspaper"></i> Últimas Noticias</h3>\s*<ul class="highlight-list">).*?(</ul>\s*<a href=")[^"]+(".*?</a>\s*</div>\s*</div>)',
    re.DOTALL
)

new_noticias_list = """
                            <li><a href="javascript:void(0);" data-target="newsModal1" class="open-review-modal"
                                    style="color: var(--text-main);"><strong>Korn Cancelado:</strong> Tras las recientes funas, la banda cancela su visita.</a></li>
                            <li><a href="javascript:void(0);" data-target="newsModal2" class="open-review-modal"
                                    style="color: var(--text-main);"><strong>Knotfest 2026:</strong> Preventa de boletos e información de sede.</a></li>
                            <li><a href="javascript:void(0);" data-target="newsModal3" class="open-review-modal"
                                    style="color: var(--text-main);"><strong>Black Label Society:</strong> Zakk Wylde pospone presentaciones en CDMX.</a></li>
"""

def replacer_noticias(match):
    new_href = "#news-section"
    return match.group(1) + '\n' + new_noticias_list + '                        ' + match.group(2) + new_href + match.group(3)

html = noticias_highlight_pattern.sub(replacer_noticias, html)

with open(html_path, 'w') as f:
    f.write(html)

print("Updated Highlight Cards!")
