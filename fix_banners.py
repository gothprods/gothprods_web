import re

with open('index.html', 'r') as f:
    html = f.read()

# Restore the first card (Agenda)
agenda_pattern = re.compile(r'<!-- Últimas Noticias -->\s*<div class="card highlight-card">\s*<div class="card-image" style="background-image: url\(\'assets/reload_2\.jpg\'\); background-position: center;"></div>\s*<div class="card-content">\s*<h3><i class="fa-solid fa-calendar-days"></i> Agenda Mayo 2026</h3>')
agenda_fix = """<!-- Agenda del mes -->
                <div class="card highlight-card">
                    <div class="card-image" style="background-image: url('assets/banner_new.jpg');"></div>
                    <div class="card-content">
                        <h3><i class="fa-solid fa-calendar-days"></i> Agenda Mayo 2026</h3>"""
html = agenda_pattern.sub(agenda_fix, html)

# Fix the second card (Noticiero Nocturno)
news_pattern = re.compile(r'<!-- Últimas Noticias -->\s*<div class="card highlight-card">\s*<div class="card-image" style="background-image: url\(\'assets/Caos_Sonoro\.jpg\'\);"></div>\s*<div class="card-content">\s*<h3><i class="fa-solid fa-newspaper"></i> El Noticiero Nocturno</h3>')
news_fix = """<!-- Últimas Noticias -->
                <div class="card highlight-card">
                    <div class="card-image" style="background-image: url('assets/reload_2.jpg'); background-position: center;"></div>
                    <div class="card-content">
                        <h3><i class="fa-solid fa-newspaper"></i> El Noticiero Nocturno</h3>"""
html = news_pattern.sub(news_fix, html)

with open('index.html', 'w') as f:
    f.write(html)

print("Fixed banners.")
