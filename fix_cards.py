import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix Reseñas internal structure
# <div class="card-image" style="background-image: url('assets/architects_review.jpg');"></div>
# <div class="card-content"> ... </div>
def fix_review(match):
    img_url = match.group(1)
    content = match.group(2)
    return f'<img src="{img_url}" style="width: 100%; border-radius: 8px; margin-bottom: 10px; height: 140px; object-fit: cover; object-position: center;">\n{content}'

html = re.sub(r'<div class="card-image" style="background-image: url\(\'(.*?)\'\);">\s*</div>\s*<div class="card-content">([\s\S]*?)</div>', fix_review, html)

# Fix Entrevistas internal structure
def fix_interview(match):
    img_url = match.group(1)
    title = match.group(2)
    desc_and_actions = match.group(3)
    
    return f'''<img src="{img_url}" style="width: 100%; border-radius: 8px; margin-bottom: 10px; height: 140px; object-fit: cover; object-position: center;">
<h3 style="font-size: 1rem; line-height: 1.2;">{title}</h3>
{desc_and_actions}'''

html = re.sub(
    r'<div class="interview-left">\s*<div class="card-image"\s*style="background-image: url\(\'(.*?)\'\);">\s*</div>\s*<div class="interview-meta">\s*<span class="badge">.*?</span>\s*<h3>(.*?)</h3>\s*</div>\s*</div>\s*<div class="interview-right">([\s\S]*?)</div>',
    fix_interview,
    html
)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("done")
