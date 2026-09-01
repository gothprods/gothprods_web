with open('index.css', 'r') as f:
    content = f.read()

content = content.replace('''
.hero {
    min-height: 50vh;
    display: flex;
    align-items: center;
    padding: 80px 5% 40px 5%; /* Adjusted padding for removed navbar */
    margin-top: 0;
    position: relative;
    overflow: hidden;
}''', '''
.hero {
    min-height: 50vh;
    display: flex;
    align-items: center;
    padding: 80px 5% 40px 5%; /* Adjusted padding for removed navbar */
    margin-top: 0;
    position: relative;
    overflow: hidden;
    background-color: var(--bg-color);
    isolation: isolate;
}''')

with open('index.css', 'w') as f:
    f.write(content)
