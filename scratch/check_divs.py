with open('templates/admin_dashboard.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

count = 0
for i in range(1503, 1906):
    line = lines[i]
    count += line.count('<div')
    count -= line.count('</div')
    
    if count < 0:
        print(f"Negative div count at line {i+1}: {count}")
