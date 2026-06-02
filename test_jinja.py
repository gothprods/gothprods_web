from flask import Flask, render_template
import app

with app.app.app_context():
    try:
        render_template('index.html', noticiero_items=[], reseñas_items=[], entrevistas_items=[], galeria_items=[], metalpulse_items=[], metalpulse_tracks=[], caossonoro_items=[], agenda_grouped={}, agenda_items=[], upcoming_agenda=[], settings={})
        print("Success")
    except Exception as e:
        print(f"Error: {e}")
