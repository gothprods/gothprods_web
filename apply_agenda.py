import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_agenda = """        <section id="agenda" class="section agenda-section">
            <div class="section-header">
                <h2>Agenda <span>Metalera 2026</span></h2>
            </div>
            
            {% for month_name, items in agenda_grouped.items() %}
            <h3 style="color: var(--accent-color); margin-bottom: 10px; margin-top: 20px; text-transform: uppercase;">{{ month_name }}</h3>
            <div class="news-rail">
                {% for item in items %}
                <div class="agenda-card {% if item.author < current_date %}past-event{% endif %}">
                    <img src="{{ item.image_filename if item.image_filename.startswith('http') or item.image_filename.startswith('assets') else 'updates/' + item.image_filename }}" onerror="this.src='assets/logo.png';" alt="Logo" class="agenda-logo">
                    <h3>{{ item.title }}</h3>
                    <p>{{ item.short_desc }}</p>
                    <p style="margin-top: 5px; color: var(--accent-color); font-weight: bold;">{{ item.full_desc }}</p>
                    {% if item.yt_link == 'Y' %}
                    <img src="assets/viking.jpg" class="agenda-viking-small" title="Goth Prods Crew">
                    {% endif %}
                </div>
                {% endfor %}
            </div>
            {% endfor %}
        </section>"""

# Replace the entire agenda section using regex
html = re.sub(r'<section id="agenda" class="section agenda-section">.*?</section>', new_agenda, html, flags=re.DOTALL)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("done")
