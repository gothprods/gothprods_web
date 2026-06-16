import re

with open("templates/admin_dashboard.html", "r") as f:
    content = f.read()

# 1. Hide tabs for non-admin
tabs_to_hide = [
    '<button class="tab-btn" onclick="openTab(event, \'tab-sync\')"><i class="fa-solid fa-rotate"></i> Sincronización Automática</button>',
    '<button class="tab-btn" onclick="openTab(event, \'tab-metalpulse\')"><i class="fa-solid fa-headphones"></i> Metal Pulse</button>',
    '<button class="tab-btn" onclick="openTab(event, \'tab-banda\')"><i class="fa-solid fa-star"></i> Banda de la Semana</button>',
    '<button class="tab-btn" onclick="openTab(event, \'tab-caos\')"><i class="fa-solid fa-microphone"></i> Caos Sonoro</button>',
    '<button class="tab-btn" onclick="openTab(event, \'tab-lookfeel\')"><i class="fa-solid fa-paint-roller"></i> Look & Feel</button>'
]

for tab in tabs_to_hide:
    content = content.replace(tab, f"{{% if session.get('role') in ['admin', 'root'] %}}\n        {tab}\n        {{% endif %}}")

# 2. Add Users tab button (only admin)
users_tab_btn = """        {% if session.get('role') in ['admin', 'root'] %}
        <button class="tab-btn" onclick="openTab(event, 'tab-users')"><i class="fa-solid fa-users"></i> Gestión de Usuarios</button>
        {% endif %}"""

content = content.replace(
    '<button class="tab-btn" onclick="openTab(event, \'tab-preview\')"><i class="fa-solid fa-desktop"></i> Vista Previa</button>',
    f'<button class="tab-btn" onclick="openTab(event, \'tab-preview\')"><i class="fa-solid fa-desktop"></i> Vista Previa</button>\n{users_tab_btn}'
)

# 3. Restrict select options for Editor
old_select = """    <select name="section" required>
        <option value="Reseñas de Conciertos">Reseñas de Conciertos</option>
        <option value="El Noticiero Nocturno">El Noticiero Nocturno</option>
        <option value="Metal Pulse Tracks">Metal Pulse Tracks</option>
        <option value="La Galería Nocturna">La Galería Nocturna</option>
        <option value="Caos Sonoro">Caos Sonoro</option>
        <option value="Colaboraciones">Colaboraciones</option>
    </select>"""

new_select = """    <select name="section" required>
        <option value="Reseñas de Conciertos">Reseñas de Conciertos</option>
        <option value="El Noticiero Nocturno">El Noticiero Nocturno</option>
        {% if session.get('role') in ['admin', 'root'] %}
        <option value="Metal Pulse Tracks">Metal Pulse Tracks</option>
        <option value="La Galería Nocturna">La Galería Nocturna</option>
        <option value="Caos Sonoro">Caos Sonoro</option>
        <option value="Colaboraciones">Colaboraciones</option>
        {% endif %}
    </select>"""

content = content.replace(old_select, new_select)


# 4. Add Users Tab Content
users_tab_content = """
    <!-- TAB 8: GESTION DE USUARIOS -->
    {% if session.get('role') in ['admin', 'root'] %}
    <div id="tab-users" class="tab-content">
        <h3 id="form-users-title"><i class="fa-solid fa-user-plus"></i> Añadir Nuevo Usuario</h3>
        <p style="text-align: center; color: var(--text-muted); margin-bottom: 20px; font-size: 0.9rem;">Crea o edita cuentas para tu equipo. Administradores tienen acceso total, Editores solo a Noticias y Reseñas.</p>
        
        <form id="users-form" method="POST" action="/admin/users/add" style="max-width: 600px; margin: 0 auto; background: #111; padding: 25px; border-radius: 8px; border: 1px solid #333;">
            <label>Nombre Real</label>
            <input type="text" name="nombre" id="user_nombre" required>
            
            <label>Nombre de Usuario (Username)</label>
            <input type="text" name="username" id="user_username" required>

            <label>Correo Electrónico (Opcional si usa Username)</label>
            <input type="email" name="email" id="user_email">

            <label>Contraseña <small>(Deja en blanco para no cambiarla al editar)</small></label>
            <input type="password" name="password" id="user_password">

            <label>Perfil (Rol)</label>
            <select name="role" id="user_role" required>
                <option value="admin">Administrador (Acceso Total)</option>
                <option value="editor">Editor (Solo Noticiero/Reseñas)</option>
            </select>

            <div style="display: flex; gap: 10px;">
                <button type="submit" id="submit-user-btn" style="flex: 1;"><i class="fa-solid fa-save"></i> Guardar Usuario</button>
                <button type="button" id="cancel-user-btn" style="display: none; background: #555; width: auto;" onclick="cancelUserEdit()"><i class="fa-solid fa-xmark"></i> Cancelar</button>
            </div>
        </form>

        <h3 style="margin-top: 40px; border-top: 1px solid #333; padding-top: 30px;"><i class="fa-solid fa-users-gear"></i> Lista de Usuarios</h3>
        <div class="table-container">
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
        </div>
    </div>
    {% endif %}
"""

content = content.replace("</div>\n\n    <!-- JavaScript -->", users_tab_content + "\n</div>\n\n    <!-- JavaScript -->")


# 5. Add JS functions
js_code = """
        // User Management scripts
        function editUser(id, nombre, username, email, role) {
            document.getElementById('form-users-title').innerHTML = '<i class="fa-solid fa-user-pen"></i> Editar Usuario';
            var form = document.getElementById('users-form');
            form.action = '/admin/users/edit/' + id;
            document.getElementById('user_nombre').value = nombre;
            document.getElementById('user_username').value = username;
            document.getElementById('user_email').value = email;
            document.getElementById('user_role').value = role;
            
            document.getElementById('submit-user-btn').innerHTML = '<i class="fa-solid fa-save"></i> Actualizar Usuario';
            document.getElementById('cancel-user-btn').style.display = 'inline-block';
            
            form.scrollIntoView({ behavior: 'smooth' });
        }

        function cancelUserEdit() {
            document.getElementById('form-users-title').innerHTML = '<i class="fa-solid fa-user-plus"></i> Añadir Nuevo Usuario';
            var form = document.getElementById('users-form');
            form.action = '/admin/users/add';
            form.reset();
            
            document.getElementById('submit-user-btn').innerHTML = '<i class="fa-solid fa-save"></i> Guardar Usuario';
            document.getElementById('cancel-user-btn').style.display = 'none';
        }
"""

content = content.replace("</script>", js_code + "\n</script>")

with open("templates/admin_dashboard.html", "w") as f:
    f.write(content)

print("HTML Patch applied")
