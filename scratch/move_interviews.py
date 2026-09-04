import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern for the interviews block
interviews_pattern = r"{% if settings\.get\('show_interviews', '1'\) == '1' %}\s*<section id=\"under-interviews\".*?</section>\s*{% endif %}"
match_interviews = re.search(interviews_pattern, content, flags=re.DOTALL)

if match_interviews:
    interviews_block = match_interviews.group(0)
    # Delete from original place
    content = content.replace(interviews_block, "")
    
    # We want to place it directly after metal-pulse finishes.
    # metal-pulse block ends with:
    #         </section>
    #         </section>
    #         {% endif %}
    
    metal_pulse_pattern = r"{% if settings\.get\('show_metalpulse', '1'\) == '1' %}.*?<section id=\"metal-pulse\".*?</section>\s*</section>\s*{% endif %}"
    match_metal_pulse = re.search(metal_pulse_pattern, content, flags=re.DOTALL)
    
    if match_metal_pulse:
        metal_pulse_block = match_metal_pulse.group(0)
        # We append the interviews block after the metal pulse block
        new_combined_block = metal_pulse_block + "\n\n        " + interviews_block
        content = content.replace(metal_pulse_block, new_combined_block)
        
        with open('templates/index.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print("Moved successfully.")
    else:
        print("Metal pulse block not found.")
else:
    print("Interviews block not found.")

