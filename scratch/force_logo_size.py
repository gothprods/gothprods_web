with open('index.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Force the size with important
css = css.replace(
    ".dock-logo img {\n    width: 65px;\n    height: auto;",
    ".dock-logo img {\n    width: 65px !important;\n    height: 65px !important;\n    object-fit: contain;"
)

css = css.replace(
    ".dock-logo img {\n        width: 55px;\n    }",
    ".dock-logo img {\n        width: 55px !important;\n        height: 55px !important;\n        object-fit: contain;\n    }"
)

css = css.replace(
    ".dock-socials a, .dock-auth a { font-size: 1rem; }\n    .dock-logo img { width: 52px; }",
    ".dock-socials a, .dock-auth a { font-size: 1rem; }\n    .dock-logo img { width: 52px !important; height: 52px !important; object-fit: contain; }"
)

with open('index.css', 'w', encoding='utf-8') as f:
    f.write(css)

# Update cache buster
with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('href="/index.css?v=63"', 'href="/index.css?v=64"')
html = html.replace('assets/dock_header_icon.png\').lstrip(\'/\') }}?v=63"', 'assets/dock_header_icon.png\').lstrip(\'/\') }}?v=64"')

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Forced size and updated cache buster")
