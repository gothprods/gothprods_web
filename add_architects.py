import re

html_path = 'index.html'
with open(html_path, 'r') as f:
    html = f.read()

# 1. Remove Language Switcher
lang_switcher_pattern = re.compile(
    r'<div class="lang-switcher".*?</div>\s*</nav>',
    re.DOTALL
)
html = lang_switcher_pattern.sub('</nav>', html)

# 2. Add Architects Review Card
new_card = """
                <div class="card review-card">
                    <div class="card-image" style="background-image: url('assets/architects_review.png');">
                    </div>
                    <div class="card-content">
                        <span class="badge">Nuevo</span>
                        <h3 style="margin-top: 10px; font-size: 1.4rem;">BRUTAL CORONACIÓN DE ARCHITECTS EN EL VELÓDROMO</h3>
                        <p>La oscuridad capitalina fue testigo de una liturgia brutal donde el asfalto retumbó bajo el peso del metal moderno. La maquinaria comandada por Sam Carter demostró su poderío absoluto.</p>
                        <a href="javascript:void(0);" data-target="reviewModal5" class="read-more open-review-modal"
                            style="color: var(--accent-color); font-weight: bold; text-transform: uppercase;">Leer
                            reseña completa &rarr;</a>
                    </div>
                </div>

"""
# Find the start of the triple-grid
triple_grid_pattern = re.compile(r'(<div class="grid-container triple-grid">)')
html = triple_grid_pattern.sub(r'\1\n' + new_card, html)

# 3. Add Architects Modal
new_modal = """
    <!-- Review Modal 5 (Architects) -->
    <div id="reviewModal5" class="modal">
        <div class="modal-content">
            <span class="close-modal">&times;</span>
            <img src="assets/architects_review.png" alt="Architects Banner" class="modal-banner">
            <div class="modal-body">
                <h2>BRUTAL CORONACIÓN DE ARCHITECTS EN EL VELÓDROMO</h2>

                <p>La oscuridad capitalina fue testigo de una liturgia brutal donde el asfalto retumbó bajo el peso del metal moderno. En una velada donde la sangre joven reclamó su lugar en el panteón del ruido, la maquinaria comandada por Sam Carter demostró por qué están destinados a heredar el trono de una escena que poco a poco despide a sus leyendas caídas.</p>

                <p>La hostilidad sonora comenzó con el asalto de los lobos suecos, Thrown, quienes, a pesar de hacer esperar a su jauría por unos instantes, desataron un vendaval de new metalcore abrasador. Su ejecución en directo fue un mazo directo al cráneo, perfecto para encender las brasas del moshpit, aunque los devotos de las frecuencias más oscuras sintieron la ausencia de esa bestia invisible: el golpe subsónico, esa frecuencia aplastante que te roba el aliento desde el pecho. Fue, sin duda, una advertencia sónica y un aperitivo cruento antes del inminente asalto estelar.</p>

                <p>Cuando Architects tomó esta catedral de concreto, la devoción fue absoluta. A través de una travesía que cruzó desde la agresividad implacable de sus primeros himnos hasta las texturas más melódicas y reflexivas de sus recientes placas discográficas, la banda conjuró un infierno encantador. Cañonazos como "Animals" y "Doomsday" hicieron estallar la cordura de los presentes; el recinto se convirtió en un océano de cuerpos colisionando, iluminado por el fuego pagano de las bengalas. Aunque el monstruo de los graves profundos no rugió desde la mesa de audio con la fuerza de antaño, la entrega visceral de los británicos bastó para hacer colapsar el lugar de pura energía.</p>

                <p>La consagración de Architects en el asfalto mexicano no fue un evento aislado, sino el cumplimiento de una profecía ineludible. Mientras la vieja guardia de las grandes arenas comienza a despedirse y nuestras leyendas ceden sus coronas, la maquinaria británica demostró tener los pulmones, la rabia y la maestría técnica para cargar con el peso del metal mundial sobre sus hombros. Sam Carter y los suyos no solo comandaron una carnicería sonora durante más de hora y media; reventaron el recinto con la autoridad absoluta de quienes están destinados a adueñarse de los carteles masivos en los años venideros. El velódromo quedó marcado por el fuego y la sentencia dictada frente a miles de almas: el futuro del ruido extremo está asegurado y su arquitectura es inquebrantable.</p>
            </div>
        </div>
    </div>
"""
# Insert before the closing body tag or right before the <script src="app.js"></script>
script_pattern = re.compile(r'(<script src="app.js"></script>)')
html = script_pattern.sub(new_modal + r'\n\1', html)

with open(html_path, 'w') as f:
    f.write(html)

print("Updated with Architects review!")
