import re
import glob

def patch(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # regex to match: variable_name.startswith('assets')
    # variable_name can have dots, e.g. item.image_filename
    pattern = r'([\w\.]+)\.startswith\(([\'"])assets\2\)'
    
    # replace with: (var.startswith('assets') or var.startswith('/assets'))
    replacement = r'(\1.startswith(\2assets\2) or \1.startswith(\2/assets\2))'
    
    new_content = re.sub(pattern, replacement, content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Patched {filepath}")

for f in glob.glob('templates/*.html'):
    patch(f)
