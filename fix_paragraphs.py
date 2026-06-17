import re

files_to_fix = [
    "templates/index.html",
    "templates/articulo.html",
    "templates/evento.html"
]

def fix_file(filename):
    with open(filename, "r") as f:
        content = f.read()
    
    # Find all <p> tags that contain `safe }}` and have style attributes.
    # We change them to <div> tags to allow internal <div> formatting from the editor.
    # We also change `pre-line` to `pre-wrap` so spaces between paragraphs are preserved.
    
    def replacer(match):
        attributes = match.group(1)
        inner_content = match.group(2)
        
        # Change pre-line to pre-wrap
        attributes = attributes.replace("pre-line", "pre-wrap")
        
        return f"<div{attributes}>{inner_content}</div>"

    # Regex matches <p attributes>{{ ... safe }}</p>
    new_content = re.sub(r'<p([^>]*style="[^"]*"[^>]*)>(.*?\|\s*safe\s*}})</p>', replacer, content)
    
    with open(filename, "w") as f:
        f.write(new_content)

for f in files_to_fix:
    try:
        fix_file(f)
        print(f"Fixed {f}")
    except Exception as e:
        print(f"Skipped {f} - {e}")
