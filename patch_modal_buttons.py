import re

with open("templates/index.html", "r") as f:
    content = f.read()

# Update Evento Modal FB button
old_fb = """{% if evento.fb_link %}<a href="{{ evento.fb_link }}" target="_blank" class="platform-btn" style="background: #4267B2; padding: 10px 20px; font-size: 1.1rem;"><i class="fa-brands fa-facebook"></i> Evento</a>{% endif %}"""
new_fb = """{% if evento.fb_link %}<a href="{{ evento.fb_link }}" target="_blank" class="platform-btn" style="background: transparent; padding: 8px 15px; font-size: 0.95rem; border-radius: 4px; color: var(--accent-color); text-decoration: none; border: 1px solid var(--accent-color); min-width: auto; transition: all 0.3s;" onmouseover="this.style.background='var(--accent-color)'; this.style.color='#000';" onmouseout="this.style.background='transparent'; this.style.color='var(--accent-color)';"><i class="fa-brands fa-facebook-f"></i> Evento</a>{% endif %}"""
content = content.replace(old_fb, new_fb)

# Update Evento Modal IG button
old_ig = """{% if evento.ig_link %}<a href="{{ evento.ig_link }}" target="_blank" class="platform-btn" style="background: #E1306C; padding: 10px 20px; font-size: 1.1rem;"><i class="fa-brands fa-instagram"></i> Evento</a>{% endif %}"""
new_ig = """{% if evento.ig_link %}<a href="{{ evento.ig_link }}" target="_blank" class="platform-btn" style="background: transparent; padding: 8px 15px; font-size: 0.95rem; border-radius: 4px; color: var(--accent-color); text-decoration: none; border: 1px solid var(--accent-color); min-width: auto; transition: all 0.3s;" onmouseover="this.style.background='var(--accent-color)'; this.style.color='#000';" onmouseout="this.style.background='transparent'; this.style.color='var(--accent-color)';"><i class="fa-brands fa-instagram"></i> Evento</a>{% endif %}"""
content = content.replace(old_ig, new_ig)

with open("templates/index.html", "w") as f:
    f.write(content)

print("Modal buttons homologated")
