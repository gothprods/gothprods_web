with open('templates/admin_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# We will literally find the dos string blocks and replace them in reverse order
conciertos_block = """<div style="background: #1a1a1a; padding: 15px; border-radius: 8px; border: 1px solid #333; margin-bottom: 15px;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
        <label style="display: flex; align-items: center; gap: 10px; cursor: pointer; font-weight: bold; margin: 0; color: var(--accent-color);">
            Conciertos <span style="font-size: 0.75rem; color: #888;">(Menú)</span>
        </label>
    </div>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
        <div><label style="font-size: 0.8rem; color: #aaa;">Título en el Menú</label><input type="text" name="title_conciertos" value="{{ settings.get('title_conciertos', 'Conciertos') }}" style="background: #222; padding: 8px; border-radius: 4px; border: 1px solid #444; width: 100%; color: #fff;"></div>
        <div><label style="font-size: 0.8rem; color: #aaa;">Ícono (Imagen)</label><input type="file" name="icon_conciertos" accept="image/*" style="background: #222; padding: 6px; border-radius: 4px; border: 1px solid #444; width: 100%; color: #fff; font-size: 0.8rem;"></div>
    </div>
</div>"""

news_block = """<div style="background: #1a1a1a; padding: 15px; border-radius: 8px; border: 1px solid #333; margin-bottom: 15px;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
        <label style="display: flex; align-items: center; gap: 10px; cursor: pointer; font-weight: bold; margin: 0; color: var(--accent-color);">
            <label class="switch" style="margin: 0;">
                <input type="checkbox" name="show_news" value="1" {% if settings.get('show_news', '1') == '1' %}checked{% endif %}>
                <span class="slider"></span>
            </label>
            El Noticiero Nocturno
        </label>
    </div>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
        <div>
            <label style="font-size: 0.8rem; color: #aaa;">Título en el Menú</label>
            <input type="text" name="title_news" value="{{ settings.get('title_news', 'El Noticiero Nocturno') }}" style="background: #222; padding: 8px; border-radius: 4px; border: 1px solid #444; width: 100%; color: #fff;">
        </div>
        <div>
            <label style="font-size: 0.8rem; color: #aaa;">Ícono (Imagen)</label>
            <input type="file" name="icon_news" accept="image/*" style="background: #222; padding: 6px; border-radius: 4px; border: 1px solid #444; width: 100%; color: #fff; font-size: 0.8rem;">
        </div>
    </div>
</div>"""

# They are contiguous in the file: conciertos_block + '\n' + news_block (or with some spaces)
import re

# We remove them both and insert them reversed
pattern = re.compile(re.escape(conciertos_block) + r'\s+' + re.escape(news_block))

if pattern.search(content):
    content = pattern.sub(news_block + '\n' + conciertos_block, content)
    with open('templates/admin_dashboard.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Swapped successfully")
else:
    print("Pattern not found. Checking exactly.")

