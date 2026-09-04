with open('index.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Desktop original (width: 50px) -> 65px
css = css.replace(
    ".dock-logo img {\n    width: 50px;",
    ".dock-logo img {\n    width: 65px;"
)

# Short screen (width: 40px) -> 52px
css = css.replace(
    ".dock-socials a, .dock-auth a { font-size: 1rem; }\n    .dock-logo img { width: 40px; }",
    ".dock-socials a, .dock-auth a { font-size: 1rem; }\n    .dock-logo img { width: 52px; }"
)

# Mobile (width: 40px) -> 55px
css = css.replace(
    ".dock-logo img {\n        width: 40px;\n    }",
    ".dock-logo img {\n        width: 55px;\n    }"
)

with open('index.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Logo resized")
