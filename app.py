from flask import Flask, send_from_directory, request, session, redirect, url_for, render_template, flash, jsonify
import sqlite3
import os
import random
import string
import smtplib
from datetime import timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import uuid
from PIL import Image

load_dotenv('config.env')

app = Flask(__name__, static_folder='.', static_url_path='/static')
app.secret_key = os.getenv('SECRET_KEY', 'super_secret_goth_key')
app.config['UPLOAD_FOLDER'] = 'updates'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 2592000
app.permanent_session_lifetime = timedelta(minutes=30)

def optimize_and_save_image(file_obj, save_dir, prefix=""):
    """
    Saves an uploaded image file, converting it to WebP format and resizing it if it's too large.
    Returns the final filename relative to the base directory (or just the filename if stored in updates).
    """
    # Generate a unique secure filename with .webp extension
    original_filename = secure_filename(file_obj.filename)
    base_name = os.path.splitext(original_filename)[0]
    final_filename = f"{prefix}{uuid.uuid4().hex[:8]}_{base_name}.webp"
    final_path = os.path.join(save_dir, final_filename)
    
    try:
        img = Image.open(file_obj)
        # WebP supports RGBA natively. Only convert P to RGBA or RGB depending on transparency.
        if img.mode == "P":
            if 'transparency' in img.info:
                img = img.convert("RGBA")
            else:
                img = img.convert("RGB")
            
        # Resize if width is larger than 1200px
        max_width = 1200
        if img.width > max_width:
            ratio = max_width / float(img.width)
            new_height = int((float(img.height) * float(ratio)))
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
            
        img.save(final_path, "WEBP", quality=80, optimize=True)
        return final_filename
    except Exception as e:
        print(f"Error optimizing image: {e}")
        # Fallback to normal save if not a valid image
        fallback_name = secure_filename(file_obj.filename)
        fallback_path = os.path.join(save_dir, fallback_name)
        file_obj.seek(0)
        file_obj.save(fallback_path)
        return fallback_name

DB_FILE = 'gothprods.db'
DB_LIVE_FILE = 'gothprods_live.db'

def get_db_connection(live=False):
    db_path = DB_LIVE_FILE if live else DB_FILE
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    
    # Auto-migrate schema for banda_semana
    try:
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(banda_semana)")
        columns = [col[1] for col in cursor.fetchall()]
        
        required_columns = [
            'ano_formacion', 'line_up', 'titulo_resena', 'texto_resena', 
            'discografia', 'ultimo_lanzamiento_titulo', 'ultimo_lanzamiento_tipo', 
            'ultimo_lanzamiento_url', 'ultimo_lanzamiento_plataforma', 
            'ultimo_lanzamiento_sp_link', 'ultimo_lanzamiento_ap_link',
            'bio_larga', 'is_active', 'fecha_inicio', 'fecha_fin'
        ]
        
        for col in required_columns:
            if col not in columns:
                if col == 'is_active':
                    cursor.execute(f"ALTER TABLE banda_semana ADD COLUMN {col} INTEGER DEFAULT 1")
                else:
                    cursor.execute(f"ALTER TABLE banda_semana ADD COLUMN {col} TEXT")
        conn.commit()
    except Exception as e:
        print("Schema migration error:", e)

    # Auto-migrate schema for users
    try:
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'nombre' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN nombre TEXT")
        if 'username' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN username TEXT")
        if 'is_active' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN is_active INTEGER DEFAULT 1")
            
        # Migrate existing root user
        cursor.execute("UPDATE users SET username = 'root', nombre = 'Administrador', role = 'admin', is_active = 1 WHERE email = 'goth.prods@gmail.com' AND username IS NULL")
        
        conn.commit()
    except Exception as e:
        print("Schema migration error (users):", e)

    return conn

def get_settings(live=False):
    conn = get_db_connection(live)
    try:
        rows = conn.execute("SELECT key, value FROM settings").fetchall()
        settings = {row['key']: row['value'] for row in rows}
    except sqlite3.OperationalError:
        # En caso de que la tabla aún no exista
        settings = {}
    conn.close()
    return settings


# --- EMAIL CONFIGURATION ---
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "goth.prods@gmail.com"
SENDER_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "")

def send_verification_email(to_email, code, subject="Código de Verificación - Goth Prods"):
    if not SENDER_PASSWORD:
        print(f"[WARNING] No GMAIL_APP_PASSWORD. Simulation: Code for {to_email} is {code}")
        return True
    try:
        msg = MIMEText(f"Tu código para Goth Prods es: {code}")
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = to_email

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

# --- FRONTEND ---
@app.route('/')
def index():
    is_preview = request.args.get('preview') == '1' and 'user_id' in session
    conn = get_db_connection(live=not is_preview)
    import datetime
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    # Query for the latest Banda de la Semana
    raw_bandas = conn.execute("SELECT * FROM banda_semana ORDER BY id DESC").fetchall()
    bandas_semana = []
    seen_bands = set()
    for b in raw_bandas:
        # Check if the band is active (default 1 if column just added, but could be 0)
        is_active = b['is_active'] if 'is_active' in b.keys() else 1
        
        # Check dates
        fecha_inicio = b['fecha_inicio'] if 'fecha_inicio' in b.keys() and b['fecha_inicio'] else None
        fecha_fin = b['fecha_fin'] if 'fecha_fin' in b.keys() and b['fecha_fin'] else None
        
        in_date_range = True
        if fecha_inicio and current_date < fecha_inicio:
            in_date_range = False
        if fecha_fin and current_date > fecha_fin:
            in_date_range = False
            
        if is_active == 1 and in_date_range and b['nombre'] not in seen_bands:
            seen_bands.add(b['nombre'])
            bandas_semana.append(b)
            if len(bandas_semana) == 5:
                break
    
    # Existing content queries
    noticiero_items = conn.execute("SELECT * FROM content_items WHERE section = 'El Noticiero Nocturno' ORDER BY created_at DESC").fetchall()
    reseñas_items = conn.execute("SELECT * FROM content_items WHERE section = 'Reseñas de Conciertos' ORDER BY created_at DESC, id DESC").fetchall()
    entrevistas_items = conn.execute("SELECT * FROM content_items WHERE section = 'Entrevistas Under' ORDER BY created_at DESC, id DESC").fetchall()
    agenda_items = conn.execute("SELECT * FROM content_items WHERE section = 'Agenda Metalera' ORDER BY author ASC").fetchall()
    galeria_items = conn.execute("SELECT * FROM content_items WHERE section IN ('La Galería Nocturna', 'Caos Sonoro', 'Colaboraciones') ORDER BY created_at DESC, id DESC").fetchall()
    metalpulse_items = conn.execute("SELECT * FROM content_items WHERE section = 'Metal Pulse' ORDER BY created_at DESC, id DESC").fetchall()
    caossonoro_items = conn.execute("SELECT * FROM content_items WHERE section = 'Caos Sonoro' ORDER BY created_at DESC, id DESC").fetchall()
    metalpulse_tracks = conn.execute("SELECT * FROM content_items WHERE section = 'Metal Pulse Tracks' ORDER BY id DESC").fetchall()
    conn.close()
    
    # Group agenda items by month
    from collections import OrderedDict
    import datetime
    
    # Define spanish months manually to map from date string
    spanish_months = {
        '01': 'Enero', '02': 'Febrero', '03': 'Marzo', '04': 'Abril',
        '05': 'Mayo', '06': 'Junio', '07': 'Julio', '08': 'Agosto',
        '09': 'Septiembre', '10': 'Octubre', '11': 'Noviembre', '12': 'Diciembre'
    }
    
    agenda_grouped = OrderedDict()
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    for item in agenda_items:
        # author has 'YYYY-MM-DD'
        month_num = item['author'].split('-')[1] if item['author'] else '05'
        month_name = spanish_months.get(month_num, 'Mayo')
        if month_name not in agenda_grouped:
            agenda_grouped[month_name] = []
        agenda_grouped[month_name].append(item)

    upcoming_agenda = [item for item in agenda_items if item['author'] >= current_date]

    return render_template('index.html', 
                           noticiero_items=noticiero_items,
                           reseñas_items=reseñas_items,
                           entrevistas_items=entrevistas_items,
                           galeria_items=galeria_items,
                           metalpulse_items=metalpulse_items,
                           metalpulse_tracks=metalpulse_tracks,
                           caossonoro_items=caossonoro_items,
                           agenda_grouped=agenda_grouped,
                           agenda_items=agenda_items,
                           upcoming_agenda=upcoming_agenda,
                           current_date=current_date,
                           settings=get_settings(live=not is_preview),
                           bandas_semana=bandas_semana)

@app.route('/banda/<int:id>')
def view_banda(id):
    is_preview = request.args.get('preview') == '1'
    conn = get_db_connection(live=not is_preview)
    banda = conn.execute("SELECT * FROM banda_semana WHERE id = ?", (id,)).fetchone()
    conn.close()
    
    if not banda:
        return "Banda no encontrada", 404
        
    settings = get_settings(live=not is_preview)
    return render_template('banda.html', banda=banda, settings=settings)

@app.route('/articulo/<int:id>')
def view_articulo(id):
    is_preview = request.args.get('preview') == '1'
    conn = get_db_connection(live=not is_preview)
    item = conn.execute("SELECT * FROM content_items WHERE id = ?", (id,)).fetchone()
    conn.close()
    
    if not item:
        return "Artículo no encontrado", 404
        
    settings = get_settings(live=not is_preview)
    return render_template('articulo.html', item=item, settings=settings)

@app.route('/<path:path>')
def serve_static(path):
    if os.path.exists(path):
        return send_from_directory('.', path)
    return "Not found", 404

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    name = request.form.get('name', 'N/A')
    email = request.form.get('email', 'N/A')
    message = request.form.get('message', 'N/A')
    files = request.files.getlist('attachments')
    
    # Construir el mensaje de correo
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = "contacto@gothprods.com"
    msg['Subject'] = f"Nuevo Material/Contacto de Berserkers: {name}"
    
    body = f"Nombre / Banda: {name}\n"
    body += f"Correo de Contacto: {email}\n"
    body += f"Mensaje:\n{message}\n"
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Procesar archivos adjuntos
    if files:
        for f in files:
            if f and f.filename:
                # Leer el archivo en memoria (sin guardarlo en disco)
                file_data = f.read()
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(file_data)
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename="{f.filename}"'
                )
                msg.attach(part)
                
    try:
        # Enviar correo
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        if SENDER_PASSWORD:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        # Si se envió correctamente, puedes devolver a la página con un mensaje
        # Si se necesita un popup o flash, se puede usar flash()
        return """
        <script>
            alert("¡Mensaje y material enviados exitosamente a contacto@gothprods.com!");
            window.location.href = "/#contact";
        </script>
        """
    except Exception as e:
        print(f"Error al enviar contacto: {e}")
        return """
        <script>
            alert("Hubo un error al enviar el correo. Por favor, inténtalo más tarde.");
            window.location.href = "/#contact";
        </script>
        """

# --- ADMIN ROUTES ---
@app.route('/admin')
def admin_redirect():
    if 'user_id' in session:
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('admin_login'))

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE email = ? OR username = ?", (email, email)).fetchone()
        
        if user:
            if 'is_active' in user.keys() and user['is_active'] == 0:
                flash('Tu cuenta ha sido desactivada.', 'error')
            elif user['password'] and check_password_hash(user['password'], password):
                if user.keys().count('must_change_password') > 0 and user['must_change_password'] == 1:
                    session['setup_email'] = user['email']
                    return redirect(url_for('setup_root_password'))
                
                session.permanent = True
                session['user_id'] = user['id']
                session['role'] = user['role']
                session['email'] = user['email']
                session['username'] = user['username'] if 'username' in user.keys() else ''
                session['nombre'] = user['nombre'] if 'nombre' in user.keys() else ''
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Credenciales incorrectas.', 'error')
        else:
            flash('Usuario no encontrado.', 'error')
        conn.close()

    return render_template('admin_login.html')

@app.route('/admin/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if user:
            code = ''.join(random.choices(string.digits, k=6))
            conn.execute("UPDATE users SET verification_code = ? WHERE id = ?", (code, user['id']))
            conn.commit()
            send_verification_email(user['email'], code, subject="Recuperación de Contraseña - Goth Prods")
            session['reset_email'] = email
            return redirect(url_for('reset_password'))
        else:
            flash('Si el correo existe, se ha enviado un código de recuperación.', 'success')
        conn.close()

    return render_template('admin_forgot.html')

@app.route('/admin/reset_password', methods=['GET', 'POST'])
def reset_password():
    if 'reset_email' not in session:
        return redirect(url_for('admin_login'))
        
    if request.method == 'POST':
        code = request.form['code']
        new_password = request.form['new_password']
        email = session['reset_email']
        
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if user and user['verification_code'] == code:
            hashed_pw = generate_password_hash(new_password, method='pbkdf2:sha256')
            conn.execute("UPDATE users SET password = ?, verification_code = NULL WHERE id = ?", (hashed_pw, user['id']))
            conn.commit()
            session.pop('reset_email', None)
            flash('¡Contraseña actualizada con éxito! Ya puedes iniciar sesión.', 'success')
            return redirect(url_for('admin_login'))
        else:
            flash('El código es incorrecto.', 'error')
        conn.close()

    return render_template('admin_reset.html')

@app.route('/admin/setup', methods=['GET', 'POST'])
def setup_root_password():
    if 'setup_email' not in session:
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        password = request.form['password']
        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
        conn = get_db_connection()
        conn.execute("UPDATE users SET password = ?, must_change_password = 0 WHERE email = ?", (hashed_pw, session['setup_email']))
        conn.commit()
        conn.close()
        flash('Contraseña maestra configurada. Por favor, inicia sesión.', 'success')
        session.pop('setup_email', None)
        return redirect(url_for('admin_login'))
        
    return render_template('admin_setup.html')

@app.route('/admin/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        section = request.form.get('section')
        if session.get('role') == 'editor' and section not in ['El Noticiero Nocturno', 'Reseñas de Conciertos']:
            flash('Acceso denegado', 'error')
            return redirect(url_for('admin_dashboard'))
        title = request.form.get('title')
        short_desc = request.form.get('short_desc')
        full_desc = request.form.get('full_desc')
        yt_link = request.form.get('yt_link', '')
        sp_link = request.form.get('sp_link', '')
        ap_link = request.form.get('ap_link', '')
        author = request.form.get('author')
        image = request.files.get('image')
        pub_date = request.form.get('pub_date')

        safe_title = "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ']).rstrip().replace(" ", "_")
        
        image_filename = ""
        if image and image.filename:
            image_filename = optimize_and_save_image(image, app.config['UPLOAD_FOLDER'], prefix="content_")
            
        copy_text = f"🔥 ¡NUEVO CONTENIDO EN GOTH PRODS! 🔥\n\n"
        copy_text += f"SECCIÓN: {section}\n"
        copy_text += f"TÍTULO: {title}\n\n"
        copy_text += f"{short_desc}\n\n"
        copy_text += f"💬 Conoce más detalles:\n{full_desc}\n\n"
        
        if yt_link or sp_link or ap_link:
            copy_text += f"🎧 ESCÚCHALO AHORA:\n"
            if yt_link: copy_text += f"📺 YouTube: {yt_link}\n"
            if sp_link: copy_text += f"🟢 Spotify: {sp_link}\n"
            if ap_link: copy_text += f"🍎 Apple Podcasts: {ap_link}\n"
            copy_text += "\n"
            
        copy_text += f"✍️ Por: {author}\n"
        copy_text += f"#GothProds #Metal #Podcast #NoticiasMetal"
        
        text_filename = f"{safe_title}.txt"
        text_path = os.path.join(app.config['UPLOAD_FOLDER'], text_filename)
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(copy_text)
            
        # --- NUEVO: Guardar en Base de Datos ---
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO content_items 
            (section, title, short_desc, full_desc, image_filename, yt_link, sp_link, ap_link, author, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (section, title, short_desc, full_desc, image_filename, yt_link, sp_link, ap_link, author, pub_date))
        conn.commit()
        conn.close()
            
        flash(f'¡Éxito! Archivos generados y página web actualizada automáticamente.', 'success')
        return redirect(url_for('admin_dashboard'))

    conn = get_db_connection()
    all_items = conn.execute("SELECT id, section, title, short_desc, full_desc, yt_link, sp_link, ap_link, created_at FROM content_items WHERE section IN ('El Noticiero Nocturno', 'Reseñas de Conciertos', 'Metal Pulse Tracks') ORDER BY id DESC LIMIT 100").fetchall()
    todas_bandas = conn.execute("SELECT * FROM banda_semana ORDER BY id DESC").fetchall()
    all_users = conn.execute('SELECT id, nombre, username, email, role, is_active FROM users ORDER BY id DESC').fetchall() if session.get('role') in ['admin', 'root'] else []
    conn.close()

    return render_template('admin_dashboard.html', all_items=all_items, settings=get_settings(), todas_bandas=todas_bandas, all_users=all_users)

@app.route('/admin/settings', methods=['POST'])
def update_settings():
    if 'user_id' not in session:
        return redirect(url_for('admin_login'))
    if session.get('role') not in ['admin', 'root']:
        return redirect(url_for('admin_dashboard'))
        
    hero_title = request.form.get('hero_title')
    hero_subtitle = request.form.get('hero_subtitle')
    show_reviews = request.form.get('show_reviews', '0')
    show_news = request.form.get('show_news', '0')
    show_interviews = request.form.get('show_interviews', '0')
    show_metalpulse = request.form.get('show_metalpulse', '0')
    show_agenda = request.form.get('show_agenda', '0')
    show_banda_semana = request.form.get('show_banda_semana', '0')
    hamburger_active = request.form.get('hamburger_active', '0')
    
    conn = get_db_connection()
    queries = [
        ("INSERT OR REPLACE INTO settings (key, value) VALUES ('hero_title', ?)", (hero_title,)),
        ("INSERT OR REPLACE INTO settings (key, value) VALUES ('hero_subtitle', ?)", (hero_subtitle,)),
        ("INSERT OR REPLACE INTO settings (key, value) VALUES ('show_reviews', ?)", (show_reviews,)),
        ("INSERT OR REPLACE INTO settings (key, value) VALUES ('show_news', ?)", (show_news,)),
        ("INSERT OR REPLACE INTO settings (key, value) VALUES ('show_interviews', ?)", (show_interviews,)),
        ("INSERT OR REPLACE INTO settings (key, value) VALUES ('show_metalpulse', ?)", (show_metalpulse,)),
        ("INSERT OR REPLACE INTO settings (key, value) VALUES ('show_agenda', ?)", (show_agenda,)),
        ("INSERT OR REPLACE INTO settings (key, value) VALUES ('show_banda_semana', ?)", (show_banda_semana,)),
        ("INSERT OR REPLACE INTO settings (key, value) VALUES ('hamburger_active', ?)", (hamburger_active,))
    ]
    
    file_keys = ['hero_bg', 'header_logo', 'hamburger_icon', 'galeria_bg', 'metalpulse_bg']
    for fk in file_keys:
        file = request.files.get(fk)
        if file and file.filename != '':
            if file.filename.lower().endswith(('.mp4', '.webm', '.gif')):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
            else:
                filename = optimize_and_save_image(file, app.config['UPLOAD_FOLDER'], prefix=f"{fk}_")
            queries.append(("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (fk, f"updates/{filename}")))

    for q, params in queries:
        conn.execute(q, params)
        
    conn.commit()
    conn.close()
    flash('Look & Feel modificado. Es necesario validar en vista previa antes de liberar.', 'success')
    return redirect(url_for('admin_dashboard'))

import shutil

@app.route('/admin/go_live', methods=['POST'])
def go_live():
    if 'user_id' not in session: return redirect(url_for('admin_login'))
    shutil.copyfile(DB_FILE, DB_LIVE_FILE)
    flash("¡El sitio ha sido actualizado! Los cambios están en vivo.", "success")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/discard_drafts', methods=['POST'])
def discard_drafts():
    if 'user_id' not in session: return redirect(url_for('admin_login'))
    shutil.copyfile(DB_LIVE_FILE, DB_FILE)
    flash("Borradores descartados. El panel vuelve a estar sincronizado con la versión en vivo.", "success")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/caos_sonoro', methods=['POST'])
def update_caos_sonoro():
    if 'user_id' not in session: return redirect(url_for('admin_login'))
    
    caos_episode = request.form.get('caos_episode', '')
    caos_date = request.form.get('caos_date', '')
    caos_time = request.form.get('caos_time', '')
    caos_guests = request.form.get('caos_guests', '')
    
    conn = get_db_connection()
    # Use INSERT OR REPLACE if settings has a unique constraint on key, or INSERT if not exists, but we might not have a UNIQUE constraint on key.
    # We will do a generic approach: delete and insert.
    conn.execute("DELETE FROM settings WHERE key IN ('caos_episode', 'caos_date', 'caos_time', 'caos_guests')")
    
    queries = [
        ("INSERT INTO settings (key, value) VALUES ('caos_episode', ?)", (caos_episode,)),
        ("INSERT INTO settings (key, value) VALUES ('caos_date', ?)", (caos_date,)),
        ("INSERT INTO settings (key, value) VALUES ('caos_time', ?)", (caos_time,)),
        ("INSERT INTO settings (key, value) VALUES ('caos_guests', ?)", (caos_guests,))
    ]
    
    for q, p in queries:
        conn.execute(q, p)
        
    conn.commit()
    conn.close()
    flash('Configuración de Caos Sonoro actualizada. Es necesario validar en vista previa antes de liberar.', 'success')
    return redirect(url_for('admin_dashboard'))

def parse_embed_url(url, plataforma):
    if not url: return ''
    if plataforma == 'Spotify' and 'open.spotify.com/embed' not in url:
        return url.replace('open.spotify.com/', 'open.spotify.com/embed/')
    elif plataforma == 'Apple Music' and 'embed.music.apple.com' not in url:
        return url.replace('music.apple.com', 'embed.music.apple.com')
    return url

@app.route('/admin/banda', methods=['POST'])
def add_banda():
    if 'user_id' not in session: return redirect(url_for('admin_login'))
    
    nombre = request.form['nombre']
    pais = request.form['pais']
    ciudad = request.form['ciudad']
    bio_corta = request.form['bio_corta']
    ano_formacion = request.form.get('ano_formacion', '')
    line_up = request.form.get('line_up', '')
    ig_link = request.form.get('ig_link', '')
    fb_link = request.form.get('fb_link', '')
    tk_link = request.form.get('tk_link', '')
    sp_link = request.form.get('sp_link', '')
    ap_link = request.form.get('ap_link', '')
    yt_link = request.form.get('yt_link', '')
    titulo_resena = request.form.get('titulo_resena', '')
    texto_resena = request.form.get('texto_resena', '')
    
    discografia = request.form.get('discografia', '')
    ultimo_lanzamiento_titulo = request.form.get('ultimo_lanzamiento_titulo', '')
    ultimo_lanzamiento_tipo = request.form.get('ultimo_lanzamiento_tipo', 'Album')
    
    fecha_inicio = request.form.get('fecha_inicio', None)
    fecha_fin = request.form.get('fecha_fin', None)
    
    if fecha_inicio == '': fecha_inicio = None
    if fecha_fin == '': fecha_fin = None
    
    raw_sp = request.form.get('ultimo_lanzamiento_sp_link', '')
    raw_ap = request.form.get('ultimo_lanzamiento_ap_link', '')
    
    ultimo_lanzamiento_sp_link = parse_embed_url(raw_sp, 'Spotify')
    ultimo_lanzamiento_ap_link = parse_embed_url(raw_ap, 'Apple Music')

    file = request.files.get('img_video_path')
    filename = ''
    if file and file.filename != '':
        optimized_name = optimize_and_save_image(file, app.config['UPLOAD_FOLDER'], prefix="banda_")
        filename = f"updates/{optimized_name}"
        
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO banda_semana (nombre, pais, ciudad, bio_corta, img_video_path, ig_link, fb_link, tk_link, sp_link, ap_link, yt_link, ano_formacion, line_up, titulo_resena, texto_resena, discografia, ultimo_lanzamiento_titulo, ultimo_lanzamiento_tipo, ultimo_lanzamiento_sp_link, ultimo_lanzamiento_ap_link, fecha_inicio, fecha_fin)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (nombre, pais, ciudad, bio_corta, filename, ig_link, fb_link, tk_link, sp_link, ap_link, yt_link, ano_formacion, line_up, titulo_resena, texto_resena, discografia, ultimo_lanzamiento_titulo, ultimo_lanzamiento_tipo, ultimo_lanzamiento_sp_link, ultimo_lanzamiento_ap_link, fecha_inicio, fecha_fin))
    conn.commit()
    conn.close()
    
    flash('Banda guardada temporalmente. Es necesario validar en vista previa antes de liberar.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/banda/edit/<int:id>', methods=['POST'])
def edit_banda(id):
    if 'user_id' not in session: return redirect(url_for('admin_login'))
    
    nombre = request.form['nombre']
    pais = request.form['pais']
    ciudad = request.form['ciudad']
    bio_corta = request.form['bio_corta']
    ano_formacion = request.form.get('ano_formacion', '')
    line_up = request.form.get('line_up', '')
    ig_link = request.form.get('ig_link', '')
    fb_link = request.form.get('fb_link', '')
    tk_link = request.form.get('tk_link', '')
    sp_link = request.form.get('sp_link', '')
    ap_link = request.form.get('ap_link', '')
    yt_link = request.form.get('yt_link', '')
    titulo_resena = request.form.get('titulo_resena', '')
    texto_resena = request.form.get('texto_resena', '')
    
    discografia = request.form.get('discografia', '')
    ultimo_lanzamiento_titulo = request.form.get('ultimo_lanzamiento_titulo', '')
    ultimo_lanzamiento_tipo = request.form.get('ultimo_lanzamiento_tipo', 'Album')

    fecha_inicio = request.form.get('fecha_inicio', None)
    fecha_fin = request.form.get('fecha_fin', None)
    
    if fecha_inicio == '': fecha_inicio = None
    if fecha_fin == '': fecha_fin = None
    
    raw_sp = request.form.get('ultimo_lanzamiento_sp_link', '')
    raw_ap = request.form.get('ultimo_lanzamiento_ap_link', '')
    
    ultimo_lanzamiento_sp_link = parse_embed_url(raw_sp, 'Spotify')
    ultimo_lanzamiento_ap_link = parse_embed_url(raw_ap, 'Apple Music')

    conn = get_db_connection()
    
    file = request.files.get('img_video_path')
    if file and file.filename != '':
        optimized_name = optimize_and_save_image(file, app.config['UPLOAD_FOLDER'], prefix="banda_")
        filename = f"updates/{optimized_name}"
        conn.execute('''
            UPDATE banda_semana SET nombre=?, pais=?, ciudad=?, bio_corta=?, img_video_path=?, ig_link=?, fb_link=?, tk_link=?, sp_link=?, ap_link=?, yt_link=?, ano_formacion=?, line_up=?, titulo_resena=?, texto_resena=?, discografia=?, ultimo_lanzamiento_titulo=?, ultimo_lanzamiento_tipo=?, ultimo_lanzamiento_sp_link=?, ultimo_lanzamiento_ap_link=?, fecha_inicio=?, fecha_fin=?
            WHERE id=?
        ''', (nombre, pais, ciudad, bio_corta, filename, ig_link, fb_link, tk_link, sp_link, ap_link, yt_link, ano_formacion, line_up, titulo_resena, texto_resena, discografia, ultimo_lanzamiento_titulo, ultimo_lanzamiento_tipo, ultimo_lanzamiento_sp_link, ultimo_lanzamiento_ap_link, fecha_inicio, fecha_fin, id))
    else:
        conn.execute('''
            UPDATE banda_semana SET nombre=?, pais=?, ciudad=?, bio_corta=?, ig_link=?, fb_link=?, tk_link=?, sp_link=?, ap_link=?, yt_link=?, ano_formacion=?, line_up=?, titulo_resena=?, texto_resena=?, discografia=?, ultimo_lanzamiento_titulo=?, ultimo_lanzamiento_tipo=?, ultimo_lanzamiento_sp_link=?, ultimo_lanzamiento_ap_link=?, fecha_inicio=?, fecha_fin=?
            WHERE id=?
        ''', (nombre, pais, ciudad, bio_corta, ig_link, fb_link, tk_link, sp_link, ap_link, yt_link, ano_formacion, line_up, titulo_resena, texto_resena, discografia, ultimo_lanzamiento_titulo, ultimo_lanzamiento_tipo, ultimo_lanzamiento_sp_link, ultimo_lanzamiento_ap_link, fecha_inicio, fecha_fin, id))
        
    conn.commit()
    conn.close()
    
    flash('Banda editada temporalmente. Es necesario validar en vista previa antes de liberar.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/toggle_banda/<int:id>', methods=['POST'])
def toggle_banda(id):
    if 'user_id' not in session: return redirect(url_for('admin_login'))
    conn = get_db_connection()
    b = conn.execute("SELECT is_active FROM banda_semana WHERE id = ?", (id,)).fetchone()
    if b:
        new_status = 0 if b['is_active'] == 1 else 1
        conn.execute("UPDATE banda_semana SET is_active = ? WHERE id = ?", (new_status, id))
        conn.commit()
    conn.close()
    return jsonify({"success": True})

@app.route('/admin/banda/delete/<int:id>', methods=['POST'])
def delete_banda(id):
    if 'user_id' not in session: return redirect(url_for('admin_login'))
    conn = get_db_connection()
    conn.execute('DELETE FROM banda_semana WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Banda eliminada en borrador. Es necesario validar en vista previa antes de liberar.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete/<int:id>', methods=['POST'])
def delete_record(id):
    if 'user_id' not in session:
        return redirect(url_for('admin_login'))
    conn = get_db_connection()
    conn.execute("DELETE FROM content_items WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash('Eliminación en borrador. Es necesario validar en vista previa antes de liberar.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/edit/<int:id>', methods=['GET', 'POST'])
def edit_record(id):
    if 'user_id' not in session:
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    if request.method == 'POST':
        title = request.form.get('title')
        short_desc = request.form.get('short_desc')
        full_desc = request.form.get('full_desc')
        yt_link = request.form.get('yt_link', '')
        sp_link = request.form.get('sp_link', '')
        ap_link = request.form.get('ap_link', '')
        pub_date = request.form.get('pub_date')
        
        # Opcional imagen nueva
        image = request.files.get('image')
        if image and image.filename:
            image_filename = optimize_and_save_image(image, app.config['UPLOAD_FOLDER'], prefix="content_")
            conn.execute('''
                UPDATE content_items SET title=?, short_desc=?, full_desc=?, image_filename=?, yt_link=?, sp_link=?, ap_link=?, created_at=? WHERE id=?
            ''', (title, short_desc, full_desc, image_filename, yt_link, sp_link, ap_link, pub_date, id))
        else:
            conn.execute('''
                UPDATE content_items SET title=?, short_desc=?, full_desc=?, yt_link=?, sp_link=?, ap_link=?, created_at=? WHERE id=?
            ''', (title, short_desc, full_desc, yt_link, sp_link, ap_link, pub_date, id))
        
        conn.commit()
        conn.close()
        flash('Configuración actualizada exitosamente.', 'success')
        return redirect(url_for('admin_dashboard'))
    
    item = conn.execute("SELECT * FROM content_items WHERE id = ?", (id,)).fetchone()
    conn.close()
    if not item:
        flash('Registro no encontrado.', 'error')
    return render_template('admin_edit.html', item=item)

@app.route('/api/fetch_meta', methods=['POST'])
def fetch_meta():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
        
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
        with urllib.request.urlopen(req, timeout=5) as response:
            html = response.read().decode('utf-8')
            
        title_match = re.search(r'<meta property="og:title" content="([^"]+)"', html)
        if title_match:
            og_title = title_match.group(1)
            # Spotify format: "Track Name - song and lyrics by Band Name | Spotify"
            if ' by ' in og_title:
                parts = og_title.split(' by ')
                song = parts[0].replace(' - song and lyrics', '').replace(' - song', '').strip()
                band = parts[1].split('|')[0].replace('on Apple Music', '').strip()
                return jsonify({'title': song, 'band': band})
            return jsonify({'title': og_title, 'band': ''})
            
        return jsonify({'title': '', 'band': ''})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/update_single_setting', methods=['POST'])
def update_single_setting():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    key = request.form.get('key')
    value = request.form.get('value', '0')
    conn = get_db_connection()
    cur = conn.execute("SELECT * FROM settings WHERE key = ?", (key,))
    if not cur.fetchone():
        conn.execute("INSERT INTO settings (key, value) VALUES (?, ?)", (key, value))
    else:
        conn.execute("UPDATE settings SET value = ? WHERE key = ?", (value, key))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/admin/sync_galeria', methods=['POST'])
def sync_galeria():
    if 'user_id' not in session:
        return redirect(url_for('admin_login'))
    if session.get('role') not in ['admin', 'root']:
        return redirect(url_for('admin_dashboard'))
    import subprocess
    subprocess.run(['python3', 'sync_rss.py', 'galeria'])
    flash('La Galería Nocturna se ha sincronizado automáticamente desde YouTube.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/sync_metal_pulse', methods=['POST'])
def sync_metal_pulse():
    if 'user_id' not in session:
        return redirect(url_for('admin_login'))
    if session.get('role') not in ['admin', 'root']:
        return redirect(url_for('admin_dashboard'))
    import subprocess
    subprocess.run(['python3', 'sync_rss.py', 'metal_pulse'])
    flash('Metal Pulse se ha sincronizado automáticamente desde Apple Podcast/Spotify (Ivoox).', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/sync_entrevistas', methods=['POST'])
def sync_entrevistas():
    if 'user_id' not in session:
        return redirect(url_for('admin_login'))
    if session.get('role') not in ['admin', 'root']:
        return redirect(url_for('admin_dashboard'))
    import subprocess
    subprocess.run(['python3', 'sync_rss.py', 'entrevistas'])
    flash('Entrevistas Under se ha sincronizado automáticamente desde la Playlist de YouTube.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/sync_agenda', methods=['POST'])
def sync_agenda():
    if 'user_id' not in session:
        return redirect(url_for('admin_login'))
    if session.get('role') not in ['admin', 'root']:
        return redirect(url_for('admin_dashboard'))
    
    import urllib.request
    import csv
    import io
    import re
    
    sheet_url = "https://docs.google.com/spreadsheets/d/1FTb-EzMtCGoxb0tAjoVQtTTeGJFd6qCP/export?format=csv"
    try:
        req = urllib.request.Request(sheet_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            csv_data = response.read().decode('utf-8')
            
        if "html" in csv_data[:100].lower() or "google" in csv_data[:100].lower():
            flash('Error: El Google Sheet es PRIVADO. Debes cambiar los permisos del archivo a "Cualquier persona con el enlace puede leer".', 'error')
            return redirect(url_for('admin_dashboard'))
            
        reader = csv.DictReader(io.StringIO(csv_data))
        months_map = {'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12, 'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4}
        
        conn = get_db_connection()
        conn.execute("DELETE FROM content_items WHERE section = 'Agenda Metalera'")
        
        for row in reader:
            if 'Evento' not in row or not row['Evento'].strip(): continue
            evento = row['Evento'].strip()
            ciudad = row.get('Ciudad', '').strip()
            venue = row.get('Venue', '').strip()
            fecha_raw = row.get('Fecha', '').strip()
            gp = row.get('GP', 'N').strip()
            
            month = 12
            for m_name, m_num in months_map.items():
                if m_name in fecha_raw.lower():
                    month = m_num
                    break
                    
            day_match = re.search(r'\d+', fecha_raw)
            day = int(day_match.group(0)) if day_match else 1
            sort_date = f"2026-{month:02d}-{day:02d}"
            logo_filename = f"assets/logos/{evento.lower().replace(' ', '').replace('/', '')}.png"
            
            conn.execute('''
                INSERT INTO content_items (section, title, short_desc, full_desc, image_filename, yt_link, author)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', ("Agenda Metalera", evento, f"{venue} | {ciudad}", fecha_raw, logo_filename, gp, sort_date))
        
        conn.commit()
        conn.close()
        flash('Agenda Metalera actualizada temporalmente. Es necesario validar en vista previa antes de liberar.', 'success')
    except Exception as e:
        flash(f'Error al sincronizar Agenda: {str(e)}', 'error')

    return redirect(url_for('admin_dashboard'))


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
        return jsonify({"success": False, "error": "Unauthorized"}), 403
    conn = get_db_connection()
    user = conn.execute("SELECT is_active FROM users WHERE id=?", (id,)).fetchone()
    if user:
        new_status = 0 if user['is_active'] == 1 else 1
        conn.execute("UPDATE users SET is_active=? WHERE id=?", (new_status, id))
        conn.commit()
    conn.close()
    return jsonify({"success": True})

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
