import re

with open("templates/admin_dashboard.html", "r") as f:
    content = f.read()

# 1. Update toolbar styles & buttons
# Replace the old toolbar with the new sticky, smaller one containing alignment buttons.

old_toolbar_regex = r'<div class="textarea-toolbar" style="display: flex; gap: 10px; margin-bottom: 5px; background: #222; padding: 5px; border-radius: 4px; border: 1px solid #444;">(.*?)</div>'

new_toolbar_html = """
<div class="textarea-toolbar" style="display: flex; gap: 5px; background: #222; padding: 5px; border: 1px solid #444; border-bottom: none; border-radius: 4px 4px 0 0; position: sticky; top: 0; z-index: 100;">
    <button type="button" onmousedown="formatVisual(event, 'bold')" style="background: #333; color: #fff; border: 1px solid #555; padding: 2px 6px; font-size: 0.85rem; border-radius: 3px; cursor: pointer;" title="Negrita"><i class="fa-solid fa-bold"></i></button>
    <div style="width: 1px; background: #444; margin: 0 5px;"></div>
    <button type="button" onmousedown="formatVisual(event, 'foreColor', '#ffffff')" style="background: #333; color: #fff; border: 1px solid #555; padding: 2px 6px; font-size: 0.85rem; border-radius: 3px; cursor: pointer;" title="Texto Blanco"><i class="fa-solid fa-droplet"></i> Blanco</button>
    <button type="button" onmousedown="formatVisual(event, 'foreColor', '#716d4a')" style="background: #333; color: var(--accent-color); border: 1px solid #555; padding: 2px 6px; font-size: 0.85rem; border-radius: 3px; cursor: pointer;" title="Texto Dorado"><i class="fa-solid fa-droplet"></i> Dorado</button>
    <div style="width: 1px; background: #444; margin: 0 5px;"></div>
    <button type="button" onmousedown="formatVisual(event, 'justifyLeft')" style="background: #333; color: #fff; border: 1px solid #555; padding: 2px 6px; font-size: 0.85rem; border-radius: 3px; cursor: pointer;" title="Izquierda"><i class="fa-solid fa-align-left"></i></button>
    <button type="button" onmousedown="formatVisual(event, 'justifyCenter')" style="background: #333; color: #fff; border: 1px solid #555; padding: 2px 6px; font-size: 0.85rem; border-radius: 3px; cursor: pointer;" title="Centro"><i class="fa-solid fa-align-center"></i></button>
    <button type="button" onmousedown="formatVisual(event, 'justifyRight')" style="background: #333; color: #fff; border: 1px solid #555; padding: 2px 6px; font-size: 0.85rem; border-radius: 3px; cursor: pointer;" title="Derecha"><i class="fa-solid fa-align-right"></i></button>
    <button type="button" onmousedown="formatVisual(event, 'justifyFull')" style="background: #333; color: #fff; border: 1px solid #555; padding: 2px 6px; font-size: 0.85rem; border-radius: 3px; cursor: pointer;" title="Justificar"><i class="fa-solid fa-align-justify"></i></button>
</div>
"""

content = re.sub(old_toolbar_regex, new_toolbar_html.strip(), content, flags=re.DOTALL)

# Also update the rich-editor border radius so it looks connected to the toolbar
content = content.replace(
    'class="rich-editor" contenteditable="true" style="min-height: 120px; background: #111; color: #fff; border: 1px solid #333; border-radius: 4px; padding: 10px; outline: none; overflow-y: auto; white-space: pre-wrap;"',
    'class="rich-editor" contenteditable="true" style="min-height: 120px; background: #111; color: #fff; border: 1px solid #333; border-radius: 0 0 4px 4px; padding: 10px; outline: none; overflow-y: auto; white-space: pre-wrap;"'
)


# 2. Update Javascript formatVisual function
old_js_if = """    if (action === 'bold') {
        document.execCommand('bold', false, null);
    } else if (action === 'foreColor') {
        // Modern approach allows inline styles instead of <font> tags
        document.execCommand('styleWithCSS', false, true);
        document.execCommand('foreColor', false, value);
    }"""

new_js_if = """    if (action === 'foreColor') {
        document.execCommand('styleWithCSS', false, true);
        document.execCommand('foreColor', false, value);
    } else {
        document.execCommand(action, false, null);
    }"""

content = content.replace(old_js_if, new_js_if)

# 3. Inject onsubmit into the forms
def inject_onsubmit(form_id, html_content):
    if f'id="{form_id}"' in html_content:
        # Avoid duplicating
        if f'onsubmit="syncAllVisualsToEditors()"' not in html_content:
            html_content = re.sub(rf'(<form[^>]*id="{form_id}"[^>]*)>', r'\1 onsubmit="syncAllVisualsToEditors()">', html_content)
    return html_content

content = inject_onsubmit("main-form", content)
content = inject_onsubmit("banda-form", content)
content = inject_onsubmit("eventos-form", content)

with open("templates/admin_dashboard.html", "w") as f:
    f.write(content)

print("Patch applied successfully.")
