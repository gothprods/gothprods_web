with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_badge = '<div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(-12deg); background: rgba(10, 0, 0, 0.9); color: #ff1e1e; border: 4px double #ff1e1e; padding: 10px 15px; font-size: 1.6rem; font-weight: 900; letter-spacing: 5px; border-radius: 8px; z-index: 10; text-shadow: 0 0 8px rgba(255, 30, 30, 0.8); box-shadow: 0 0 15px rgba(255, 30, 30, 0.5), inset 0 0 10px rgba(255, 30, 30, 0.3); text-transform: uppercase; pointer-events: none; width: 85%; text-align: center; font-family: \'Oswald\', sans-serif;">CANCELADO</div>'

new_badge = '<div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(-12deg); background: rgba(0, 0, 0, 0.85); color: #ff0000; border: 4px double #ff0000; padding: 10px 15px; font-size: 1.6rem; font-weight: 900; letter-spacing: 5px; border-radius: 8px; z-index: 10; text-shadow: 0 0 10px rgba(255, 0, 0, 1); box-shadow: 0 0 15px rgba(255, 0, 0, 0.8), inset 0 0 12px rgba(255, 0, 0, 0.6); text-transform: uppercase; pointer-events: none; width: 85%; text-align: center; font-family: \'Oswald\', sans-serif;">CANCELADO</div>'

content = content.replace(old_badge, new_badge)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Stamp red upgraded")
