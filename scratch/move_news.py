with open('templates/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1

# Buscamos la SECCIÓN de news
for i, line in enumerate(lines):
    if '<section id="news"' in line:
        if "{% if settings.get('show_news'" in lines[i-1]:
            start_idx = i - 1
        elif "{% if settings.get('show_news'" in lines[i-2]:
            start_idx = i - 2
        else:
            start_idx = i
        break

if start_idx != -1:
    for i in range(start_idx, len(lines)):
        if "{% endif %}" in lines[i] and "</section>" in lines[i-1]:
            end_idx = i
            break

print(f"News start: {start_idx}, end: {end_idx}")

if start_idx != -1 and end_idx != -1:
    news_block = lines[start_idx:end_idx+1]
    
    del lines[start_idx:end_idx+1]
    
    reviews_idx = -1
    for i, line in enumerate(lines):
        if '<section id="reviews"' in line:
            if "{% if settings.get('show_reviews'" in lines[i-1]:
                reviews_idx = i - 1
            elif "{% if settings.get('show_reviews'" in lines[i-2]:
                reviews_idx = i - 2
            else:
                reviews_idx = i
            break
            
    print(f"Reviews idx: {reviews_idx}")
    if reviews_idx != -1:
        # We append a div id="conciertos" to the news block
        news_block.append('        <div id="conciertos" style="scroll-margin-top: 100px;"></div>\n')
        
        lines = lines[:reviews_idx] + news_block + ["\n"] + lines[reviews_idx:]
        
        with open('templates/index.html', 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print("Moved News and injected Conciertos div!")
    else:
        print("Reviews section not found")
else:
    print("News section not found")
