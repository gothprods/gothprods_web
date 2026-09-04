with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# We will find the entire block for the contact form and comment it out or remove it.
pattern = re.compile(
    r"(\{% if settings\.get\('show_contactanos', '1'\) == '1' %\})\s*(<section id=\"contact\" class=\"section contact-section\">.*?Únete a los <span>Berserkers.*?</section>)\s*(\{% endif %\})",
    re.DOTALL
)

match = pattern.search(content)
if match:
    # Instead of deleting, I will comment out the whole thing in jinja or html
    # Or simply remove it from the page
    new_content = pattern.sub('', content)
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Sección eliminada.")
else:
    print("No se encontró el patrón exacto.")
