with open('templates/admin_dashboard.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

count = 0
start = False
for i, line in enumerate(lines):
    if 'id="tab-lookfeel"' in line:
        start = True
    
    if start:
        count += line.count('<div')
        count -= line.count('</div')
        
        if count == 0:
            print(f"Tab closed at line {i+1}")
            break
        elif count < 0:
            print(f"Negative count at line {i+1}: {count}")
            break
