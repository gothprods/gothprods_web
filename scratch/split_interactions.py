with open('templates/admin_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace button HTML
html_replacements = [
    ('Todos (<span id="cat-count-all">0</span>) | <i class="fa-solid fa-bolt"></i> <span id="cat-int-all">0</span>',
     'Todos (<span id="cat-count-all">0</span>) &nbsp;|&nbsp; <i class="fa-solid fa-eye" style="color:#00d2ff;"></i> <span id="cat-views-all">0</span> &nbsp;|&nbsp; <i class="fa-solid fa-heart" style="color:#ff4757;"></i> <span id="cat-likes-all">0</span>'),
    ('📰 Noticias (<span id="cat-count-noticia">0</span>) | <i class="fa-solid fa-bolt"></i> <span id="cat-int-noticia">0</span>',
     '📰 Noticias (<span id="cat-count-noticia">0</span>) &nbsp;|&nbsp; <i class="fa-solid fa-eye" style="color:#00d2ff;"></i> <span id="cat-views-noticia">0</span> &nbsp;|&nbsp; <i class="fa-solid fa-heart" style="color:#ff4757;"></i> <span id="cat-likes-noticia">0</span>'),
    ('🎸 Reseñas (<span id="cat-count-reseña">0</span>) | <i class="fa-solid fa-bolt"></i> <span id="cat-int-reseña">0</span>',
     '🎸 Reseñas (<span id="cat-count-reseña">0</span>) &nbsp;|&nbsp; <i class="fa-solid fa-eye" style="color:#00d2ff;"></i> <span id="cat-views-reseña">0</span> &nbsp;|&nbsp; <i class="fa-solid fa-heart" style="color:#ff4757;"></i> <span id="cat-likes-reseña">0</span>'),
    ('💀 Bandas (<span id="cat-count-banda">0</span>) | <i class="fa-solid fa-bolt"></i> <span id="cat-int-banda">0</span>',
     '💀 Bandas (<span id="cat-count-banda">0</span>) &nbsp;|&nbsp; <i class="fa-solid fa-eye" style="color:#00d2ff;"></i> <span id="cat-views-banda">0</span> &nbsp;|&nbsp; <i class="fa-solid fa-heart" style="color:#ff4757;"></i> <span id="cat-likes-banda">0</span>'),
    ('📅 Agenda (<span id="cat-count-agenda">0</span>) | <i class="fa-solid fa-bolt"></i> <span id="cat-int-agenda">0</span>',
     '📅 Agenda (<span id="cat-count-agenda">0</span>) &nbsp;|&nbsp; <i class="fa-solid fa-eye" style="color:#00d2ff;"></i> <span id="cat-views-agenda">0</span> &nbsp;|&nbsp; <i class="fa-solid fa-heart" style="color:#ff4757;"></i> <span id="cat-likes-agenda">0</span>')
]

for old, new in html_replacements:
    content = content.replace(old, new)

# Replace JS logic
old_js = """                let stats = {
                    all: { count: 0, int: 0 },
                    noticia: { count: 0, int: 0 },
                    reseña: { count: 0, int: 0 },
                    banda: { count: 0, int: 0 },
                    agenda: { count: 0, int: 0 }
                };"""

new_js = """                let stats = {
                    all: { count: 0, views: 0, likes: 0 },
                    noticia: { count: 0, views: 0, likes: 0 },
                    reseña: { count: 0, views: 0, likes: 0 },
                    banda: { count: 0, views: 0, likes: 0 },
                    agenda: { count: 0, views: 0, likes: 0 }
                };"""
content = content.replace(old_js, new_js)

old_js2 = """                    const totalInt = views + likes;
                    
                    stats.all.count++;
                    stats.all.int += totalInt;
                    
                    if(sec.includes('notici')) {
                        stats.noticia.count++;
                        stats.noticia.int += totalInt;
                    } else if(sec.includes('reseña')) {
                        stats.reseña.count++;
                        stats.reseña.int += totalInt;
                    } else if(sec.includes('banda')) {
                        stats.banda.count++;
                        stats.banda.int += totalInt;
                    } else if(sec.includes('agenda')) {
                        stats.agenda.count++;
                        stats.agenda.int += totalInt;
                    }"""

new_js2 = """                    stats.all.count++;
                    stats.all.views += views;
                    stats.all.likes += likes;
                    
                    if(sec.includes('notici')) {
                        stats.noticia.count++;
                        stats.noticia.views += views;
                        stats.noticia.likes += likes;
                    } else if(sec.includes('reseña')) {
                        stats.reseña.count++;
                        stats.reseña.views += views;
                        stats.reseña.likes += likes;
                    } else if(sec.includes('banda')) {
                        stats.banda.count++;
                        stats.banda.views += views;
                        stats.banda.likes += likes;
                    } else if(sec.includes('agenda')) {
                        stats.agenda.count++;
                        stats.agenda.views += views;
                        stats.agenda.likes += likes;
                    }"""
content = content.replace(old_js2, new_js2)

old_js3 = """                Object.keys(stats).forEach(cat => {
                    const countEl = document.getElementById('cat-count-' + cat);
                    const intEl = document.getElementById('cat-int-' + cat);
                    if(countEl) countEl.innerText = stats[cat].count;
                    if(intEl) intEl.innerText = stats[cat].int;
                });"""

new_js3 = """                Object.keys(stats).forEach(cat => {
                    const countEl = document.getElementById('cat-count-' + cat);
                    const viewsEl = document.getElementById('cat-views-' + cat);
                    const likesEl = document.getElementById('cat-likes-' + cat);
                    if(countEl) countEl.innerText = stats[cat].count;
                    if(viewsEl) viewsEl.innerText = stats[cat].views;
                    if(likesEl) likesEl.innerText = stats[cat].likes;
                });"""
content = content.replace(old_js3, new_js3)

with open('templates/admin_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("JS and HTML Split Replaced.")
