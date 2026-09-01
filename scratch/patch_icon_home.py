with open('templates/admin_dashboard.html', 'r') as f:
    content = f.read()

old_logo = '''            <label>Logo Central (Header)</label>
            <input type="file" name="header_logo" accept="image/*" style="background: #222; padding: 10px; border-radius: 4px; border: 1px solid #444; width: 100%; margin-bottom: 20px; color: #fff;">'''

new_logo = '''            <label>Logo Central (Header)</label>
            <input type="file" name="header_logo" accept="image/*" style="background: #222; padding: 10px; border-radius: 4px; border: 1px solid #444; width: 100%; margin-bottom: 20px; color: #fff;">
            
            <label>Ícono Menú Lateral (Home)</label>
            <input type="file" name="icon_home" accept="image/*" style="background: #222; padding: 10px; border-radius: 4px; border: 1px solid #444; width: 100%; margin-bottom: 20px; color: #fff;">'''

content = content.replace(old_logo, new_logo)

with open('templates/admin_dashboard.html', 'w') as f:
    f.write(content)
