with open('templates/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1

# Buscamos la línea exacta que abre la SECCIÓN
for i, line in enumerate(lines):
    if '<section id="under-interviews"' in line:
        # The if statement is one line before
        if "{% if settings.get('show_interviews'" in lines[i-1]:
            start_idx = i - 1
        else:
            start_idx = i
        break

if start_idx != -1:
    # Buscar el primer {% endif %} después de la section
    for i in range(start_idx, len(lines)):
        if "{% endif %}" in lines[i] and "</section>" in lines[i-1]:
            end_idx = i
            break

print(f"Start: {start_idx}, End: {end_idx}")

if start_idx != -1 and end_idx != -1:
    interviews_block = lines[start_idx:end_idx+1]
    
    del lines[start_idx:end_idx+1]
    
    # Buscamos la SECCIÓN de reviews
    reviews_idx = -1
    for i, line in enumerate(lines):
        if '<section id="reviews"' in line:
            # The if statement is one line before (or maybe two)
            if "{% if settings.get('show_reviews'" in lines[i-1]:
                reviews_idx = i - 1
            elif "{% if settings.get('show_reviews'" in lines[i-2]:
                reviews_idx = i - 2
            else:
                reviews_idx = i
            break
            
    print(f"Reviews idx: {reviews_idx}")
    if reviews_idx != -1:
        lines = lines[:reviews_idx] + interviews_block + ["\n"] + lines[reviews_idx:]
        
        with open('templates/index.html', 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print("Surgically moved CORRECTLY!")
    else:
        print("Reviews section not found")
else:
    print("Interviews section not found")

