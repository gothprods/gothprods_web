import re

with open("templates/admin_dashboard.html", "r") as f:
    content = f.read()

# 1. Add forceescape to data attributes that might contain HTML
attributes_to_escape = [
    r'(data-full="{{ item\.full_desc) (\| default\(\'\'\, true\))? }}',
    r'(data-biocorta="{{ b\.bio_corta) (\| default\(\'\'\, true\))? }}',
    r'(data-textores="{{ b\.texto_resena) (\| default\(\'\'\, true\))? }}',
    r'(data-disco="{{ b\.discografia) (\| default\(\'\'\, true\))? }}',
    r'(data-biocorta="{{ e\.bio_corta) (\| default\(\'\'\, true\))? }}',
    r'(data-texto="{{ e\.texto_articulo) (\| default\(\'\'\, true\))? }}'
]

# For each, replace with `| forceescape` appended
# Example: data-full="{{ item.full_desc | default('', true) | forceescape }}"
for attr_pattern in attributes_to_escape:
    # Instead of regex, let's just do targeted string replaces to be safer
    pass

# String replacements for forceescape
replacements = {
    'data-full="{{ item.full_desc | default(\'\', true) }}"': 'data-full="{{ item.full_desc | default(\'\', true) | forceescape }}"',
    'data-biocorta="{{ b.bio_corta }}"': 'data-biocorta="{{ b.bio_corta | forceescape }}"',
    'data-textores="{{ b.texto_resena }}"': 'data-textores="{{ b.texto_resena | forceescape }}"',
    'data-disco="{{ b.discografia }}"': 'data-disco="{{ b.discografia | forceescape }}"',
    'data-biocorta="{{ e.bio_corta }}"': 'data-biocorta="{{ e.bio_corta | forceescape }}"',
    'data-texto="{{ e.texto_articulo }}"': 'data-texto="{{ e.texto_articulo | forceescape }}"',
    'data-full="{{ item.full_desc }}"': 'data-full="{{ item.full_desc | forceescape }}"'
}

for old, new in replacements.items():
    content = content.replace(old, new)


# 2. Add syncAllEditorsToTextareas function and update onsubmit
new_sync_function = """
function syncAllEditorsToTextareas() {
    document.querySelectorAll('.visual-editor-container').forEach(container => {
        const textarea = container.querySelector('textarea');
        const editor = container.querySelector('.rich-editor');
        if(textarea && editor) {
            textarea.value = editor.innerHTML;
        }
    });
}
"""

if "function syncAllEditorsToTextareas()" not in content:
    content = content.replace("function syncAllVisualsToEditors()", new_sync_function + "\nfunction syncAllVisualsToEditors()")

# Update onsubmit to use syncAllEditorsToTextareas
content = content.replace('onsubmit="syncAllVisualsToEditors()"', 'onsubmit="syncAllEditorsToTextareas()"')


with open("templates/admin_dashboard.html", "w") as f:
    f.write(content)

print("Editor bugs fixed!")
