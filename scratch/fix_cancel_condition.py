with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_cond = "{% set is_cancelled = ('cancelado' in item.title|lower) or (item.sp_link and 'cancelado' in item.sp_link|lower) %}"
new_cond = "{% set is_cancelled = ('cancelado' in item.title|lower) or (item.sp_link and 'cancelado' in item.sp_link|lower) or (item.full_desc and 'cancelado' in item.full_desc|lower) %}"

content = content.replace(old_cond, new_cond)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Condition fixed")
