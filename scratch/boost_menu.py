with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the inline style for inactive icons
content = content.replace(
    "opacity: 0.3; pointer-events: none; filter: grayscale(100%);",
    "opacity: 0.65; pointer-events: none; filter: grayscale(100%) brightness(1.5);"
)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('index.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Boost default icons
css = css.replace(
    "border: 1px solid rgba(113, 109, 74, 0.4);\n    border-radius: 50%;",
    "border: 1px solid rgba(113, 109, 74, 0.6);\n    border-radius: 50%;\n    filter: brightness(1.2) drop-shadow(0 0 3px rgba(113, 109, 74, 0.3));"
)

# Boost hover effect
css = css.replace(
    ".dock-item:hover a {\n    color: var(--accent-color);\n}",
    ".dock-item:hover a {\n    color: var(--accent-color);\n}\n.dock-item:hover a img {\n    filter: brightness(1.5) drop-shadow(0 0 10px rgba(113, 109, 74, 0.8));\n    border-color: var(--accent-color);\n}"
)

# Boost hover logic opacity
css = css.replace(
    ".dock-menu:hover .dock-item {\n    opacity: 0.6;\n}",
    ".dock-menu:hover .dock-item {\n    opacity: 0.75;\n}"
)

with open('index.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Boost applied.")
