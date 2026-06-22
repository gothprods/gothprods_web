import re

with open("templates/index.html", "r") as f:
    content = f.read()

# 1. Change all the inline justify-content: center; that I added to flex-start
content = content.replace('justify-content: center;"\n                    {% set icon_path', 'justify-content: flex-start;"\n                    {% set icon_path')
content = content.replace('justify-content: center;">\n                            {% set icon_path', 'justify-content: flex-start;">\n                            {% set icon_path')

# 2. Add the icon to Entrevistas Under
icon_key = 'icon_interviews'
default_icon = 'assets/entrevistas_icon.png'

def replacer_entrevistas(match):
    return f"""<div class="header-titles" style="display: flex; align-items: center; gap: 15px; justify-content: flex-start;">
                    {{% set icon_path = settings.get('{icon_key}', '{default_icon}') %}}
                    <img loading="lazy" src="{{{{ icon_path if icon_path.startswith('http') or icon_path.startswith('assets') else 'updates/' + icon_path }}}}" class="section-medal">
                    <div class="header-text-group" style="text-align: left; margin: 0;">
                        {match.group(1)}
                    </div>
                </div>"""

content = re.sub(r'<div class="header-titles">\s*(<h2>Entrevistas <span>Under</span></h2>)\s*</div>', replacer_entrevistas, content, 1)


# Let's also check Medios Aliados, just in case, I should align it to flex-start and give it the icon if it exists, or just align the text to left.
# Currently Medios Aliados is:
# <section id="medios-aliados">
#     <h2>Medios <span>Aliados</span></h2>
# Actually Medios aliados h2 has text-align: center in CSS.

with open("templates/index.html", "w") as f:
    f.write(content)

with open("index.css", "r") as f:
    css_content = f.read()

# Change Medios Aliados from text-align: center to text-align: left
css_content = css_content.replace('text-align: center;\n}\n\n#medios-aliados h2', 'text-align: left;\n}\n\n#medios-aliados h2')
css_content = css_content.replace('.section-header {\n    display: flex;\n    justify-content: space-between;', '.section-header {\n    display: flex;\n    justify-content: flex-start;') # wait, space-between might be needed if there are actions on the right.
# Let's just make sure `.section-header` text is left aligned.
# .section-header { align-items: center; justify-content: space-between; }
# If there are no actions, space-between centers it if we don't have width 100%. Actually let's just make `.section-header` have `justify-content: flex-start; gap: 20px;` if it's currently center.
css_content = css_content.replace('justify-content: center;\n    align-items: center;\n    margin-bottom: 2rem;', 'justify-content: flex-start;\n    align-items: center;\n    margin-bottom: 2rem;')

with open("index.css", "w") as f:
    f.write(css_content)

print("Patch aligned to left applied.")
