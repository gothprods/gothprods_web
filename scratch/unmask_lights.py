import re

with open('index.css', 'r') as f:
    content = f.read()

content = re.sub(r'    -webkit-mask-image:.*?\n', '', content)
content = re.sub(r'    mask-image:.*?\n', '', content)

with open('index.css', 'w') as f:
    f.write(content)
