import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Reseñas
html = re.sub(
    r'<div class="grid-container triple-grid">([\s\S]*?)</div>\s*</section>',
    r'<div class="news-rail">\1</div>\n        </section>',
    html
)
html = html.replace('class="card review-card"', 'class="news-card"')
html = html.replace('class="read-more open-review-modal"', 'class="open-review-modal" style="color: var(--accent-color); font-weight: bold; font-size: 0.85rem;"')

# 2. Entrevistas Under
# We need to change interviews-list to news-rail
html = html.replace('<div class="interviews-list">', '<div class="news-rail">')
html = html.replace('class="interview-card-horizontal"', 'class="news-card"')

# 3. Podcasts (Galeria, Pulse, Caos)
# They use <div class="podcast-layout"> <div class="featured-episode">...</div> <h3>...</h3> <div class="podcast-recent-grid">...</div> </div>
# We want to change it to <div class="news-rail"> ... </div>
def replace_podcast(match):
    content = match.group(1)
    # Remove podcast-layout
    # Convert featured-episode to news-card
    content = content.replace('class="featured-episode"', 'class="news-card"')
    content = content.replace('class="featured-thumb"', 'style="width: 100%; border-radius: 8px; margin-bottom: 10px; height: 140px; object-fit: cover; object-position: center;"')
    content = content.replace('class="featured-info"', 'class="card-content"')
    
    # Convert episode-card to news-card
    content = content.replace('class="episode-card"', 'class="news-card"')
    content = content.replace('class="episode-thumb"', 'style="width: 100%; border-radius: 8px; margin-bottom: 10px; height: 140px; object-fit: cover; object-position: center;"')
    
    # Remove recent-episodes-title
    content = re.sub(r'<h3 class="recent-episodes-title">.*?</h3>', '', content)
    
    # Remove podcast-recent-grid div wrapper
    content = content.replace('<div class="podcast-recent-grid">', '')
    # The closing div for podcast-recent-grid is at the end of the content. We'll strip it manually.
    
    # Convert episode-actions to standard style
    content = content.replace('class="episode-actions"', 'class="episode-actions" style="margin-top: 15px;"')
    
    return f'<div class="news-rail">{content}</div>'

html = re.sub(r'<div class="podcast-layout">([\s\S]*?)</div>\s*</section>', lambda m: replace_podcast(m) + '\n        </section>', html)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("done")
