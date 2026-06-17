import re
import os

html_toolbar = """
<div class="textarea-toolbar" data-target="{target_name}" style="display: flex; gap: 10px; margin-bottom: 5px; background: #222; padding: 5px; border-radius: 4px; border: 1px solid #444;">
    <button type="button" onclick="formatText(this, 'bold')" style="background: #333; color: #fff; border: 1px solid #555; padding: 4px 8px; border-radius: 4px; cursor: pointer;" title="Negrita"><i class="fa-solid fa-bold"></i></button>
    <button type="button" onclick="formatText(this, 'color', '#ffffff')" style="background: #333; color: #fff; border: 1px solid #555; padding: 4px 8px; border-radius: 4px; cursor: pointer;" title="Texto Blanco"><i class="fa-solid fa-droplet"></i> Blanco</button>
    <button type="button" onclick="formatText(this, 'color', 'var(--accent-color)')" style="background: #333; color: var(--accent-color); border: 1px solid #555; padding: 4px 8px; border-radius: 4px; cursor: pointer;" title="Texto Dorado"><i class="fa-solid fa-droplet"></i> Dorado</button>
</div>
<textarea name="{target_name}"
"""

js_function = """
<script>
function formatText(btn, action, value=null) {
    const targetName = btn.parentElement.getAttribute('data-target');
    const textarea = btn.parentElement.nextElementSibling;
    
    if (!textarea || textarea.tagName.toLowerCase() !== 'textarea') {
        console.error("No textarea found next to toolbar");
        return;
    }
    
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const text = textarea.value;
    const selectedText = text.substring(start, end);
    
    let replacement = "";
    if (action === 'bold') {
        replacement = `<b>${selectedText}</b>`;
    } else if (action === 'color') {
        replacement = `<span style="color: ${value};">${selectedText}</span>`;
    }
    
    textarea.value = text.substring(0, start) + replacement + text.substring(end);
    textarea.focus();
    
    if (!selectedText) {
        let offset = action === 'bold' ? 3 : `<span style="color: ${value};">`.length;
        textarea.selectionStart = start + offset;
        textarea.selectionEnd = start + offset;
    } else {
        textarea.selectionStart = start;
        textarea.selectionEnd = start + replacement.length;
    }
}
</script>
</body>
"""

# Replace in admin_dashboard.html
with open("templates/admin_dashboard.html", "r") as f:
    admin_html = f.read()

fields = ["full_desc", "bio_corta", "texto_resena", "discografia"]

for field in fields:
    # Use re.sub to inject the toolbar just before the <textarea>
    # Make sure we don't duplicate it if already exists
    if f'data-target="{field}"' not in admin_html:
        admin_html = re.sub(rf'<textarea name="{field}"', html_toolbar.format(target_name=field), admin_html)

if "function formatText(" not in admin_html:
    admin_html = admin_html.replace("</body>", js_function)

with open("templates/admin_dashboard.html", "w") as f:
    f.write(admin_html)


def apply_safe(filepath):
    if not os.path.exists(filepath): return
    with open(filepath, "r") as f:
        content = f.read()
    
    # Previews on cards (index.html mostly)
    content = re.sub(r'{{ (item\.short_desc) }}', r'{{ \1 | striptags }}', content)
    # The truncate ones
    content = re.sub(r'{{\s*(banda_semana\.bio_corta)\|truncate', r'{{ \1 | striptags | truncate', content)
    content = re.sub(r'{{\s*(evento\.bio_corta)\|truncate', r'{{ \1 | striptags | truncate', content)
    
    # Safe rendering in modals/pages
    targets = [
        r"item\.full_desc", 
        r"banda_semana\.bio_corta", 
        r"banda_semana\.texto_resena", 
        r"banda_semana\.discografia", 
        r"evento\.bio_corta"
    ]
    
    for t in targets:
        # Match {{ item.full_desc }} specifically, avoid ones already piped to safe or truncate
        # Negative lookahead for |
        pattern = r'{{\s*(' + t + r')\s*}}'
        content = re.sub(pattern, r'{{ \1 | safe }}', content)

    with open(filepath, "w") as f:
        f.write(content)

for tpl in ["templates/index.html", "templates/banda.html", "templates/evento.html", "templates/articulo.html"]:
    apply_safe(tpl)

print("Text editing tools successfully applied!")
