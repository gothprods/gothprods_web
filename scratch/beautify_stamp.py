with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_badge = '<div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(-15deg); background: rgba(200,0,0,0.9); color: white; border: 3px solid white; padding: 10px 20px; font-size: 1.5rem; font-weight: 900; letter-spacing: 4px; border-radius: 10px; z-index: 10; text-shadow: 2px 2px 0 #000; box-shadow: 0 0 15px rgba(255,0,0,0.5); text-transform: uppercase; pointer-events: none; width: 85%; text-align: center;">CANCELADO</div>'

new_badge = '<div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(-12deg); background: rgba(10, 0, 0, 0.9); color: #ff1e1e; border: 4px double #ff1e1e; padding: 10px 15px; font-size: 1.6rem; font-weight: 900; letter-spacing: 5px; border-radius: 8px; z-index: 10; text-shadow: 0 0 8px rgba(255, 30, 30, 0.8); box-shadow: 0 0 15px rgba(255, 30, 30, 0.5), inset 0 0 10px rgba(255, 30, 30, 0.3); text-transform: uppercase; pointer-events: none; width: 85%; text-align: center; font-family: \'Oswald\', sans-serif;">CANCELADO</div>'

# Also let's tweak the container to be slightly less grayscale (so you can see some color of the band) but darker
old_container = 'style="opacity: 0.7; filter: grayscale(80%); position: relative;"'
new_container = 'style="opacity: 0.75; filter: grayscale(60%) sepia(20%) hue-rotate(-10deg); position: relative;"'

content = content.replace(old_badge, new_badge)
content = content.replace(old_container, new_container)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Stamp beautified")
