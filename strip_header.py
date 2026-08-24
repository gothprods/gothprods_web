import os
import glob
import re

files_to_patch = ['templates/articulo.html', 'templates/banda.html', 'templates/evento.html', 'templates/mexapedia.html']

for filepath in files_to_patch:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove header
    content = re.sub(r'<header class="navbar">.*?</header>', '', content, flags=re.DOTALL)
    
    # Remove sidebar-menu
    content = re.sub(r'<div id="sidebar-menu" class="sidebar">.*?</div>\s*<!-- MAIN CONTENT -->', '<!-- MAIN CONTENT -->', content, flags=re.DOTALL)
    
    # Remove old main-nav if it exists
    content = re.sub(r'<nav class="main-nav" id="main-nav">.*?</nav>', '', content, flags=re.DOTALL)
    
    # Adjust padding-top in <main>
    content = re.sub(r'padding-top:\s*100px;', 'padding-top: 40px;', content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Headers and sidebars removed successfully.")
