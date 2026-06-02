import re

html_path = 'index.html'
with open(html_path, 'r') as f:
    html = f.read()

# 1. Physically remove tickets buttons
html = re.sub(r'\s*<a href="#" class="tickets-btn">Tickets</a>', '', html)

# 2. Add past-event class to past events
# We will find each <li class="agenda-item"> and its subsequent <div class="agenda-date">...</div>
# If month is ABR or (month is MAY and day is 01), we add 'past-event' to 'agenda-item'

def replace_past_events(match):
    full_text = match.group(0)
    # Check if it contains ABR
    if '<span class="month">ABR</span>' in full_text:
        return full_text.replace('class="agenda-item"', 'class="agenda-item past-event"')
    # Check if it contains MAY 01
    elif '<span class="month">MAY</span><span class="day">01</span>' in full_text:
        return full_text.replace('class="agenda-item"', 'class="agenda-item past-event"')
    return full_text

# Regex to match the entire agenda-item block up to the date
html = re.sub(r'<li class="agenda-item".*?<div class="agenda-date">.*?</div>', replace_past_events, html, flags=re.DOTALL)

with open(html_path, 'w') as f:
    f.write(html)

css_path = 'index.css'
with open(css_path, 'r') as f:
    css = f.read()

if '.past-event' not in css:
    css += """

/* Estilos para eventos pasados */
.past-event {
    opacity: 0.4;
    filter: grayscale(100%);
    pointer-events: none;
}
"""
    with open(css_path, 'w') as f:
        f.write(css)

print("Tickets removed and past events grayed out!")
