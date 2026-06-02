import re
import urllib.parse

# 1. Modify index.css
with open('index.css', 'r') as f:
    css = f.read()

# Replace agenda-list and everything up to footer
start_idx = css.find('.agenda-list {')
end_idx = css.find('/* Footer */')

new_css = """
.agenda-list {
    display: flex;
    overflow-x: auto;
    gap: 1.5rem;
    padding-bottom: 1.5rem;
    list-style: none;
    scroll-snap-type: x mandatory;
}

/* Custom Scrollbar for Agenda List */
.agenda-list::-webkit-scrollbar {
    height: 8px;
}
.agenda-list::-webkit-scrollbar-track {
    background: var(--bg-secondary);
    border-radius: 4px;
}
.agenda-list::-webkit-scrollbar-thumb {
    background: var(--accent-color);
    border-radius: 4px;
}

.agenda-item {
    flex: 0 0 300px;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    background-color: var(--bg-secondary);
    padding: 1.5rem;
    border-top: 4px solid var(--accent-color);
    border-radius: 8px;
    transition: transform 0.3s ease, background-color 0.3s ease;
    scroll-snap-align: start;
}

.agenda-item:hover {
    background-color: #222;
    transform: translateY(-5px);
}

.agenda-logo {
    width: 100%;
    height: 100px;
    object-fit: contain;
    margin-bottom: 1rem;
    border-radius: 4px;
}

.agenda-date {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 1rem;
    font-family: var(--font-heading);
}

.agenda-date .month {
    color: var(--accent-color);
    font-size: 1.2rem;
}

.agenda-date .day {
    font-size: 2rem;
    font-weight: 700;
    line-height: 1;
}

.agenda-details {
    flex-grow: 1;
    margin-bottom: 1.5rem;
}

.agenda-details h3 {
    display: none; /* Hide H3 since we use logos now */
}

.agenda-details p {
    color: var(--text-muted);
    font-size: 1.1rem;
}

"""

css = css[:start_idx] + new_css + css[end_idx:]

# Remove media query rules for agenda
media_query_remove = """    .agenda-item {
        flex-direction: column;
        align-items: flex-start;
    }
    .agenda-date {
        border-right: none;
        border-bottom: 1px solid var(--border-color);
        padding-right: 0;
        margin-right: 0;
        padding-bottom: 1rem;
        margin-bottom: 1rem;
    }"""

css = css.replace(media_query_remove, "")

with open('index.css', 'w') as f:
    f.write(css)

# 2. Modify index.html
with open('index.html', 'r') as f:
    html = f.read()

def inject_logo(match):
    full_match = match.group(0)
    # Check if it has an h3
    h3_match = re.search(r'<h3>(.*?)</h3>', full_match)
    if not h3_match:
        return full_match
    
    band_name = h3_match.group(1).strip()
    encoded_name = urllib.parse.quote(band_name)
    # Create the logo tag with fallback
    file_name = band_name.replace(' ', '_').replace('/', '').lower() + '.png'
    img_tag = f'<img src="assets/logos/{file_name}" onerror="this.onerror=null; this.src=\'https://placehold.co/300x100/111111/A59B5D?text={encoded_name}\'" alt="{band_name} Logo" class="agenda-logo">'
    
    # insert img_tag right after <li class="agenda-item">
    new_str = re.sub(r'(<li class="agenda-item">)', r'\1\n                        ' + img_tag, full_match)
    return new_str

html = re.sub(r'<li class="agenda-item">.*?</li>', inject_logo, html, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(html)
