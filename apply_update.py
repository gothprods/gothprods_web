import os
import re

html_path = 'index.html'

def apply_update():
    # File info
    title = "Los Venues Favoritos en US: Sphere y Allegiant Stadium"
    short_desc = "Recientemente, la revista Billboard ha posicionado a estos dos recintos de Las Vegas en la cima absoluta del éxito global..."
    full_desc = """Recientemente, la revista Billboard ha posicionado a estos dos recintos de Las Vegas en la cima absoluta del éxito global, nombrando a la Sphere como el recinto de entretenimiento con mayor recaudación en el mundo y al Allegiant Stadium como el estadio de mayores ingresos en Estados Unidos y el segundo a nivel mundial.

A continuación, te contamos por qué dominan la industria:

The Sphere
Su interior alberga una monumental pantalla LED envolvente de resolución 16K y un sistema de sonido direccional que sumergen al público en una experiencia sensorial y cinematográfica inigualable.

Demostró ser el recinto más rentable a nivel global al generar ingresos históricos mediante un modelo de negocios premium que prioriza la calidad y exclusividad sobre la cantidad de eventos.

Está redefiniendo el futuro del entretenimiento en vivo al combinar exitosamente conciertos y deportes, como las artes marciales mixtas, con narrativas visuales de vanguardia.

Allegiant Stadium
Posee una de las arquitecturas más innovadoras de la liga, destacando su techo translúcido y sus enormes ventanas retráctiles de vidrio que enmarcan a la perfección el horizonte de la ciudad.

En su interior resguarda la imponente Antorcha Conmemorativa de Al Davis, una estructura impresa en 3D de 93 pies de altura que funciona con fuego real y es considerada una maravilla de la ingeniería.

Revolucionó la experiencia de los aficionados al ofrecer comodidades dignas de un resort de lujo, con conectividad de última generación, espacios exclusivos y una oferta gastronómica de primer nivel."""
    
    img_name = "updates/Los_Venues_Favoritos_en_US_Sphere_y_Allegiant_Stadium.png"
    modal_id = "newsModal100" # Unique ID

    # Generate HTML chunks
    new_card = f"""
                <div class="news-card">
                    <img src="{img_name}" alt="{title}" style="width: 100%; border-radius: 8px; margin-bottom: 10px; height: 140px; object-fit: cover; object-position: center;">
                    <h3 style="font-size: 1rem; line-height: 1.2;">{title.upper()}</h3>
                    <p style="font-size: 0.85rem; margin-bottom: 10px;">{short_desc}</p>
                    <a href="javascript:void(0);" data-target="{modal_id}" class="open-review-modal" style="color: var(--accent-color); font-weight: bold; font-size: 0.85rem;">Leer más &rarr;</a>
                </div>"""

    new_modal = f"""
    <!-- Modal para Noticia Nueva -->
    <div id="{modal_id}" class="modal">
        <div class="modal-content">
            <span class="close-modal">&times;</span>
            <h2 style="color: var(--accent-color); margin-bottom: 20px;">{title}</h2>
            <img src="{img_name}" style="width: 100%; border-radius: 8px; margin-bottom: 20px;">
            <div style="color: #ccc; line-height: 1.6; white-space: pre-line;">
                {full_desc}
            </div>
        </div>
    </div>
    """

    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Inject Card into <div class="news-rail">
    rail_start = html_content.find('<div class="news-rail">')
    if rail_start != -1:
        insert_pos = html_content.find('>', rail_start) + 1
        html_content = html_content[:insert_pos] + new_card + html_content[insert_pos:]

    # Inject Modal before </body>
    body_end = html_content.rfind('</body>')
    if body_end != -1:
        html_content = html_content[:body_end] + new_modal + html_content[body_end:]

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == "__main__":
    apply_update()
    print("Update applied to index.html!")
