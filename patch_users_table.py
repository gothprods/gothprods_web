import re

with open("templates/admin_dashboard.html", "r") as f:
    content = f.read()

# 1. Update the table HTML
old_table = """        <div class="table-container">
            <table class="dashboard-table">
                <thead>
                    <tr>
                        <th>Nombre</th>
                        <th>Username</th>
                        <th>Email</th>
                        <th>Perfil</th>
                        <th>Estado</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    {% for user in all_users %}
                    <tr>
                        <td>{{ user.nombre }}</td>
                        <td>{{ user.username }}</td>
                        <td>{{ user.email }}</td>
                        <td><span style="padding: 3px 8px; border-radius: 4px; font-size: 0.8rem; background: {% if user.role == 'admin' %}#aa00ff{% else %}#1DB954{% endif %};">{{ user.role | capitalize }}</span></td>
                        <td>
                            {% if user.is_active == 1 %}
                                <span style="color: #4CAF50;"><i class="fa-solid fa-check-circle"></i> Activo</span>
                            {% else %}
                                <span style="color: #ff3b3b;"><i class="fa-solid fa-ban"></i> Inactivo</span>
                            {% endif %}
                        </td>
                        <td>
                            <button onclick="editUser('{{ user.id }}', '{{ user.nombre }}', '{{ user.username }}', '{{ user.email }}', '{{ user.role }}')" style="padding: 5px 10px; font-size: 0.8rem; margin: 0; width: auto; display: inline-block;">
                                <i class="fa-solid fa-pen"></i> Editar
                            </button>
                            
                            <form action="/admin/users/toggle/{{ user.id }}" method="POST" style="display: inline-block; margin: 0; padding: 0; box-shadow: none; background: transparent;">
                                <button type="submit" style="padding: 5px 10px; margin: 0; width: auto; font-size: 0.8rem; border-radius: 4px; background: {% if user.is_active == 1 %}#ff3b3b{% else %}#4CAF50{% endif %};">
                                    {% if user.is_active == 1 %}
                                        <i class="fa-solid fa-ban"></i> Desactivar
                                    {% else %}
                                        <i class="fa-solid fa-check"></i> Activar
                                    {% endif %}
                                </button>
                            </form>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>"""

new_table = """        <div style="overflow-x: auto;">
            <table style="width: 100%; border-collapse: collapse; font-size: 0.9rem; text-align: left;">
                <thead>
                    <tr style="border-bottom: 1px solid #444;">
                        <th style="padding: 10px; width: 25%;">Nombre Real</th>
                        <th style="padding: 10px; width: 15%;">Username</th>
                        <th style="padding: 10px; width: 25%;">Email</th>
                        <th style="padding: 10px; width: 15%; text-align: center;">Perfil</th>
                        <th style="padding: 10px; width: 10%; text-align: center;">Acceso</th>
                        <th style="padding: 10px; width: 10%; text-align: right;">Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    {% for user in all_users %}
                    <tr style="border-bottom: 1px solid #333;">
                        <td style="padding: 10px; color: #fff;">{{ user.nombre }}</td>
                        <td style="padding: 10px; color: #aaa;">@{{ user.username }}</td>
                        <td style="padding: 10px; color: #888;">{{ user.email }}</td>
                        <td style="padding: 10px; text-align: center;"><span style="padding: 3px 8px; border-radius: 4px; font-size: 0.8rem; background: {% if user.role == 'admin' %}#aa00ff{% else %}#1DB954{% endif %}; color: #fff;">{{ user.role | capitalize }}</span></td>
                        <td style="padding: 10px; text-align: center;">
                            <label class="switch" style="margin-top: 5px;">
                                <input type="checkbox" onchange="toggleUserStatus('{{ user.id }}')" {% if user.is_active == 1 %}checked{% endif %}>
                                <span class="slider"></span>
                            </label>
                        </td>
                        <td style="padding: 10px; text-align: right;">
                            <button onclick="editUser('{{ user.id }}', '{{ user.nombre }}', '{{ user.username }}', '{{ user.email }}', '{{ user.role }}')" style="padding: 5px 10px; font-size: 0.8rem; margin: 0; width: auto; background: #333; color: white; border: none; border-radius: 4px; cursor: pointer; display: inline-block;">
                                <i class="fa-solid fa-pen"></i> Editar
                            </button>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>"""

if old_table in content:
    content = content.replace(old_table, new_table)
else:
    print("Warning: old table not found exactly.")


# 2. Add JS function
js_function = """        function toggleUserStatus(id) {
            fetch('/admin/users/toggle/' + id, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if(!data.success) {
                    alert('Error al actualizar el estado del usuario');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Hubo un error de conexión');
            });
        }
"""

if "function toggleUserStatus" not in content:
    content = content.replace("function cancelUserEdit() {", js_function + "\n        function cancelUserEdit() {")

with open("templates/admin_dashboard.html", "w") as f:
    f.write(content)

print("Patch applied.")
