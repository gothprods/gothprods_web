with open('templates/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# find interviews
start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if "{% if settings.get('show_interviews', '1') == '1' %}" in line:
        start_idx = i
    if start_idx != -1 and "</section>" in line and "{% endif %}" in lines[i+1]:
        end_idx = i + 1
        break

if start_idx != -1 and end_idx != -1:
    interviews_block = lines[start_idx:end_idx+1]
    
    # remove from original place (deleting backwards or making a new list)
    del lines[start_idx:end_idx+1]
    
    # find reviews
    reviews_idx = -1
    for i, line in enumerate(lines):
        if "{% if settings.get('show_reviews', '1') == '1' %}" in line:
            reviews_idx = i
            break
            
    if reviews_idx != -1:
        # insert
        lines = lines[:reviews_idx] + interviews_block + ["\n"] + lines[reviews_idx:]
        
        with open('templates/index.html', 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print("Surgically moved!")
    else:
        print("Reviews not found.")
else:
    print("Interviews not found.")
