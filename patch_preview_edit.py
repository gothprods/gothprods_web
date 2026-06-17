import re

# 1. Update index.css
css_append = """
.preview-edit-btn {
    position: absolute;
    top: 10px;
    right: 10px;
    background-color: var(--accent-color);
    color: #000;
    padding: 8px 15px;
    border-radius: 20px;
    font-size: 0.9rem;
    font-weight: bold;
    text-decoration: none;
    z-index: 100;
    box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    transition: transform 0.2s;
    font-family: 'Inter', sans-serif;
    display: flex;
    align-items: center;
    gap: 5px;
}
.preview-edit-btn:hover {
    transform: scale(1.05);
    color: #000;
}
"""

with open("index.css", "a") as f:
    f.write(css_append)

# 2. Update index.html
with open("templates/index.html", "r") as f:
    html = f.read()

# Banda
html = html.replace('<div class="banda-slide fade"', '<div class="banda-slide fade" style="position:relative;"')
if "edit_type=banda" not in html:
    html = html.replace(
        '<div class="grid-container" style="display: flex;', 
        '{% if is_preview %}<a href="/admin/dashboard?edit_type=banda&edit_id={{ banda_semana.id }}" target="_parent" class="preview-edit-btn"><i class="fa-solid fa-pen"></i> Corregir Banda</a>{% endif %}\n                            <div class="grid-container" style="display: flex;'
    )

# Evento
html = html.replace('<div class="evento-slide fade"', '<div class="evento-slide fade" style="position:relative;"')
if "edit_type=evento" not in html:
    html = html.replace(
        '<div class="grid-container" style="display: flex; flex-wrap: wrap;', 
        '{% if is_preview %}<a href="/admin/dashboard?edit_type=evento&edit_id={{ evento.id }}" target="_parent" class="preview-edit-btn"><i class="fa-solid fa-pen"></i> Corregir Evento</a>{% endif %}\n                        <div class="grid-container" style="display: flex; flex-wrap: wrap;'
    )

# Content items (article-card)
if "edit_type=content" not in html:
    html = html.replace(
        '<div class="article-card"',
        '<div class="article-card" style="position: relative;"'
    )
    html = html.replace(
        '<img loading="lazy" src="{{ item.image_path }}"',
        '{% if is_preview %}<a href="/admin/dashboard?edit_type=content&edit_id={{ item.id }}" target="_parent" class="preview-edit-btn"><i class="fa-solid fa-pen"></i> Editar</a>{% endif %}\n                        <img loading="lazy" src="{{ item.image_path }}"'
    )

with open("templates/index.html", "w") as f:
    f.write(html)

# 3. Update articulo.html
with open("templates/articulo.html", "r") as f:
    art_html = f.read()

if "edit_type=content" not in art_html:
    art_html = art_html.replace(
        '<div style="max-width: 800px; margin: 0 auto; background: #111;',
        '<div style="max-width: 800px; margin: 0 auto; background: #111; position: relative;'
    )
    art_html = art_html.replace(
        '<a href="/" style="color: var(--accent-color);',
        '{% if is_preview %}<a href="/admin/dashboard?edit_type=content&edit_id={{ item.id }}" target="_parent" class="preview-edit-btn" style="top: 20px; right: 20px;"><i class="fa-solid fa-pen"></i> Corregir Artículo en Panel</a>{% endif %}\n            <a href="/" style="color: var(--accent-color);'
    )
    with open("templates/articulo.html", "w") as f:
        f.write(art_html)

# 4. Update admin_dashboard.html (Add JS)
js_script = """
<script>
window.addEventListener('DOMContentLoaded', (event) => {
    const urlParams = new URLSearchParams(window.location.search);
    const editType = urlParams.get('edit_type');
    const editId = urlParams.get('edit_id');

    if (editType && editId) {
        let btn = null;
        if (editType === 'banda') {
            openTab(event, 'tab-banda');
            btn = document.querySelector(`.edit-banda-btn[data-id="${editId}"]`);
        } else if (editType === 'evento') {
            openTab(event, 'tab-eventos');
            btn = document.querySelector(`.edit-banda-btn[data-id="${editId}"]`);
        } else if (editType === 'content') {
            btn = document.querySelector(`.edit-btn[data-id="${editId}"]`);
            if (btn) {
                const tab = btn.closest('.tab-content');
                if (tab) {
                    openTab(event, tab.id);
                }
            }
        }
        
        if (btn) {
            // Wait slightly for tab transition
            setTimeout(() => {
                btn.click();
                btn.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }, 300);
        }
        
        // Remove query parameters from URL without reloading
        window.history.replaceState({}, document.title, "/admin/dashboard");
    }
});
</script>
</body>
"""

with open("templates/admin_dashboard.html", "r") as f:
    admin_html = f.read()

if "const editType = urlParams.get('edit_type');" not in admin_html:
    admin_html = admin_html.replace("</body>", js_script)
    with open("templates/admin_dashboard.html", "w") as f:
        f.write(admin_html)

print("Preview Edit Buttons injected successfully!")
