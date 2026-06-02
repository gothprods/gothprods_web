import re
import os
import shutil

html_path = 'index.html'
with open(html_path, 'r') as f:
    html = f.read()

png_mappings = {
    'AC/DC': 'acdc.png',
    'Dream Theater': 'dreamtheater.png',
    'Ill Nino': 'ill_nino.png',
    'Jinjer': 'jinjer.png',
    'Black Label Society': 'blacklabelsociety.png',
    'Architects': 'architects.png',
    'Midnigth': 'midnight.png',
    'Amaranthe': 'amaranthe.png',
    'A.N.I.M.A.L': 'animal.png',
    'Gojira y Knocked Loose': 'gojira.png',
    'Metallica': 'metallica.png',
    'Pantera y Avatar': 'knockedloose.png' # We don't have pantera, let's use knockedloose as placeholder for now, or just leave it
}

jpg_files = [f for f in os.listdir('.') if f.endswith('.jpg')]

def replace_logo(match):
    full_str = match.group(0)
    h3_match = re.search(r'<h3>(.*?)</h3>', full_str)
    if not h3_match:
        h3_match = re.search(r'<h3[^>]*>(.*?)</h3>', full_str)
        if not h3_match:
            return full_str

    band_name = h3_match.group(1).strip()
    
    new_src = None
    if band_name in png_mappings:
        new_src = f"assets/logos/{png_mappings[band_name]}"
    else:
        expected_jpg = f"{band_name}.jpg"
        if os.path.exists(expected_jpg):
            shutil.move(expected_jpg, f"assets/logos/{expected_jpg}")
            new_src = f"assets/logos/{expected_jpg}"
        elif os.path.exists(f"assets/logos/{expected_jpg}"):
            new_src = f"assets/logos/{expected_jpg}"
        else:
            for j in jpg_files:
                if j.startswith(band_name) or band_name in j:
                    if os.path.exists(j):
                        shutil.move(j, f"assets/logos/{j}")
                    new_src = f"assets/logos/{j}"
                    break
            if not new_src:
                for j in os.listdir('assets/logos'):
                    if j.endswith('.jpg') and (j.startswith(band_name) or band_name in j):
                        new_src = f"assets/logos/{j}"
                        break

    if new_src:
        new_str = re.sub(r'src="assets/logos/[^"]+"', f'src="{new_src}"', full_str)
        return new_str
    
    return full_str

new_html = re.sub(r'<li class="agenda-item">.*?</li>', replace_logo, html, flags=re.DOTALL)

with open(html_path, 'w') as f:
    f.write(new_html)

print("HTML updated.")
