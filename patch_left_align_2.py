with open("templates/index.html", "r") as f:
    content = f.read()

content = content.replace('class="header-titles" style="display: flex; align-items: center; gap: 15px; justify-content: center;"', 'class="header-titles" style="display: flex; align-items: center; gap: 15px; justify-content: flex-start;"')

with open("templates/index.html", "w") as f:
    f.write(content)

print("Patch 3 applied.")
