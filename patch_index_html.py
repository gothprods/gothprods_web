import re

with open("templates/index.html", "r") as f:
    content = f.read()

# 1. Replace the start of banda-semana section
old_banda_start = """        {% if settings.get('show_banda_semana', '1') == '1' and bandas_semana %}
        <section id="banda-semana" class="section highlights-section" style="background: linear-gradient(to right, #111, #000); border-bottom: 2px solid var(--accent-color); padding: 3.5rem 5%;">
            <div class="section-header" style="margin-bottom: 20px;">
                <h2>Banda de la <span>Semana</span></h2>
            </div>"""

new_banda_start = """        {% if (settings.get('show_banda_semana', '1') == '1' and bandas_semana) or eventos_semana %}
        <section id="banda-eventos-semana" class="section highlights-section" style="background: linear-gradient(to right, #111, #000); border-bottom: 2px solid var(--accent-color); padding: 3.5rem 5%;">
            <div style="display: flex; flex-wrap: wrap; gap: 40px;">
                
                {% if settings.get('show_banda_semana', '1') == '1' and bandas_semana %}
                <div style="flex: 1; min-width: 300px;">
                    <div class="section-header" style="margin-bottom: 20px;">
                        <h2 style="font-size: 2.2rem;">Banda de la <span>Semana</span></h2>
                    </div>"""

content = content.replace(old_banda_start, new_banda_start)

# 2. Add Eventos after Banda slider
old_banda_end = """            <!-- Slider Dots -->
            <div style="text-align: center; margin-top: 30px;">
                {% for banda_semana in bandas_semana %}
                <span class="banda-dot {% if loop.index == 1 %}active{% endif %}" onclick="currentBandaSlide({{ loop.index }})" style="height: 12px; width: 12px; margin: 0 5px; background-color: {% if loop.index == 1 %}var(--accent-color){% else %}#555{% endif %}; border-radius: 50%; display: inline-block; cursor: pointer; transition: background-color 0.3s ease;"></span>
                {% endfor %}
            </div>

        </section>"""

new_banda_end = """            <!-- Slider Dots -->
            <div style="text-align: center; margin-top: 30px;">
                {% for banda_semana in bandas_semana %}
                <span class="banda-dot {% if loop.index == 1 %}active{% endif %}" onclick="currentBandaSlide({{ loop.index }})" style="height: 12px; width: 12px; margin: 0 5px; background-color: {% if loop.index == 1 %}var(--accent-color){% else %}#555{% endif %}; border-radius: 50%; display: inline-block; cursor: pointer; transition: background-color 0.3s ease;"></span>
                {% endfor %}
            </div>
            
            </div>
            {% endif %}

            {% if eventos_semana %}
            <div style="flex: 1; min-width: 300px;">
                <div class="section-header" style="margin-bottom: 20px;">
                    <h2 style="font-size: 2.2rem;">Eventos de la <span>Semana</span></h2>
                </div>
                <div class="evento-slider-container" style="position: relative; overflow: hidden;">
                    {% for evento in eventos_semana %}
                    <div class="evento-slide fade" style="animation: fadeEffect 1s; {% if loop.index != 1 %}display: none;{% endif %}">
                        <div style="display: flex; flex-direction: column; gap: 15px;">
                            <img loading="lazy" src="{{ evento.img_video_path }}" alt="{{ evento.nombre_evento }}" style="width: 100%; height: auto; border-radius: 12px; box-shadow: 0 10px 20px rgba(0,0,0,0.8);">
                            <h3 class="notranslate" style="font-size: 1.8rem; color: var(--accent-color); margin-bottom: 0px; font-family: 'Oswald', sans-serif; text-transform: uppercase;">{{ evento.titulo_articulo }}</h3>
                            <p style="font-size: 1.2rem; color: #fff; font-weight: bold; margin-bottom: 5px;">{{ evento.nombre_evento }}</p>
                            <p style="font-size: 0.95rem; color: #888; margin-bottom: 10px;"><i class="fa-solid fa-calendar-day"></i> {{ evento.fecha_evento }} | <i class="fa-solid fa-location-dot"></i> {{ evento.ciudad }}, {{ evento.pais }}</p>
                            <div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 8px; border: 1px solid #333;">
                                <p style="font-size: 0.95rem; line-height: 1.4; margin-bottom: 15px; color: #ccc;">{{ evento.bio_corta }}</p>
                                <button onclick="openEventoModal({{ evento.id }})" style="background: transparent; color: var(--accent-color); border: 1px solid var(--accent-color); padding: 5px 12px; font-size: 0.85rem; border-radius: 4px; cursor: pointer; text-transform: uppercase; font-family: 'Oswald', sans-serif; letter-spacing: 1px; transition: all 0.3s;"><i class="fa-solid fa-book-open"></i> Leer más</button>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
                {% if eventos_semana|length > 1 %}
                <div style="text-align: center; margin-top: 20px;">
                    {% for evento in eventos_semana %}
                    <span class="evento-dot {% if loop.index == 1 %}active{% endif %}" onclick="currentEventoSlide({{ loop.index }})" style="height: 12px; width: 12px; margin: 0 5px; background-color: {% if loop.index == 1 %}var(--accent-color){% else %}#555{% endif %}; border-radius: 50%; display: inline-block; cursor: pointer; transition: background-color 0.3s ease;"></span>
                    {% endfor %}
                </div>
                {% endif %}
            </div>
            {% endif %}

        </div>
        </section>"""

content = content.replace(old_banda_end, new_banda_end)

# 3. Add Evento Modals
old_modal_marker = """        <!-- BANDA MODALS (One for each band) -->"""
new_modal_marker = """        <!-- EVENTO MODALS -->
        {% for evento in eventos_semana %}
        <div id="evento-modal-{{ evento.id }}" class="banda-modal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.9); z-index: 9999; justify-content: center; align-items: center; padding: 20px;">
            <div id="evento-modal-content-{{ evento.id }}" style="background: #111; max-width: 800px; width: 100%; max-height: 90vh; overflow-y: auto; border: 1px solid var(--accent-color); border-radius: 8px; position: relative;">
                <button onclick="closeEventoModal({{ evento.id }})" style="position: absolute; right: 20px; top: 20px; background: transparent; border: none; color: #fff; font-size: 2rem; cursor: pointer; z-index: 10;"><i class="fa-solid fa-times"></i></button>
                <div style="padding: 40px 30px;">
                    <h2 class="notranslate" style="color: var(--accent-color); font-size: 2.5rem; margin-bottom: 5px; text-align: center; font-family: 'Oswald', sans-serif; text-transform: uppercase;">{{ evento.titulo_articulo }}</h2>
                    <h3 style="text-align: center; color: #fff; font-size: 1.5rem; margin-bottom: 10px;">{{ evento.nombre_evento }}</h3>
                    <p style="text-align: center; color: #888; font-size: 1.1rem; margin-bottom: 30px;">
                        <i class="fa-solid fa-location-dot"></i> {{ evento.ciudad }}, {{ evento.pais }} | 
                        <i class="fa-solid fa-calendar-days"></i> {{ evento.fecha_evento }}<br>
                        <i class="fa-solid fa-bullhorn"></i> Promotor: {{ evento.promotor }}
                    </p>
                    <div style="text-align: center; margin-bottom: 30px;">
                        <img loading="lazy" src="{{ evento.img_video_path }}" style="width: 100%; max-width: 600px; height: auto; border-radius: 8px;">
                    </div>
                    <p style="font-size: 1.1rem; line-height: 1.8; color: #ddd; margin-bottom: 20px; text-align: justify; white-space: pre-line;">{{ evento.texto_articulo }}</p>
                    <div style="display: flex; gap: 15px; justify-content: center; margin-top: 30px;">
                        {% if evento.fb_link %}<a href="{{ evento.fb_link }}" target="_blank" class="platform-btn" style="background: #4267B2; padding: 10px 20px; font-size: 1.1rem;"><i class="fa-brands fa-facebook"></i> Evento</a>{% endif %}
                        {% if evento.ig_link %}<a href="{{ evento.ig_link }}" target="_blank" class="platform-btn" style="background: #E1306C; padding: 10px 20px; font-size: 1.1rem;"><i class="fa-brands fa-instagram"></i> Evento</a>{% endif %}
                    </div>
                </div>
            </div>
        </div>
        {% endfor %}

        <!-- BANDA MODALS (One for each band) -->"""

content = content.replace(old_modal_marker, new_modal_marker)

# 4. Add Evento Script
old_script_marker = """<script>
        // --- BANDA DE LA SEMANA SLIDER ---"""
new_script_marker = """<script>
        // --- EVENTOS DE LA SEMANA SLIDER ---
        let eventoSlideIndex = 0;
        let eventoSlides = document.getElementsByClassName("evento-slide");
        let eventoDots = document.getElementsByClassName("evento-dot");
        
        if(eventoSlides.length > 0) {
            function showEventoSlides() {
                for (let i = 0; i < eventoSlides.length; i++) {
                    eventoSlides[i].style.display = "none";  
                }
                eventoSlideIndex++;
                if (eventoSlideIndex > eventoSlides.length) {eventoSlideIndex = 1}    
                for (let i = 0; i < eventoDots.length; i++) {
                    eventoDots[i].style.backgroundColor = "#555";
                }
                if(eventoSlides[eventoSlideIndex-1]) {
                    eventoSlides[eventoSlideIndex-1].style.display = "block";  
                    if(eventoDots[eventoSlideIndex-1]) {
                        eventoDots[eventoSlideIndex-1].style.backgroundColor = "var(--accent-color)";
                    }
                }
                setTimeout(showEventoSlides, 20000); // 20 seconds
            }
            showEventoSlides();

            function currentEventoSlide(n) {
                eventoSlideIndex = n - 1;
                for (let i = 0; i < eventoSlides.length; i++) {
                    eventoSlides[i].style.display = "none";  
                }
                for (let i = 0; i < eventoDots.length; i++) {
                    eventoDots[i].style.backgroundColor = "#555";
                }
                eventoSlides[eventoSlideIndex].style.display = "block";
                if(eventoDots[eventoSlideIndex]) {
                    eventoDots[eventoSlideIndex].style.backgroundColor = "var(--accent-color)";
                }
            }
            
            // Expose globally
            window.currentEventoSlide = currentEventoSlide;
        }

        // --- BANDA DE LA SEMANA SLIDER ---"""

content = content.replace(old_script_marker, new_script_marker)

# 5. Add Modal Functions
old_modal_js_marker = """function openBandaModal(id) {"""
new_modal_js_marker = """function openEventoModal(id) {
            document.getElementById('evento-modal-' + id).style.display = 'flex';
            document.body.style.overflow = 'hidden';
        }
        function closeEventoModal(id) {
            document.getElementById('evento-modal-' + id).style.display = 'none';
            document.body.style.overflow = 'auto';
        }
        window.openEventoModal = openEventoModal;
        window.closeEventoModal = closeEventoModal;
        
        function openBandaModal(id) {"""

content = content.replace(old_modal_js_marker, new_modal_js_marker)

with open("templates/index.html", "w") as f:
    f.write(content)

print("index.html patched successfully")
