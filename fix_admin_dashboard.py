import re

with open("templates/admin_dashboard.html", "r") as f:
    content = f.read()

# 1. Add formatText function
js_function = """
function formatText(btn, action, value=null) {
    const targetName = btn.parentElement.getAttribute('data-target');
    const textarea = btn.parentElement.nextElementSibling;
    
    if (!textarea || textarea.tagName.toLowerCase() !== 'textarea') {
        console.error("No textarea found next to toolbar");
        return;
    }
    
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const text = textarea.value;
    const selectedText = text.substring(start, end);
    
    let replacement = "";
    if (action === 'bold') {
        replacement = `<b>${selectedText}</b>`;
    } else if (action === 'color') {
        replacement = `<span style="color: ${value};">${selectedText}</span>`;
    }
    
    textarea.value = text.substring(0, start) + replacement + text.substring(end);
    textarea.focus();
    
    if (!selectedText) {
        let offset = action === 'bold' ? 3 : `<span style="color: ${value};">`.length;
        textarea.selectionStart = start + offset;
        textarea.selectionEnd = start + offset;
    } else {
        textarea.selectionStart = start;
        textarea.selectionEnd = start + replacement.length;
    }
}
"""

if "function formatText(" not in content:
    # Inject it before the last script tag closure or endblock
    content = content.replace("</script>\n{% endblock %}", js_function + "\n</script>\n{% endblock %}")

# 2. Add data-author to the content_items edit buttons
# data-title="{{ item.title }}" -> data-title="{{ item.title }}" data-author="{{ item.author }}"
content = re.sub(r'data-title="{{ item\.title }}"', r'data-title="{{ item.title }}" data-author="{{ item.author }}"', content)

# 3. Update editRecord JS function
# document.querySelector('#main-form input[name="title"]').value = btn.getAttribute('data-title') || '';
# add author below title
author_js = "document.querySelector('#main-form input[name=\"author\"]').value = btn.getAttribute('data-author') || '';"
if "input[name=\"author\"]" not in content:
    content = content.replace(
        "document.querySelector('#main-form input[name=\"title\"]').value = btn.getAttribute('data-title') || '';",
        "document.querySelector('#main-form input[name=\"title\"]').value = btn.getAttribute('data-title') || '';\n    " + author_js
    )

with open("templates/admin_dashboard.html", "w") as f:
    f.write(content)

print("admin_dashboard.html fixed successfully!")
