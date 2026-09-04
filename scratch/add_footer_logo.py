import re

# 1. Update app.py
with open('app.py', 'r', encoding='utf-8') as f:
    app_content = f.read()

app_content = app_content.replace(
    "file_keys = ['hero_bg', 'header_logo', 'icon_home', 'galeria_bg'",
    "file_keys = ['hero_bg', 'header_logo', 'icon_home', 'footer_logo', 'galeria_bg'"
)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_content)

# 2. Update admin_dashboard.html
with open('templates/admin_dashboard.html', 'r', encoding='utf-8') as f:
    admin_content = f.read()

admin_content = admin_content.replace(
    '<input type="file" name="icon_home" accept="image/*" style="background: #222; padding: 10px; border-radius: 4px; border: 1px solid #444; width: 100%; margin-bottom: 20px; color: #fff;">',
    '<input type="file" name="icon_home" accept="image/*" style="background: #222; padding: 10px; border-radius: 4px; border: 1px solid #444; width: 100%; margin-bottom: 20px; color: #fff;">\n            \n            <label>Logo del Footer</label>\n            <input type="file" name="footer_logo" accept="image/*" style="background: #222; padding: 10px; border-radius: 4px; border: 1px solid #444; width: 100%; margin-bottom: 20px; color: #fff;">'
)

with open('templates/admin_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(admin_content)

# 3. Update index.html
with open('templates/index.html', 'r', encoding='utf-8') as f:
    index_content = f.read()

old_footer_img = '<img loading="lazy" decoding="async" src="/assets/logo.webp?v=2" alt="Goth Prods Logo" class="footer-logo">'
new_footer_img = """{% set footer_logo = settings.get('footer_logo', '/assets/logo.webp') %}
                <img loading="lazy" decoding="async" src="{{ footer_logo if footer_logo.startswith('http') or footer_logo.startswith('/assets') or footer_logo.startswith('assets') else '/' + footer_logo }}" alt="Goth Prods Logo" class="footer-logo">"""

index_content = index_content.replace(old_footer_img, new_footer_img)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(index_content)

print("Footer logo feature added successfully.")
