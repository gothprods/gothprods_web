import os
import glob

def fix_paths(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix CSS
    content = content.replace('href="index.css', 'href="/index.css')
    
    # Fix JS
    content = content.replace('src="script.js', 'src="/script.js')
    
    # Fix assets
    content = content.replace('href="assets/', 'href="/assets/')
    content = content.replace('src="assets/', 'src="/assets/')
    
    # Check if there are other assets like 'assets/...' in settings.get
    content = content.replace("'assets/", "'/assets/")
    content = content.replace('"assets/', '"/assets/')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for filepath in glob.glob('templates/*.html'):
    fix_paths(filepath)

print("Paths patched successfully.")
