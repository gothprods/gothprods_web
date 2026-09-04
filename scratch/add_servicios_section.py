with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

servicios_section = """
        {% if settings.get('show_servicios', '1') == '1' %}
        <section id="servicios" class="section servicios-section" style="scroll-margin-top: 100px;">
            <div class="section-header">
                <div class="header-titles" style="display: flex; align-items: center; gap: 15px; justify-content: flex-start;">
                    {% set icon_path = settings.get('icon_servicios', 'updates/servicios_icon.jpg') %}
                    <img loading="lazy" decoding="async" src="{{ icon_path if icon_path.startswith('http') or (icon_path.startswith('assets') or icon_path.startswith('/assets')) else 'updates/' + icon_path }}" class="section-medal" width="65" height="65" style="width: 65px; height: 65px; min-width: 65px; min-height: 65px; border-radius: 5px;">
                    <div class="header-text-group" style="text-align: left; margin: 0;">
                        <h2 style="font-family: 'Creepster', cursive; font-weight: 400;">{{ settings.get('title_servicios', 'Servicios') }}</h2>
                    </div>
                </div>
            </div>
            <div style="text-align: center; color: #aaa; padding: 40px; border: 1px dashed #333; border-radius: 8px; margin: 20px 0;">
                <p>Nuestros servicios de producción, promoción y booking estarán disponibles aquí próximamente.</p>
            </div>
        </section>
        {% endif %}
"""

# Insert before equipo or contacto
content = content.replace('<section id="equipo"', servicios_section + '\n        <section id="equipo"')

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("added")
