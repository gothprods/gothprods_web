import re

# 1. Update app.py
with open("app.py", "r") as f:
    app_content = f.read()

delete_route = """@app.route('/admin/evento/delete/<int:id>', methods=['POST'])
def delete_evento(id):
    if 'user_id' not in session: return redirect(url_for('admin_login'))
    conn = get_db_connection()
    conn.execute('DELETE FROM eventos_semana WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Evento eliminado en borrador. Es necesario validar en vista previa antes de liberar.', 'success')
    return redirect(url_for('admin_dashboard'))

"""

if "@app.route('/admin/evento/delete/<int:id>')" not in app_content:
    # Insert right after delete_banda
    app_content = app_content.replace("def delete_banda(id):\n    if 'user_id' not in session: return redirect(url_for('admin_login'))\n    conn = get_db_connection()\n    conn.execute('DELETE FROM banda_semana WHERE id = ?', (id,))\n    conn.commit()\n    conn.close()\n    flash('Banda eliminada en borrador. Es necesario validar en vista previa antes de liberar.', 'success')\n    return redirect(url_for('admin_dashboard'))\n", 
    "def delete_banda(id):\n    if 'user_id' not in session: return redirect(url_for('admin_login'))\n    conn = get_db_connection()\n    conn.execute('DELETE FROM banda_semana WHERE id = ?', (id,))\n    conn.commit()\n    conn.close()\n    flash('Banda eliminada en borrador. Es necesario validar en vista previa antes de liberar.', 'success')\n    return redirect(url_for('admin_dashboard'))\n\n" + delete_route)
    
    with open("app.py", "w") as f:
        f.write(app_content)

# 2. Update admin_dashboard.html
with open("templates/admin_dashboard.html", "r") as f:
    admin_content = f.read()

old_btn = """                                onclick="editEventoRecord(this)">
                                <i class="fa-solid fa-pen"></i> Editar
                            </button>"""

new_btn = """                                onclick="editEventoRecord(this)"
                                style="display: inline-block; padding: 5px 10px; background: #333; color: white; border: none; border-radius: 4px; margin-right: 5px; font-size: 0.8rem; cursor: pointer; text-transform: none; width: auto;">
                                <i class="fa-solid fa-pen"></i> Editar
                            </button>
                            <form method="POST" action="/admin/evento/delete/{{ e.id }}" onsubmit="return confirm('¿Seguro que deseas eliminar este evento?');" style="display: inline-block; margin: 0; padding: 0; box-shadow: none; background: transparent;">
                                <button type="submit" style="padding: 5px 10px; background: #ff3b3b; margin: 0; width: auto; border: none; font-size: 0.8rem; text-transform: none; border-radius: 4px;"><i class="fa-solid fa-trash"></i> Eliminar</button>
                            </form>"""

# Only replace the one in the Eventos table. 
# There's a risk of replacing too much if not careful, but `editEventoRecord(this)` is unique to that button.
if 'action="/admin/evento/delete/{{ e.id }}"' not in admin_content:
    admin_content = admin_content.replace(old_btn, new_btn)
    with open("templates/admin_dashboard.html", "w") as f:
        f.write(admin_content)

print("Delete route and button added.")
