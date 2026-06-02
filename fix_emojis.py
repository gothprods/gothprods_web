import re

html_path = 'index.html'
with open(html_path, 'r') as f:
    html = f.read()

# 1. Fix Metallica card preview (remove emoji & improve object-position)
old_meta_preview = """<img src="assets/reload_2.jpg" alt="Metallica ReLoad" style="width: 100%; border-radius: 8px; margin-bottom: 10px; height: 140px; object-fit: cover;">
                    <h3 style="font-size: 1rem; line-height: 1.2;">🎸🔥 ¡METALLICA ANUNCIA EL ÉPICO BOX SET REMASTERIZADO DE 'RELOAD'! 🔥🎸</h3>"""

new_meta_preview = """<img src="assets/reload_2.jpg" alt="Metallica ReLoad" style="width: 100%; border-radius: 8px; margin-bottom: 10px; height: 140px; object-fit: cover; object-position: center;">
                    <h3 style="font-size: 1rem; line-height: 1.2;">¡METALLICA ANUNCIA EL ÉPICO BOX SET REMASTERIZADO DE 'RELOAD'!</h3>"""

html = html.replace(old_meta_preview, new_meta_preview)

# 2. Fix Dimebag card preview (remove emoji & improve object-position)
old_dime_preview = """<img src="assets/dimebag_dean.jpg" alt="Dimebag Dean Guitars" style="width: 100%; border-radius: 8px; margin-bottom: 10px; height: 140px; object-fit: cover; background: #222;">
                    <h3 style="font-size: 1rem; line-height: 1.2;">🚨 ¡ACTUALIZACIÓN EN LA BATALLA LEGAL: DIMEBAG DARRELL VS. DEAN GUITARS!</h3>"""

new_dime_preview = """<img src="assets/dimebag_dean.jpg" alt="Dimebag Dean Guitars" style="width: 100%; border-radius: 8px; margin-bottom: 10px; height: 140px; object-fit: cover; object-position: top center; background: #222;">
                    <h3 style="font-size: 1rem; line-height: 1.2;">¡ACTUALIZACIÓN EN LA BATALLA LEGAL: DIMEBAG DARRELL VS. DEAN GUITARS!</h3>"""

html = html.replace(old_dime_preview, new_dime_preview)

# 3. Fix Metallica Modal (remove emojis)
html = html.replace("<h2>🎸🔥 ¡METALLICA ANUNCIA EL ÉPICO BOX SET REMASTERIZADO DE 'RELOAD'! 🔥🎸</h2>", "<h2>¡METALLICA ANUNCIA EL ÉPICO BOX SET REMASTERIZADO DE 'RELOAD'!</h2>")

# 4. Fix Dimebag Modal (remove emojis, add missing image)
old_dime_modal = """    <div id="newsModal5" class="modal">
        <div class="modal-content">
            <span class="close-modal">&times;</span>
            <div class="modal-body">
                <h2>🚨 ¡ACTUALIZACIÓN EN LA BATALLA LEGAL: DIMEBAG DARRELL VS. DEAN GUITARS!</h2>"""

new_dime_modal = """    <div id="newsModal5" class="modal">
        <div class="modal-content">
            <span class="close-modal">&times;</span>
            <img src="assets/dimebag_dean.jpg" alt="Dimebag Dean Guitars" class="modal-banner" style="object-position: top center;">
            <div class="modal-body">
                <h2>¡ACTUALIZACIÓN EN LA BATALLA LEGAL: DIMEBAG DARRELL VS. DEAN GUITARS!</h2>"""

html = html.replace(old_dime_modal, new_dime_modal)

with open(html_path, 'w') as f:
    f.write(html)

print("Updated emojis and images successfully!")
