with open('templates/admin_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Insert the updateCategoryStats function before filterInteractionsTable
js_code = """
            function updateCategoryStats() {
                const rows = document.querySelectorAll('.interaction-row');
                let stats = {
                    all: { count: 0, int: 0 },
                    noticia: { count: 0, int: 0 },
                    reseña: { count: 0, int: 0 },
                    banda: { count: 0, int: 0 },
                    agenda: { count: 0, int: 0 }
                };
                
                rows.forEach(row => {
                    const sec = row.getAttribute('data-section') || '';
                    const views = parseInt(row.getAttribute('data-views')) || 0;
                    const likes = parseInt(row.getAttribute('data-likes')) || 0;
                    const totalInt = views + likes;
                    
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
                    }
                });
                
                Object.keys(stats).forEach(cat => {
                    const countEl = document.getElementById('cat-count-' + cat);
                    const intEl = document.getElementById('cat-int-' + cat);
                    if(countEl) countEl.innerText = stats[cat].count;
                    if(intEl) intEl.innerText = stats[cat].int;
                });
            }

            document.addEventListener("DOMContentLoaded", updateCategoryStats);

            function filterInteractionsTable() {"""

content = content.replace("            function filterInteractionsTable() {", js_code)

with open('templates/admin_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("JS Inserted.")
