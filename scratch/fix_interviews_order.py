import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern for the interviews block (it's currently below reviews or news)
interviews_pattern = r"{% if settings\.get\('show_interviews', '1'\) == '1' %}\s*<section id=\"under-interviews\".*?</section>\s*{% endif %}"
match_interviews = re.search(interviews_pattern, content, flags=re.DOTALL)

if match_interviews:
    interviews_block = match_interviews.group(0)
    # Remove from current location
    content = content.replace(interviews_block, "")
    
    # We want to insert it directly BEFORE reviews block
    reviews_pattern = r"{% if settings\.get\('show_reviews', '1'\) == '1' %}"
    
    content = content.replace(reviews_pattern, interviews_block + "\n\n        " + reviews_pattern, 1)
    
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Moved interviews BEFORE reviews (i.e. AFTER metal-pulse).")
else:
    print("Interviews block not found.")
