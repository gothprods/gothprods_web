import re

html_path = 'index.html'

with open(html_path, 'r') as f:
    html = f.read()

# I will use BeautifulSoup or Regex? Regex is fine if I match chunks.
# Let's extract the featured episode block.
featured_pattern = re.compile(r'<div class="featured-episode">(.*?)</div>\s*</div>\s*<h3 class="recent-episodes-title">', re.DOTALL)
featured_match = featured_pattern.search(html)

if featured_match:
    featured_content = featured_match.group(1)
    
    # Create the new Episode 15 for the grid
    # It needs the thumb link, title, and a short description
    # The current featured is Episodio 15
    thumb_15 = re.search(r'<img src="(.*?)"', featured_content).group(1)
    desc_15_full = re.search(r'<p>(.*?)</p>', featured_content, re.DOTALL).group(1)
    desc_15_short = "Colaboración con Mexapedia y Brutal Revista. Perry y JC reciben a Ángel para hablar sobre el Metal Chingón."
    
    ep_15_card = f"""
                    <div class="episode-card">
                        <img src="{thumb_15}"
                            alt="Caos Sonoro Episodio 15" class="episode-thumb">
                        <h3>Caos Sonoro | Episodio 15</h3>
                        <p>{desc_15_short}</p>
                        <div class="episode-actions">
                            <a href="https://open.spotify.com/show/2hnlgkcGNl9GOAPa0WT9HW?si=7e9b95f203464fe6"
                                target="_blank" class="platform-btn spotify-btn"><i class="fa-brands fa-spotify"></i>
                                Spotify</a>
                            <a href="https://www.youtube.com/watch?v=Tvr20W_ON74" target="_blank"
                                class="platform-btn"><i class="fa-brands fa-youtube"></i> YouTube</a>
                        </div>
                    </div>"""
    
    # New Featured Episode 16
    new_featured = featured_content.replace('Episodio 15 | Abril 2, 2026', 'Episodio 16 | Abril 29, 2026')
    new_featured = new_featured.replace('Episodio 15', 'Episodio 16')
    new_desc = "Nuevo episodio analizando las controversias y cancelaciones recientes: Korn es funado, las sedes del Knotfest 2026 y la situación con Black Label Society."
    new_featured = re.sub(r'<p>.*?</p>', f'<p>{new_desc}</p>', new_featured, count=1, flags=re.DOTALL)
    # I don't have the new video ID, I will use a generic or keep the old one, but wait, the thumbnail can be Caos_Sonoro.jpg for now
    new_featured = re.sub(r'<img src=".*?"', '<img src="assets/Caos_Sonoro.jpg"', new_featured, count=1)
    
    # Replace the featured
    html = html.replace(featured_content, new_featured)
    
    # Now shift the grid
    # We find the podcast-recent-grid
    grid_pattern = re.compile(r'<div class="podcast-recent-grid">\s*(.*?)\s*</div>\s*</section>', re.DOTALL)
    grid_match = grid_pattern.search(html)
    
    if grid_match:
        grid_content = grid_match.group(1)
        # grid_content has 3 episode-cards. Let's split by '<div class="episode-card">'
        cards = grid_content.split('<div class="episode-card">')
        # cards[0] is empty space
        # cards[1] is ep 14
        # cards[2] is ep 13
        # cards[3] is ep 12
        
        # New grid content: ep_15 + ep_14 + ep_13
        new_grid_content = ep_15_card + '\n                    <div class="episode-card">' + cards[1] + '<div class="episode-card">' + cards[2]
        
        html = html.replace(grid_content, new_grid_content)
        
with open(html_path, 'w') as f:
    f.write(html)

print("Episodes updated!")
