import re
with open("templates/admin_dashboard.html", "r") as f:
    content = f.read()

# We need to swap the positions.
# Current: <div class="textarea-toolbar"...</div>\n<textarea name="..." ...></textarea>
# Problem: we don't know exactly what's inside the textarea, it could be multi-line.
# It's actually safer to just do a simple replacement if we know the exact structure.
