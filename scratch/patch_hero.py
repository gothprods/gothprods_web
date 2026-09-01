with open('templates/index.html', 'r') as f:
    content = f.read()

old_hero = '''            <div class="hero-content">
                <h2 style="font-family: 'Creepster', cursive; font-weight: 400;">{{ settings.get('hero_title', 'Goth Productions es una creadora de contenidos enfocados al género más feroz del planeta') }}</h2>
                <p>{{ settings.get('hero_subtitle', 'Reviews de álbumes, cobertura de festivales y conciertos, colaboraciones con medios, entrevistas y mucho más.') }}</p>

            </div>'''

new_hero = '''            <div class="hero-content">
                {% set ht = settings.get('hero_title', 'Goth Productions es una creadora de contenidos enfocados al género más feroz del planeta') %}
                {% if ht %}
                <h2 style="font-family: 'Creepster', cursive; font-weight: 400;">{{ ht }}</h2>
                {% endif %}
                
                {% set hs = settings.get('hero_subtitle', 'Reviews de álbumes, cobertura de festivales y conciertos, colaboraciones con medios, entrevistas y mucho más.') %}
                {% if hs %}
                <p>{{ hs }}</p>
                {% endif %}
            </div>'''

content = content.replace(old_hero, new_hero)

with open('templates/index.html', 'w') as f:
    f.write(content)
