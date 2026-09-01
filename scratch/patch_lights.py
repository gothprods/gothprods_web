with open('index.css', 'r') as f:
    content = f.read()

old_lights = '''    background: 
        radial-gradient(circle at 15% 20%, rgba(0, 104, 71, 0.15) 0%, transparent 40%),
        radial-gradient(circle at 50% 10%, rgba(255, 255, 255, 0.08) 0%, transparent 40%),
        radial-gradient(circle at 85% 20%, rgba(206, 17, 38, 0.15) 0%, transparent 40%);'''

new_lights = '''    background: 
        radial-gradient(circle at 15% 20%, rgba(0, 104, 71, 0.35) 0%, transparent 45%),
        radial-gradient(circle at 50% 10%, rgba(255, 255, 255, 0.15) 0%, transparent 45%),
        radial-gradient(circle at 85% 20%, rgba(206, 17, 38, 0.35) 0%, transparent 45%);'''

content = content.replace(old_lights, new_lights)

with open('index.css', 'w') as f:
    f.write(content)
