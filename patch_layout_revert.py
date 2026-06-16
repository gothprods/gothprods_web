import re

with open("templates/index.html", "r") as f:
    content = f.read()

# 1. Change the wrapper back to side-by-side
old_wrapper = """        <section id="banda-eventos-semana" class="section highlights-section" style="background: linear-gradient(to right, #111, #000); border-bottom: 2px solid var(--accent-color); padding: 3.5rem 5%;">
            <div style="display: flex; flex-direction: column; gap: 60px;">"""
new_wrapper = """        <section id="banda-eventos-semana" class="section highlights-section" style="background: linear-gradient(to right, #111, #000); border-bottom: 2px solid var(--accent-color); padding: 3.5rem 5%;">
            <div style="display: flex; flex-wrap: wrap; gap: 40px;">"""
content = content.replace(old_wrapper, new_wrapper)

# 2. Adjust Banda Slide
old_banda = """                    <div class="grid-container" style="display: flex; flex-wrap: wrap; align-items: center; gap: 20px;">
                <div style="flex: 1; min-width: 300px; max-width: 400px; margin: 0 auto;">
                    <img loading="lazy" src="{{ banda_semana.img_video_path }}" alt="{{ banda_semana.nombre }}" style="width: 100%; height: auto; border-radius: 12px; box-shadow: 0 10px 20px rgba(0,0,0,0.8);">
                </div>
                <div style="flex: 1; min-width: 300px; color: #ddd;">"""

new_banda = """                    <div class="grid-container" style="display: flex; flex-wrap: wrap; align-items: center; gap: 20px;">
                <div style="flex: 1; min-width: 200px; max-width: 350px; margin: 0 auto;">
                    <img loading="lazy" src="{{ banda_semana.img_video_path }}" alt="{{ banda_semana.nombre }}" style="width: 100%; height: auto; border-radius: 12px; box-shadow: 0 10px 20px rgba(0,0,0,0.8);">
                </div>
                <div style="flex: 1; min-width: 250px; color: #ddd;">"""
content = content.replace(old_banda, new_banda)

# 3. Adjust Evento Slide
old_evento = """                        <div class="grid-container" style="display: flex; flex-wrap: wrap; align-items: center; gap: 20px;">
                            <div style="flex: 1; min-width: 300px; max-width: 400px; margin: 0 auto;">
                                <img loading="lazy" src="{{ evento.img_video_path }}" alt="{{ evento.nombre_evento }}" style="width: 100%; height: auto; border-radius: 12px; box-shadow: 0 10px 20px rgba(0,0,0,0.8);">
                            </div>
                            <div style="flex: 1; min-width: 300px; color: #ddd;">"""

new_evento = """                        <div class="grid-container" style="display: flex; flex-wrap: wrap; align-items: center; gap: 20px;">
                            <div style="flex: 1; min-width: 200px; max-width: 350px; margin: 0 auto;">
                                <img loading="lazy" src="{{ evento.img_video_path }}" alt="{{ evento.nombre_evento }}" style="width: 100%; height: auto; border-radius: 12px; box-shadow: 0 10px 20px rgba(0,0,0,0.8);">
                            </div>
                            <div style="flex: 1; min-width: 250px; color: #ddd;">"""
content = content.replace(old_evento, new_evento)

with open("templates/index.html", "w") as f:
    f.write(content)

print("Layout reverted to side-by-side with inner wrap adjustments")
