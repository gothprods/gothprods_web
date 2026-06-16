import re

with open("app.py", "r") as f:
    content = f.read()

def insert_after(pattern, insert_str, text):
    return re.sub(f"({pattern})", r"\1\n" + insert_str, text, count=1)

# Dashboard POST
content = insert_after(
    r"section = request\.form\.get\('section'\)",
    r"        if session.get('role') == 'editor' and section not in ['El Noticiero Nocturno', 'Reseñas de Conciertos']:\n            flash('Acceso denegado', 'error')\n            return redirect(url_for('admin_dashboard'))",
    content
)

# Admin Settings
content = insert_after(
    r"def update_settings\(\):\n\s*if 'user_id' not in session:\n\s*return redirect\(url_for\('admin_login'\)\)",
    r"    if session.get('role') not in ['admin', 'root']:\n        return redirect(url_for('admin_dashboard'))",
    content
)

# Admin Banda POST
content = insert_after(
    r"def add_banda\(\):\n\s*if 'user_id' not in session:\n\s*return redirect\(url_for\('admin_login'\)\)",
    r"    if session.get('role') not in ['admin', 'root']:\n        return redirect(url_for('admin_dashboard'))",
    content
)

# Admin Edit Banda
content = insert_after(
    r"def edit_banda\(id\):\n\s*if 'user_id' not in session:\n\s*return redirect\(url_for\('admin_login'\)\)",
    r"    if session.get('role') not in ['admin', 'root']:\n        return redirect(url_for('admin_dashboard'))",
    content
)

# Admin Delete Banda
content = insert_after(
    r"def delete_banda\(id\):\n\s*if 'user_id' not in session:\n\s*return redirect\(url_for\('admin_login'\)\)",
    r"    if session.get('role') not in ['admin', 'root']:\n        return redirect(url_for('admin_dashboard'))",
    content
)

# Admin Sync routes
for sync_route in ['sync_galeria', 'sync_metal_pulse', 'sync_entrevistas', 'sync_agenda']:
    content = insert_after(
        fr"def {sync_route}\(\):\n\s*if 'user_id' not in session:\n\s*return redirect\(url_for\('admin_login'\)\)",
        r"    if session.get('role') not in ['admin', 'root']:\n        return redirect(url_for('admin_dashboard'))",
        content
    )

# Dashboard GET users block
content = insert_after(
    r"todas_bandas = conn\.execute\(\"SELECT \* FROM banda_semana ORDER BY id DESC\"\)\.fetchall\(\)",
    r"    all_users = conn.execute('SELECT id, nombre, username, email, role, is_active FROM users ORDER BY id DESC').fetchall() if session.get('role') in ['admin', 'root'] else []",
    content
)

content = content.replace(
    r"return render_template('admin_dashboard.html', all_items=all_items, settings=get_settings(), todas_bandas=todas_bandas)",
    r"return render_template('admin_dashboard.html', all_items=all_items, settings=get_settings(), todas_bandas=todas_bandas, all_users=all_users)"
)


users_routes = """
@app.route('/admin/users/add', methods=['POST'])
def add_user():
    if session.get('role') not in ['admin', 'root']:
        return redirect(url_for('admin_dashboard'))
    nombre = request.form.get('nombre')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role')
    
    hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
    conn = get_db_connection()
    try:
        conn.execute("INSERT INTO users (nombre, username, email, password, role, is_active) VALUES (?, ?, ?, ?, ?, 1)",
                     (nombre, username, email, hashed_pw, role))
        conn.commit()
        flash('Usuario creado exitosamente.', 'success')
    except Exception as e:
        flash('Error al crear usuario. Verifica que el username o correo no existan ya.', 'error')
    conn.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/users/edit/<int:id>', methods=['POST'])
def edit_user(id):
    if session.get('role') not in ['admin', 'root']:
        return redirect(url_for('admin_dashboard'))
    nombre = request.form.get('nombre')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role')
    
    conn = get_db_connection()
    try:
        if password:
            hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
            conn.execute("UPDATE users SET nombre=?, username=?, email=?, password=?, role=? WHERE id=?", 
                         (nombre, username, email, hashed_pw, role, id))
        else:
            conn.execute("UPDATE users SET nombre=?, username=?, email=?, role=? WHERE id=?", 
                         (nombre, username, email, role, id))
        conn.commit()
        flash('Usuario actualizado exitosamente.', 'success')
    except Exception as e:
        flash('Error al editar usuario.', 'error')
    conn.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/users/toggle/<int:id>', methods=['POST'])
def toggle_user(id):
    if session.get('role') not in ['admin', 'root']:
        return redirect(url_for('admin_dashboard'))
    conn = get_db_connection()
    user = conn.execute("SELECT is_active FROM users WHERE id=?", (id,)).fetchone()
    if user:
        new_status = 0 if user['is_active'] == 1 else 1
        conn.execute("UPDATE users SET is_active=? WHERE id=?", (new_status, id))
        conn.commit()
    conn.close()
    flash('Estado de usuario actualizado.', 'success')
    return redirect(url_for('admin_dashboard'))

"""

content = content.replace("@app.route('/admin/logout')", users_routes + "@app.route('/admin/logout')")

with open("app.py", "w") as f:
    f.write(content)

print("Patch applied")
