import re

with open('index.css', 'r') as f:
    css = f.read()

# 1. Band names in white and same font size
css = re.sub(r'\.agenda-details h3 \{.*?\n\}', 
             '.agenda-details h3 {\n    display: block !important;\n    color: #ffffff !important;\n    font-size: 1.5rem !important;\n    margin-bottom: 0.5rem;\n    text-align: center;\n}', css, flags=re.DOTALL)

# Hide the logos
css = re.sub(r'\.agenda-logo \{.*?\n\}',
             '.agenda-logo {\n    display: none !important;\n}', css, flags=re.DOTALL)

# Also override the .no-logo case so it doesn't conflict
css = re.sub(r'\.agenda-item\.no-logo \.agenda-details h3 \{.*?\n\}',
             '.agenda-item.no-logo .agenda-details h3 {\n    display: block;\n}', css, flags=re.DOTALL)

# 2. Hide the tickets button
css += "\n\n/* Hide tickets button as requested */\n.tickets-btn {\n    display: none !important;\n}\n"

# 3. Reduce the size of the date boxes
css = re.sub(r'\.agenda-date \.month \{.*?\n\}',
             '.agenda-date .month {\n    color: var(--accent-color);\n    font-size: 0.9rem;\n}', css, flags=re.DOTALL)
css = re.sub(r'\.agenda-date \.day \{.*?\n\}',
             '.agenda-date .day {\n    font-size: 1.5rem;\n    font-weight: 700;\n    line-height: 1;\n}', css, flags=re.DOTALL)

with open('index.css', 'w') as f:
    f.write(css)

print("Agenda styles updated!")
