with open('templates/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if "{% if settings.get('show_interviews', '1') == '1' %}" in line:
        start_idx = i
        break

if start_idx != -1:
    for i in range(start_idx, len(lines)):
        if "{% endif %}" in lines[i]:
            # This could be the first endif, let's assume it closes the block since it's just one section
            end_idx = i
            break

print(f"Start: {start_idx}, End: {end_idx}")

if start_idx != -1 and end_idx != -1:
    interviews_block = lines[start_idx:end_idx+1]
    
    del lines[start_idx:end_idx+1]
    
    reviews_idx = -1
    for i, line in enumerate(lines):
        if "{% if settings.get('show_reviews', '1') == '1' %}" in line:
            reviews_idx = i
            break
            
    print(f"Reviews idx: {reviews_idx}")
    if reviews_idx != -1:
        lines = lines[:reviews_idx] + interviews_block + ["\n"] + lines[reviews_idx:]
        
        with open('templates/index.html', 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print("Surgically moved correctly!")
