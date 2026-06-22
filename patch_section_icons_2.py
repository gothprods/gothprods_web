import re

with open("templates/index.html", "r") as f:
    content = f.read()

def replacer_destacados(match):
    return f"""<div class="section-header" style="margin-bottom: 20px;">
                        <div class="header-titles" style="display: flex; align-items: center; gap: 15px; justify-content: center;">
                            {{% set icon_path = settings.get('icon_destacados', 'assets/destacados_icon.png') %}}
                            <img loading="lazy" src="{{{{ icon_path if icon_path.startswith('http') or icon_path.startswith('assets') else 'updates/' + icon_path }}}}" class="section-medal">
                            <div class="header-text-group" style="text-align: left; margin: 0;">
                                {match.group(1)}
                            </div>
                        </div>"""

content = re.sub(r'<div class="section-header" style="margin-bottom: 20px;">\s*(<h2 style="font-size: 2\.2rem;">Bandas de la <span>Semana</span></h2>)', replacer_destacados, content, 1)
content = re.sub(r'<div class="section-header" style="margin-bottom: 20px;">\s*(<h2 style="font-size: 2\.2rem;">Eventos <span>Destacados</span></h2>)', replacer_destacados, content, 1)

with open("templates/index.html", "w") as f:
    f.write(content)

print("Patch 2 applied.")
