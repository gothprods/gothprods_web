import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = re.compile(
    r'(<div class="agenda-card \{% if item\.author < current_date %\}past-event\{% endif %\})(">.*?<img loading="lazy" decoding="async" src="\{\{ item\.image_filename.*?alt="Logo" class="agenda-logo">\s*)(\{% if item\.author < current_date %\})([\s\S]*?)(</div>\s*\{% endfor %\})',
    re.DOTALL
)

def replacer(match):
    prefix = "{% set is_cancelled = ('cancelado' in item.title|lower) or (item.sp_link and 'cancelado' in item.sp_link|lower) %}\n                    "
    div_start = r'<div class="agenda-card {% if item.author < current_date and not is_cancelled %}past-event{% endif %} {% if is_cancelled %}cancelled-event{% endif %}" {% if is_cancelled %}style="opacity: 0.7; filter: grayscale(80%); position: relative;"{% endif %}'
    
    img_part = match.group(2)
    # We want to insert the CANCELADO badge right before the img
    img_part = img_part.replace('<img loading', '{% if is_cancelled %}\n                        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(-15deg); background: rgba(200,0,0,0.9); color: white; border: 3px solid white; padding: 10px 20px; font-size: 1.5rem; font-weight: 900; letter-spacing: 4px; border-radius: 10px; z-index: 10; text-shadow: 2px 2px 0 #000; box-shadow: 0 0 15px rgba(255,0,0,0.5); text-transform: uppercase; pointer-events: none; width: 85%; text-align: center;">CANCELADO</div>\n                        {% endif %}\n                        <img loading')
    
    finalizado_start = '{% if item.author < current_date and not is_cancelled %}'
    rest = match.group(4)
    end = match.group(5)
    
    return prefix + div_start + img_part + finalizado_start + rest + end

new_content = pattern.sub(replacer, content)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Replaced {len(pattern.findall(content))} occurrences.")
