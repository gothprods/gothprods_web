import re

with open('/Users/juancarenales/Documents/Antigravity/templates/index.html', 'r') as f:
    content = f.read()

# I will find the block starting with {% if settings.get('show_banda_semana', '1') == '1' and banda_semana %}
# and ending at the corresponding {% endif %} at line 245.

new_content = """        {% if settings.get('show_banda_semana', '1') == '1' and bandas_semana %}
        <section id="banda-semana" class="section highlights-section" style="background: linear-gradient(to right, #111, #000); border-bottom: 2px solid var(--accent-color); padding: 3.5rem 5%;">
            <div class="section-header" style="margin-bottom: 20px;">
                <h2>Banda de la <span>Semana</span></h2>
            </div>
            
            <div class="banda-slider-container" style="position: relative; overflow: hidden;">
                {% for banda_semana in bandas_semana %}
                <div class="banda-slide fade" style="animation: fadeEffect 1s; {% if loop.index != 1 %}display: none;{% endif %}">
                    <div class="grid-container" style="display: flex; flex-wrap: wrap; align-items: center; gap: 20px;">
                        <div style="flex: 1; min-width: 300px; max-width: 400px; margin: 0 auto;">
                            <img src="{{ banda_semana.img_video_path }}" alt="{{ banda_semana.nombre }}" style="width: 100%; height: auto; border-radius: 12px; box-shadow: 0 10px 20px rgba(0,0,0,0.8);">
                        </div>
                        <div style="flex: 1; min-width: 300px; color: #ddd;">
                            <h3 class="notranslate" style="font-size: 2rem; color: var(--accent-color); margin-bottom: 0px; font-family: 'Oswald', sans-serif; text-transform: uppercase;">{{ banda_semana.nombre }}</h3>
                            <p style="font-size: 1rem; color: #888; margin-bottom: 10px;"><i class="fa-solid fa-location-dot"></i> {{ banda_semana.ciudad }}, {{ banda_semana.pais }}</p>
                            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; margin-top: 15px; background: rgba(0,0,0,0.3); padding: 20px; border-radius: 8px; border: 1px solid #333;">
                                
                                <!-- Columna 1: Biografía Corta -->
                                <div>
                                    <h4 style="color: var(--accent-color); font-family: 'Oswald', sans-serif; font-size: 1.1rem; text-transform: uppercase; margin-bottom: 10px; border-bottom: 1px solid #444; padding-bottom: 5px;"><i class="fa-solid fa-align-left"></i> Biografía</h4>
                                    <p style="font-size: 0.95rem; line-height: 1.4; margin-bottom: 15px;">{{ banda_semana.bio_corta }}</p>
                                    <button onclick="openBandaModal({{ banda_semana.id }})" style="background: transparent; color: var(--accent-color); border: 1px solid var(--accent-color); padding: 5px 12px; font-size: 0.85rem; border-radius: 4px; cursor: pointer; text-transform: uppercase; font-family: 'Oswald', sans-serif; letter-spacing: 1px; transition: all 0.3s;"><i class="fa-solid fa-book-open"></i> Leer historia completa</button>
                                </div>

                                <!-- Columna 2: Alineación y Discografía -->
                                <div>
                                    {% if banda_semana.line_up %}
                                    <h4 style="color: var(--accent-color); font-family: 'Oswald', sans-serif; font-size: 1.1rem; text-transform: uppercase; margin-bottom: 10px; border-bottom: 1px solid #444; padding-bottom: 5px;"><i class="fa-solid fa-users"></i> Alineación Actual</h4>
                                    <p style="font-size: 0.95rem; line-height: 1.4; color: #ccc; margin-bottom: 15px; white-space: pre-line;">{{ banda_semana.line_up }}</p>
                                    {% endif %}

                                    {% if banda_semana.discografia %}
                                    <h4 style="color: var(--accent-color); font-family: 'Oswald', sans-serif; font-size: 1.1rem; text-transform: uppercase; margin-bottom: 10px; border-bottom: 1px solid #444; padding-bottom: 5px;"><i class="fa-solid fa-list-ul"></i> Discografía</h4>
                                    <p style="font-size: 0.9rem; line-height: 1.4; color: #aaa; white-space: pre-line; margin-bottom: 15px;">{{ banda_semana.discografia }}</p>
                                    {% endif %}
                                </div>

                                <!-- Columna 3: Último Lanzamiento -->
                                {% if banda_semana.ultimo_lanzamiento_sp_link or banda_semana.ultimo_lanzamiento_ap_link %}
                                <div>
                                    <h4 style="color: var(--accent-color); font-family: 'Oswald', sans-serif; font-size: 1.1rem; text-transform: uppercase; margin-bottom: 10px; border-bottom: 1px solid #444; padding-bottom: 5px;">
                                        <i class="fa-solid fa-compact-disc"></i> Último Lanzamiento
                                    </h4>
                                    {% if banda_semana.ultimo_lanzamiento_titulo %}
                                    <p style="font-size: 0.95rem; color: #fff; margin-bottom: 10px; font-weight: bold;">{{ banda_semana.ultimo_lanzamiento_titulo }} {% if banda_semana.ultimo_lanzamiento_tipo %}<span style="color: #aaa; font-weight: normal;">({{ banda_semana.ultimo_lanzamiento_tipo }})</span>{% endif %}</p>
                                    {% endif %}
                                    
                                    <!-- Reproductor Iframe y Botones Apareados -->
                                    <div style="display: flex; flex-direction: column; gap: 15px;">
                                        {% if banda_semana.ultimo_lanzamiento_sp_link %}
                                        <div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
                                            <div style="flex: 1; min-width: 140px;">
                                                <iframe style="border-radius:12px; border: none; background: #000;" src="{{ banda_semana.ultimo_lanzamiento_sp_link }}" width="100%" height="152" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
                                            </div>
                                            <a href="{{ banda_semana.ultimo_lanzamiento_sp_link | replace('open.spotify.com/embed/', 'open.spotify.com/') }}" target="_blank" class="platform-btn spotify-btn" style="display: flex; align-items: center; justify-content: center; padding: 6px 10px; font-size: 0.8rem; border-radius: 6px; gap: 5px; min-width: 80px;"><i class="fa-brands fa-spotify"></i> Spotify</a>
                                        </div>
                                        {% endif %}

                                        {% if banda_semana.ultimo_lanzamiento_ap_link %}
                                        <div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
                                            <div style="flex: 1; min-width: 140px;">
                                                <iframe allow="autoplay *; encrypted-media *; fullscreen *; clipboard-write" frameborder="0" height="152" style="width:100%;max-width:660px;overflow:hidden;background:#000;border-radius:12px; border: none;" sandbox="allow-forms allow-popups allow-same-origin allow-scripts allow-top-navigation-by-user-activation" src="{{ banda_semana.ultimo_lanzamiento_ap_link }}{{ '&theme=dark' if '?' in banda_semana.ultimo_lanzamiento_ap_link else '?theme=dark' }}"></iframe>
                                            </div>
                                            <a href="{{ banda_semana.ultimo_lanzamiento_ap_link | replace('embed.', '') }}" target="_blank" class="platform-btn apple-btn" style="display: flex; align-items: center; justify-content: center; padding: 6px 10px; font-size: 0.8rem; border-radius: 6px; gap: 5px; min-width: 80px;"><i class="fa-brands fa-apple"></i> Apple</a>
                                        </div>
                                        {% endif %}
                                    </div>
                                </div>
                                {% endif %}
                            </div>

                            <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-top: 15px;">
                                {% if banda_semana.ig_link %}<a href="{{ banda_semana.ig_link }}" target="_blank" class="platform-btn" style="background: #E1306C; padding: 6px 12px; font-size: 0.9rem;"><i class="fa-brands fa-instagram"></i></a>{% endif %}
                                {% if banda_semana.fb_link %}<a href="{{ banda_semana.fb_link }}" target="_blank" class="platform-btn" style="background: #4267B2; padding: 6px 12px; font-size: 0.9rem;"><i class="fa-brands fa-facebook"></i></a>{% endif %}
                                {% if banda_semana.tk_link %}<a href="{{ banda_semana.tk_link }}" target="_blank" class="platform-btn" style="background: #000000; border: 1px solid #333; padding: 6px 12px; font-size: 0.9rem;"><i class="fa-brands fa-tiktok"></i></a>{% endif %}
                                {% if banda_semana.sp_link %}<a href="{{ banda_semana.sp_link }}" target="_blank" class="platform-btn spotify-btn" style="padding: 6px 12px; font-size: 0.9rem;"><i class="fa-brands fa-spotify"></i></a>{% endif %}
                                {% if banda_semana.ap_link %}<a href="{{ banda_semana.ap_link }}" target="_blank" class="platform-btn apple-btn" style="padding: 6px 12px; font-size: 0.9rem;"><i class="fa-solid fa-podcast"></i></a>{% endif %}
                                {% if banda_semana.yt_link %}<a href="{{ banda_semana.yt_link }}" target="_blank" class="platform-btn" style="padding: 6px 12px; font-size: 0.9rem;"><i class="fa-brands fa-youtube"></i></a>{% endif %}
                            </div>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>

            <!-- Slider Dots -->
            <div style="text-align: center; margin-top: 30px;">
                {% for banda_semana in bandas_semana %}
                <span class="banda-dot {% if loop.index == 1 %}active{% endif %}" onclick="currentBandaSlide({{ loop.index }})" style="height: 12px; width: 12px; margin: 0 5px; background-color: {% if loop.index == 1 %}var(--accent-color){% else %}#555{% endif %}; border-radius: 50%; display: inline-block; cursor: pointer; transition: background-color 0.3s ease;"></span>
                {% endfor %}
            </div>

        </section>

        <!-- BANDA MODALS (One for each band) -->
        {% for banda_semana in bandas_semana %}
        <div id="banda-modal-{{ banda_semana.id }}" class="banda-modal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.9); z-index: 9999; justify-content: center; align-items: center; padding: 20px;">
            <div id="banda-modal-content-{{ banda_semana.id }}" style="background: #111; max-width: 800px; width: 100%; max-height: 90vh; overflow-y: auto; border: 1px solid var(--accent-color); border-radius: 8px; position: relative;">
                <button onclick="closeBandaModal({{ banda_semana.id }})" style="position: absolute; right: 20px; top: 20px; background: transparent; border: none; color: #fff; font-size: 2rem; cursor: pointer; z-index: 10;"><i class="fa-solid fa-times"></i></button>
                <div style="padding: 40px 30px;">
                    <h2 class="notranslate" style="color: var(--accent-color); font-size: 3rem; margin-bottom: 5px; text-align: center; font-family: 'Oswald', sans-serif; text-transform: uppercase;">{{ banda_semana.nombre }}</h2>
                    <p style="text-align: center; color: #888; font-size: 1.1rem; margin-bottom: 30px;">
                        <i class="fa-solid fa-location-dot"></i> Origen: {{ banda_semana.ciudad }}, {{ banda_semana.pais }}
                        {% if banda_semana.ano_formacion %} | <i class="fa-solid fa-calendar-days"></i> Formación: {{ banda_semana.ano_formacion }}{% endif %}
                    </p>
                    <div style="text-align: center; margin-bottom: 30px;">
                        <img src="{{ banda_semana.img_video_path }}" style="width: 100%; max-width: 600px; height: auto; border-radius: 8px;">
                    </div>

                    {% if banda_semana.line_up %}
                    <div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 8px; margin-bottom: 30px; text-align: center; border-left: 3px solid var(--accent-color);">
                        <p style="margin: 0; color: #ccc; font-size: 1rem;"><strong><i class="fa-solid fa-users"></i> Line Up:</strong> {{ banda_semana.line_up }}</p>
                    </div>
                    {% endif %}

                    <p style="font-size: 1.1rem; line-height: 1.8; color: #ddd; margin-bottom: 20px; text-align: justify; white-space: pre-line;">{{ banda_semana.bio_larga if banda_semana.bio_larga else banda_semana.bio_corta }}</p>

                    {% if banda_semana.titulo_resena and banda_semana.texto_resena %}
                    <div style="background: rgba(113, 109, 74, 0.1); padding: 25px; border-radius: 8px; margin-top: 30px; border-left: 4px solid var(--accent-color);">
                        <h3 style="color: var(--accent-color); font-size: 1.8rem; margin-bottom: 15px; font-family: 'Oswald', sans-serif; text-transform: uppercase;"><i class="fa-solid fa-pen-nib"></i> {{ banda_semana.titulo_resena }}</h3>
                        <p style="font-size: 1.1rem; line-height: 1.8; color: #ddd; margin: 0; text-align: justify; white-space: pre-line;">{{ banda_semana.texto_resena }}</p>
                    </div>
                    {% endif %}
                </div>
            </div>
        </div>
        {% endfor %}

        <script>
            let bandaSlideIndex = 1;
            let bandaSlideInterval;

            function showBandaSlides(n) {
                let slides = document.getElementsByClassName("banda-slide");
                let dots = document.getElementsByClassName("banda-dot");
                if (slides.length === 0) return;
                if (n > slides.length) {bandaSlideIndex = 1}    
                if (n < 1) {bandaSlideIndex = slides.length}
                for (let i = 0; i < slides.length; i++) {
                    slides[i].style.display = "none";  
                }
                for (let i = 0; i < dots.length; i++) {
                    dots[i].style.backgroundColor = "#555";
                }
                slides[bandaSlideIndex-1].style.display = "block";  
                dots[bandaSlideIndex-1].style.backgroundColor = "var(--accent-color)";
            }

            function currentBandaSlide(n) {
                clearInterval(bandaSlideInterval);
                showBandaSlides(bandaSlideIndex = n);
                startBandaSlideTimer();
            }

            function startBandaSlideTimer() {
                bandaSlideInterval = setInterval(function() {
                    bandaSlideIndex++;
                    showBandaSlides(bandaSlideIndex);
                }, 30000);
            }

            document.addEventListener("DOMContentLoaded", function() {
                if(document.getElementsByClassName("banda-slide").length > 0) {
                    showBandaSlides(bandaSlideIndex);
                    startBandaSlideTimer();
                }
            });

            function openBandaModal(id) { 
                document.getElementById('banda-modal-' + id).style.display = 'flex'; 
                document.body.style.overflow = 'hidden'; 
            }
            function closeBandaModal(id) { 
                document.getElementById('banda-modal-' + id).style.display = 'none'; 
                document.body.style.overflow = 'auto'; 
            }

            // Cerrar con Escape
            document.addEventListener('keydown', function(event) {
                if (event.key === "Escape" || event.keyCode === 27) {
                    let modals = document.getElementsByClassName('banda-modal');
                    for (let i = 0; i < modals.length; i++) {
                        modals[i].style.display = 'none';
                    }
                    document.body.style.overflow = 'auto';
                }
            });

            // Cerrar al hacer clic fuera del modal content
            document.addEventListener('click', function(event) {
                let modals = document.getElementsByClassName('banda-modal');
                for (let i = 0; i < modals.length; i++) {
                    if (event.target === modals[i]) {
                        modals[i].style.display = 'none';
                        document.body.style.overflow = 'auto';
                    }
                }
            });
        </script>
        {% endif %}"""

pattern = r"{% if settings\.get\('show_banda_semana', '1'\) == '1' and banda_semana %}.*?{% endif %}\n"
import re
new_full_content = re.sub(pattern, new_content.replace('\\', '\\\\') + '\n', content, flags=re.DOTALL)

with open('/Users/juancarenales/Documents/Antigravity/templates/index.html', 'w') as f:
    f.write(new_full_content)
