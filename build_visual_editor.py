import re

with open("templates/admin_dashboard.html", "r") as f:
    content = f.read()

# The old toolbar pattern
old_toolbar_pattern = r'<div class="textarea-toolbar" data-target="([^"]+)"[^>]*>.*?</div>\n<textarea name="\1"([^>]*)>(.*?)</textarea>'

visual_editor_template = """
<div class="visual-editor-container" data-target="\\1">
    <div class="textarea-toolbar" style="display: flex; gap: 10px; margin-bottom: 5px; background: #222; padding: 5px; border-radius: 4px; border: 1px solid #444;">
        <button type="button" onmousedown="formatVisual(event, 'bold')" style="background: #333; color: #fff; border: 1px solid #555; padding: 4px 8px; border-radius: 4px; cursor: pointer;" title="Negrita"><i class="fa-solid fa-bold"></i></button>
        <button type="button" onmousedown="formatVisual(event, 'foreColor', '#ffffff')" style="background: #333; color: #fff; border: 1px solid #555; padding: 4px 8px; border-radius: 4px; cursor: pointer;" title="Texto Blanco"><i class="fa-solid fa-droplet"></i> Blanco</button>
        <button type="button" onmousedown="formatVisual(event, 'foreColor', '#716d4a')" style="background: #333; color: var(--accent-color); border: 1px solid #555; padding: 4px 8px; border-radius: 4px; cursor: pointer;" title="Texto Dorado"><i class="fa-solid fa-droplet"></i> Dorado</button>
    </div>
    <div class="rich-editor" contenteditable="true" style="min-height: 120px; background: #111; color: #fff; border: 1px solid #333; border-radius: 4px; padding: 10px; outline: none; overflow-y: auto; white-space: pre-wrap;" oninput="syncEditor(this)">\\3</div>
    <textarea name="\\1"\\2 style="display: none;">\\3</textarea>
</div>
"""

# Apply the replacement
content = re.sub(old_toolbar_pattern, visual_editor_template.strip(), content, flags=re.DOTALL)

# Delete the old formatText function to avoid clutter
old_format_text_pattern = r'function formatText\([^)]*\)\s*\{[^\}]*\}[^\}]*\}'
content = re.sub(old_format_text_pattern, '', content, flags=re.DOTALL)

new_js = """
function formatVisual(event, action, value=null) {
    event.preventDefault(); // Keep focus on editor by preventing default click behavior
    const btn = event.currentTarget;
    const container = btn.closest('.visual-editor-container');
    const editor = container.querySelector('.rich-editor');
    
    // Focus the editor if it isn't already focused
    if (document.activeElement !== editor) {
        editor.focus();
    }
    
    if (action === 'bold') {
        document.execCommand('bold', false, null);
    } else if (action === 'foreColor') {
        // Modern approach allows inline styles instead of <font> tags
        document.execCommand('styleWithCSS', false, true);
        document.execCommand('foreColor', false, value);
    }
    
    syncEditor(editor);
}

function syncEditor(editorDiv) {
    const container = editorDiv.closest('.visual-editor-container');
    const textarea = container.querySelector('textarea');
    textarea.value = editorDiv.innerHTML;
}

function syncAllVisualsToEditors() {
    // Also use setTimeout to ensure browser has updated textarea.value before we sync
    setTimeout(() => {
        document.querySelectorAll('.visual-editor-container').forEach(container => {
            const textarea = container.querySelector('textarea');
            const editor = container.querySelector('.rich-editor');
            if(textarea && editor) {
                editor.innerHTML = textarea.value;
            }
        });
    }, 100);
}
"""

if "function formatVisual" not in content:
    content = content.replace("</script>\n{% endblock %}", new_js + "\n</script>\n{% endblock %}")

# Add syncAllVisualsToEditors() to the end of form-resetting and editing functions
content = content.replace(
    "    window.scrollTo({ top: 0, behavior: 'smooth' });\n}",
    "    window.scrollTo({ top: 0, behavior: 'smooth' });\n    syncAllVisualsToEditors();\n}"
)
content = content.replace(
    "    document.querySelector('input[name=\"image\"]').required = true;\n}",
    "    document.querySelector('input[name=\"image\"]').required = true;\n    syncAllVisualsToEditors();\n}"
)
content = content.replace(
    "    document.getElementById('banda-form').scrollIntoView({ behavior: 'smooth' });\n}",
    "    document.getElementById('banda-form').scrollIntoView({ behavior: 'smooth' });\n    syncAllVisualsToEditors();\n}"
)
content = content.replace(
    "    document.getElementById('banda-cancel-btn').style.display = 'none';\n}",
    "    document.getElementById('banda-cancel-btn').style.display = 'none';\n    syncAllVisualsToEditors();\n}"
)

# Call syncAllVisualsToEditors on DOMContentLoaded so initial values render correctly
if "syncAllVisualsToEditors();\n});" not in content:
    content = content.replace("});\n</script>", "    syncAllVisualsToEditors();\n});\n</script>")


with open("templates/admin_dashboard.html", "w") as f:
    f.write(content)

print("Visual WYSIWYG Editor built successfully!")
