from jinja2 import Template
t = Template("{{ 'hello'.startswith(('h', 'b')) }}")
print(t.render())
