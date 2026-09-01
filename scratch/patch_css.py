with open('index.css', 'r') as f:
    content = f.read()

old_body = '''body {
    background-color: var(--bg-color);
    color: var(--text-main);
    font-family: var(--font-body);
    line-height: 1.6;
    font-size: 1.3rem;
}'''

new_body = '''body {
    background-color: var(--bg-color);
    color: var(--text-main);
    font-family: var(--font-body);
    line-height: 1.6;
    font-size: 1.3rem;
}

body::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    pointer-events: none;
    z-index: -1;
    background: 
        radial-gradient(circle at 15% 20%, rgba(0, 104, 71, 0.15) 0%, transparent 40%),
        radial-gradient(circle at 50% 10%, rgba(255, 255, 255, 0.08) 0%, transparent 40%),
        radial-gradient(circle at 85% 20%, rgba(206, 17, 38, 0.15) 0%, transparent 40%);
}'''

content = content.replace(old_body, new_body)

with open('index.css', 'w') as f:
    f.write(content)
