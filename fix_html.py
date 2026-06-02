import re

with open('index.html', 'r') as f:
    html = f.read()

# Fix the invalid escaped quotes in the onerror attributes
html = html.replace(r"this.style.display=\'none\';", "this.style.display='none';")
html = html.replace(r"this.closest(\'.agenda-item\').classList.add(\'no-logo\');", "this.closest('.agenda-item').classList.add('no-logo');")

with open('index.html', 'w') as f:
    f.write(html)
