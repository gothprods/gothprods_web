with open('index.css', 'r') as f:
    content = f.read()

content = content.replace('''
body::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    pointer-events: none;
    z-index: -3;
    background: 
        radial-gradient(circle at 15% 20%, rgba(0, 104, 71, 0.35) 0%, transparent 45%),
        radial-gradient(circle at 50% 10%, rgba(255, 255, 255, 0.15) 0%, transparent 45%),
        radial-gradient(circle at 85% 20%, rgba(206, 17, 38, 0.35) 0%, transparent 45%);
}''', '''
body::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    pointer-events: none;
    z-index: -3;
    background: 
        radial-gradient(circle at 15% 20%, rgba(0, 104, 71, 0.35) 0%, transparent 45%),
        radial-gradient(circle at 50% 10%, rgba(255, 255, 255, 0.15) 0%, transparent 45%),
        radial-gradient(circle at 85% 20%, rgba(206, 17, 38, 0.35) 0%, transparent 45%);
    -webkit-mask-image: linear-gradient(to bottom, transparent 0%, transparent 50vh, black 70vh, black 100%);
    mask-image: linear-gradient(to bottom, transparent 0%, transparent 50vh, black 70vh, black 100%);
}''')

with open('index.css', 'w') as f:
    f.write(content)
