import re

with open("templates/admin_dashboard.html", "r") as f:
    content = f.read()

content = content.replace("Eventos de la Semana", "Eventos Destacados")

with open("templates/admin_dashboard.html", "w") as f:
    f.write(content)

print("Title changed in admin dashboard")
