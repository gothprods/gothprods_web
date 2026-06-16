import re

with open("templates/index.html", "r") as f:
    content = f.read()

# Update Spotify inner wrapper
old_sp = """                                <div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap; flex: 1; min-width: 200px;">
                                    <div style="flex: 1; min-width: 140px;">
                                        <iframe style="border-radius:12px; border: none; background: #000;" src="{{ banda_semana.ultimo_lanzamiento_sp_link }}" width="100%" height="152" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
                                    </div>"""

new_sp = """                                <div style="display: flex; flex-direction: column; gap: 10px; align-items: center; flex: 1; min-width: 140px;">
                                    <div style="width: 100%;">
                                        <iframe style="border-radius:12px; border: none; background: #000;" src="{{ banda_semana.ultimo_lanzamiento_sp_link }}" width="100%" height="152" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
                                    </div>"""
content = content.replace(old_sp, new_sp)

# Update Apple inner wrapper
old_ap = """                                <div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap; flex: 1; min-width: 200px;">
                                    <div style="flex: 1; min-width: 140px;">
                                        <iframe loading="lazy" allow="autoplay *; encrypted-media *; fullscreen *; clipboard-write" frameborder="0" height="152" style="width:100%;max-width:660px;overflow:hidden;background:#000;border-radius:12px; border: none;" sandbox="allow-forms allow-popups allow-same-origin allow-scripts allow-top-navigation-by-user-activation" src="{{ banda_semana.ultimo_lanzamiento_ap_link }}{{ '&theme=dark' if '?' in banda_semana.ultimo_lanzamiento_ap_link else '?theme=dark' }}"></iframe>
                                    </div>"""

new_ap = """                                <div style="display: flex; flex-direction: column; gap: 10px; align-items: center; flex: 1; min-width: 140px;">
                                    <div style="width: 100%;">
                                        <iframe loading="lazy" allow="autoplay *; encrypted-media *; fullscreen *; clipboard-write" frameborder="0" height="152" style="width:100%;max-width:660px;overflow:hidden;background:#000;border-radius:12px; border: none;" sandbox="allow-forms allow-popups allow-same-origin allow-scripts allow-top-navigation-by-user-activation" src="{{ banda_semana.ultimo_lanzamiento_ap_link }}{{ '&theme=dark' if '?' in banda_semana.ultimo_lanzamiento_ap_link else '?theme=dark' }}"></iframe>
                                    </div>"""
content = content.replace(old_ap, new_ap)

with open("templates/index.html", "w") as f:
    f.write(content)

print("Players layout fixed")
