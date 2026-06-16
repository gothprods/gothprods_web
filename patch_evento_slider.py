import re

with open("templates/index.html", "r") as f:
    content = f.read()

# 1. Update truncate to 1300
content = content.replace("{{ evento.bio_corta|truncate(1200) }}", "{{ evento.bio_corta|truncate(1300) }}")

# 2. Add JS logic for evento-slide
js_evento_logic = """            let eventoSlideIndex = 1;
            let eventoSlideInterval;

            function showEventoSlides(n) {
                let slides = document.getElementsByClassName("evento-slide");
                let dots = document.getElementsByClassName("evento-dot");
                if (slides.length === 0) return;
                if (n > slides.length) {eventoSlideIndex = 1}    
                if (n < 1) {eventoSlideIndex = slides.length}
                for (let i = 0; i < slides.length; i++) {
                    slides[i].style.display = "none";  
                }
                for (let i = 0; i < dots.length; i++) {
                    dots[i].style.backgroundColor = "#555";
                }
                slides[eventoSlideIndex-1].style.display = "block";  
                dots[eventoSlideIndex-1].style.backgroundColor = "var(--accent-color)";
            }

            function currentEventoSlide(n) {
                clearInterval(eventoSlideInterval);
                showEventoSlides(eventoSlideIndex = n);
                startEventoSlideTimer();
            }

            function startEventoSlideTimer() {
                eventoSlideInterval = setInterval(function() {
                    eventoSlideIndex++;
                    showEventoSlides(eventoSlideIndex);
                }, 20000); // 20 seconds
            }

            document.addEventListener("DOMContentLoaded", function() {
                if(document.getElementsByClassName("evento-slide").length > 0) {
                    showEventoSlides(eventoSlideIndex);
                    startEventoSlideTimer();
                }
            });
"""

# Insert right after DOMContentLoaded for bandas
content = content.replace("""            document.addEventListener("DOMContentLoaded", function() {
                if(document.getElementsByClassName("banda-slide").length > 0) {
                    showBandaSlides(bandaSlideIndex);
                    startBandaSlideTimer();
                }
            });""", """            document.addEventListener("DOMContentLoaded", function() {
                if(document.getElementsByClassName("banda-slide").length > 0) {
                    showBandaSlides(bandaSlideIndex);
                    startBandaSlideTimer();
                }
            });
""" + "\n" + js_evento_logic)


# 3. Export currentEventoSlide to window object so inline onclick works
content = content.replace("window.closeEventoModal = closeEventoModal;", """window.closeEventoModal = closeEventoModal;
        window.currentEventoSlide = currentEventoSlide;""")


with open("templates/index.html", "w") as f:
    f.write(content)

print("Evento logic updated successfully")
