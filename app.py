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
import json
import re
import unicodedata

load_dotenv('config.env')

app = Flask(__name__, static_folder='.', static_url_path='/static')
app.secret_key = os.getenv('SECRET_KEY', 'super_secret_goth_key')
app.config['UPLOAD_FOLDER'] = 'updates'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 2592000
app.permanent_session_lifetime = timedelta(minutes=30)

@app.template_filter('fromjson')
def fromjson_filter(value):
    if value:
        try:
            return json.loads(value)
        except:
            return []
    return []

@app.template_filter('slugify')
def slugify(value):
    if not value: return ''
    
    # Split by common separators to get the main title part
    for sep in [' - ', ' – ', ' : ', ' | ']:
        if sep in str(value):
            value = str(value).split(sep)[0]
            break
            
    value = unicodedata.normalize('NFKD', str(value)).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    value = re.sub(r'[-\s]+', '-', value)
    
    # Limit to first 5 words if it's still very long
    words = value.split('-')
    if len(words) > 5:
        value = '-'.join(words[:5])
        
    return value

@app.template_filter('process_images')
def process_images_filter(text, images_json):
    if not text: return {"text": "", "unused": []}
    if not images_json: return {"text": text, "unused": []}
    
    try:
        images = json.loads(images_json)
    except:
        images = []
        
    used_indices = set()
    
    def replace_match(match):
        idx = int(match.group(1)) - 1
        if 0 <= idx < len(images):
            used_indices.add(idx)
            img_path = images[idx] if images[idx].startswith('http') or images[idx].startswith('assets') else 'updates/' + images[idx]
            return f'<div style="text-align: center; margin: 30px 0;"><img loading="lazy" src="{img_path}" style="width: 100%; max-width: 800px; height: auto; border-radius: 8px; border: 1px solid #333;" alt="Imagen intercalada"></div>'
        return match.group(0) # Keep [IMG_X] if not found
        
    processed_text = re.sub(r'\[IMG_(\d+)\]', replace_match, text)
    
    # Auto-interleave if there are still unused images
    unused_list = [img for i, img in enumerate(images) if i not in used_indices]
    
    if len(unused_list) > 0:
        # Since text is HTML, split by </p> to find logical paragraph breaks
        raw_splits = re.split(r'(</p>)', processed_text, flags=re.IGNORECASE)
        paragraphs = []
        temp = ""
        for chunk in raw_splits:
            temp += chunk
            if chunk.lower() == '</p>':
                if temp.strip():
                    paragraphs.append(temp)
                temp = ""
        if temp.strip():
            paragraphs.append(temp)
            
        # If no <p> tags, try splitting by <br> tags
        if len(paragraphs) < 2:
            raw_splits = re.split(r'(<br\s*/?>\s*<br\s*/?>)', processed_text, flags=re.IGNORECASE)
            paragraphs = []
            temp = ""
            for chunk in raw_splits:
                temp += chunk
                if '<br' in chunk.lower():
                    if temp.strip():
                        paragraphs.append(temp)
                    temp = ""
            if temp.strip():
                paragraphs.append(temp)
                
        if len(paragraphs) > 1:
            new_paragraphs = []
            img_idx = 0
            
            gap_count = len(paragraphs) - 1
            gap_step = max(1, gap_count // len(unused_list))
            
            for i, p in enumerate(paragraphs):
                new_paragraphs.append(p)
                if i < len(paragraphs) - 1 and img_idx < len(unused_list) and (i + 1) % gap_step == 0:
                    img = unused_list[img_idx]
                    img_path = img if img.startswith('http') or img.startswith('assets') else 'updates/' + img
                    
                    float_dir = "right" if img_idx % 2 == 0 else "left"
                    margin_dir = "margin: 10px 0px 10px 20px;" if float_dir == "right" else "margin: 10px 20px 10px 0px;"
                    
                    img_html = f'<img loading="lazy" src="{img_path}" style="float: {float_dir}; width: 45%; max-width: 350px; {margin_dir} border-radius: 8px; border: 1px solid #333;" alt="Imagen de artículo">'
                    new_paragraphs.append(img_html)
                    
                    original_idx = images.index(img)
                    used_indices.add(original_idx)
                    img_idx += 1
                    
            processed_text = ''.join(new_paragraphs)
            processed_text += '<div style="clear: both;"></div>'
            
    unused_images = [img for i, img in enumerate(images) if i not in used_indices]
    
    return {"text": processed_text, "unused": unused_images}

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
        if 'reset_token' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN reset_token TEXT")
        if 'reset_token_expiry' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN reset_token_expiry TIMESTAMP")
            
        # Migrate existing root user
        cursor.execute("UPDATE users SET username = 'root', nombre = 'Administrador', role = 'admin', is_active = 1 WHERE email = 'goth.prods@gmail.com' AND username IS NULL")
        
        conn.commit()
    except Exception as e:
        print("Schema migration error (users):", e)

    # Auto-create schema for eventos_semana
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS eventos_semana (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo_articulo TEXT,
                fecha_inicio_pub TEXT,
                fecha_fin_pub TEXT,
                nombre_evento TEXT,
                promotor TEXT,
                img_video_path TEXT,
                pais TEXT,
                ciudad TEXT,
                fecha_evento TEXT,
                bio_corta TEXT,
                texto_articulo TEXT,
                fb_link TEXT,
                ig_link TEXT,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Auto-create schema for performance_analytics
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                user_id TEXT,
                page_url TEXT,
                device_type TEXT,
                country TEXT,
                referrer TEXT,
                is_new_user INTEGER DEFAULT 0,
                scroll_depth INTEGER DEFAULT 0,
                time_on_page INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Auto-create schema for newsletter_subscribers
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS newsletter_subscribers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                email TEXT UNIQUE,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Add tracking columns to eventos_semana if not exists (existing logic follows)
        conn.commit()
    except Exception as e:
        print("Schema creation error (eventos_semana / performance / newsletter):", e)

    # Auto-migrate schema for eventos_semana
    try:
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(eventos_semana)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'views' not in columns:
            cursor.execute("ALTER TABLE eventos_semana ADD COLUMN views INTEGER DEFAULT 0")
        if 'likes' not in columns:
            cursor.execute("ALTER TABLE eventos_semana ADD COLUMN likes INTEGER DEFAULT 0")
        conn.commit()
    except Exception as e:
        print("Schema migration error (eventos_semana):", e)

    # Auto-migrate schema for banda_semana
    try:
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(banda_semana)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'views' not in columns:
            cursor.execute("ALTER TABLE banda_semana ADD COLUMN views INTEGER DEFAULT 0")
        if 'likes' not in columns:
            cursor.execute("ALTER TABLE banda_semana ADD COLUMN likes INTEGER DEFAULT 0")
        conn.commit()
    except Exception as e:
        print("Schema migration error (banda_semana):", e)

    # Auto-migrate schema for content_items
    try:
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(content_items)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'views' not in columns:
            cursor.execute("ALTER TABLE content_items ADD COLUMN views INTEGER DEFAULT 0")
        if 'likes' not in columns:
            cursor.execute("ALTER TABLE content_items ADD COLUMN likes INTEGER DEFAULT 0")
        conn.commit()
    except Exception as e:
        print("Schema migration error (content_items):", e)

    # Auto-migrate schema for comments
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER NOT NULL,
                parent_id INTEGER,
                author_name TEXT NOT NULL,
                content TEXT NOT NULL,
                likes INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute("PRAGMA table_info(comments)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'item_type' not in columns:
            cursor.execute("ALTER TABLE comments ADD COLUMN item_type TEXT DEFAULT 'content'")
        conn.commit()
    except Exception as e:
        print("Schema creation/migration error (comments):", e)

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
SENDER_PASSWORD = "vywvezpzobnwurdd"

def send_verification_email(to_email, code, subject="Código de Verificación - Goth Prods"):
    if not SENDER_PASSWORD:
        print(f"[WARNING] No GMAIL_APP_PASSWORD. Simulation: Code for {to_email} is {code}")
        return True
    try:
        msg = MIMEText(f"Tu código para Goth Prods es: {code}")
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = to_email

        server = smtplib.SMTP_SSL(SMTP_SERVER, 465, timeout=10)
        if SENDER_PASSWORD:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

# --- FRONTEND ---
@app.route('/api/analytics/init', methods=['POST'])
def init_analytics():
    data = request.json
    session_id = data.get('session_id')
    user_id = data.get('user_id')
    page_url = data.get('page_url')
    device_type = data.get('device_type')
    country = data.get('country', 'Unknown')
    referrer = data.get('referrer')
    is_new_user = 1 if data.get('is_new_user') else 0
    
    if not country or country == 'Unknown':
        client_ip = request.headers.get('CF-Connecting-IP') or \
                    request.headers.get('X-Real-IP') or \
                    request.headers.get('X-Forwarded-For', request.remote_addr)
        if client_ip:
            client_ip = client_ip.split(',')[0].strip()
            if client_ip not in ('127.0.0.1', '::1', 'localhost'):
                try:
                    import urllib.request, json
                    req = urllib.request.Request(f'http://ip-api.com/json/{client_ip}', headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req, timeout=2) as response:
                        ip_data = json.loads(response.read().decode())
                        if ip_data.get('status') == 'success':
                            country = ip_data.get('country', 'Unknown')
                except Exception:
                    pass
    
    conn = get_db_connection(live=True)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO performance_analytics 
        (session_id, user_id, page_url, device_type, country, referrer, is_new_user, scroll_depth, time_on_page)
        VALUES (?, ?, ?, ?, ?, ?, ?, 0, 0)
    ''', (session_id, user_id, page_url, device_type, country, referrer, is_new_user))
    record_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({"success": True, "record_id": record_id})

@app.route('/api/analytics/update', methods=['POST'])
def update_analytics():
    data = request.json or {}
    record_id = data.get('record_id')
    scroll_depth = data.get('scroll_depth', 0)
    time_on_page = data.get('time_on_page', 0)
    section_times = data.get('section_times', {})
    
    if not record_id:
        return jsonify({"success": False}), 400
        
    conn = get_db_connection(live=True)
    cursor = conn.cursor()
    
    import json
    section_times_str = json.dumps(section_times)
    
    # Only update if the new values are greater (e.g., they scrolled further or spent more time)
    cursor.execute('''
        UPDATE performance_analytics 
        SET scroll_depth = MAX(scroll_depth, ?), time_on_page = MAX(time_on_page, ?), section_times = ?
        WHERE id = ?
    ''', (scroll_depth, time_on_page, section_times_str, record_id))
    
    conn.commit()
    conn.close()
    
    return jsonify({"success": True})
@app.route('/api/track_view/<int:item_id>', methods=['POST'])
def track_view(item_id):
    item_type = request.args.get('type', 'content')
    is_preview = request.args.get('preview') == '1' and 'user_id' in session
    conn = get_db_connection(live=not is_preview)
    cursor = conn.cursor()
    
    if item_type == 'poster':
        cursor.execute("SELECT value FROM settings WHERE key = 'poster_views'")
        row = cursor.fetchone()
        new_views = int(row['value']) + 1 if row and row['value'] else 1
        cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('poster_views', ?)", (str(new_views),))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "views": new_views})
    
    if item_type == 'banda':
        table = 'banda_semana'
    elif item_type == 'evento':
        table = 'eventos_semana'
    elif item_type == 'mexapedia':
        return jsonify({"success": True, "views": 0})
    else:
        table = 'content_items'
        
    cursor.execute(f"UPDATE {table} SET views = COALESCE(views, 0) + 1 WHERE id = ?", (item_id,))
    conn.commit()
    
    # Return the new view count
    cursor.execute(f"SELECT views FROM {table} WHERE id = ?", (item_id,))
    row = cursor.fetchone()
    conn.close()
    
    new_views = row['views'] if row else 0
    return jsonify({"success": True, "views": new_views})

@app.route('/api/comments/<int:item_id>', methods=['GET'])
def get_comments(item_id):
    item_type = request.args.get('type', 'content')
    conn = get_db_connection(live=True)
    comments = conn.execute("SELECT * FROM comments WHERE item_id = ? AND item_type = ? ORDER BY created_at ASC", (item_id, item_type)).fetchall()
    conn.close()
    
    # Build a tree structure
    comments_list = [dict(c) for c in comments]
    tree = []
    lookup = {}
    for c in comments_list:
        c['replies'] = []
        lookup[c['id']] = c
        
    for c in comments_list:
        if c['parent_id']:
            parent = lookup.get(c['parent_id'])
            if parent:
                parent['replies'].append(c)
            else:
                tree.append(c) # Fallback if parent missing
        else:
            tree.append(c)
            
    return jsonify({"success": True, "comments": tree})

@app.route('/api/comments/<int:item_id>', methods=['POST'])
def post_comment(item_id):
    item_type = request.args.get('type', 'content')
    data = request.json
    author_name = data.get('author_name', 'Anónimo').strip()
    content = data.get('content', '').strip()
    parent_id = data.get('parent_id')
    
    if not author_name:
        author_name = 'Anónimo'
    if not content:
        return jsonify({"success": False, "error": "El comentario no puede estar vacío"}), 400
        
    is_preview = request.args.get('preview') == '1' and 'user_id' in session
    conn = get_db_connection(live=not is_preview)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO comments (item_id, item_type, parent_id, author_name, content) VALUES (?, ?, ?, ?, ?)",
        (item_id, item_type, parent_id, author_name, content)
    )
    conn.commit()
    conn.close()
    
    return jsonify({"success": True})

@app.route('/api/comments/like/<int:comment_id>', methods=['POST'])
def like_comment(comment_id):
    is_preview = request.args.get('preview') == '1' and 'user_id' in session
    conn = get_db_connection(live=not is_preview)
    cursor = conn.cursor()
    cursor.execute("UPDATE comments SET likes = COALESCE(likes, 0) + 1 WHERE id = ?", (comment_id,))
    conn.commit()
    
    cursor.execute("SELECT likes FROM comments WHERE id = ?", (comment_id,))
    row = cursor.fetchone()
    conn.close()
    
    return jsonify({"success": True, "likes": row['likes'] if row else 0})

@app.route('/api/track_like/<int:item_id>', methods=['POST'])
def track_like(item_id):
    item_type = request.args.get('type', 'content')
    is_preview = request.args.get('preview') == '1' and 'user_id' in session
    conn = get_db_connection(live=not is_preview)
    cursor = conn.cursor()
    
    if item_type == 'poster':
        cursor.execute("SELECT value FROM settings WHERE key = 'poster_likes'")
        row = cursor.fetchone()
        new_likes = int(row['value']) + 1 if row and row['value'] else 1
        cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('poster_likes', ?)", (str(new_likes),))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "likes": new_likes})
    
    if item_type == 'banda':
        table = 'banda_semana'
    elif item_type == 'evento':
        table = 'eventos_semana'
    else:
        table = 'content_items'
        
    cursor.execute(f"UPDATE {table} SET likes = COALESCE(likes, 0) + 1 WHERE id = ?", (item_id,))
    conn.commit()
    
    # Return the new like count
    cursor.execute(f"SELECT likes FROM {table} WHERE id = ?", (item_id,))
    row = cursor.fetchone()
    conn.close()
    
    new_likes = row['likes'] if row else 0
    return jsonify({"success": True, "likes": new_likes})

@app.route('/')
def index():
    is_preview = request.args.get('preview') == '1' and 'user_id' in session
    conn = get_db_connection(live=not is_preview)
    settings = get_settings(live=not is_preview)
    import datetime
    mexico_tz = datetime.timezone(datetime.timedelta(hours=-6))
    current_date = datetime.datetime.now(mexico_tz).strftime("%Y-%m-%d")

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
        if not is_preview:
            if fecha_inicio and current_date < fecha_inicio:
                in_date_range = False
            if fecha_fin and current_date > fecha_fin:
                in_date_range = False
            
        if is_active == 1 and in_date_range and b['nombre'] not in seen_bands:
            seen_bands.add(b['nombre'])
            bandas_semana.append(b)
            if len(bandas_semana) == 5:
                break
                
    # Query for Eventos de la Semana
    raw_eventos = conn.execute("SELECT * FROM eventos_semana ORDER BY id DESC").fetchall()
    eventos_semana = []
    for e in raw_eventos:
        is_active = e['is_active'] if 'is_active' in e.keys() else 1
        
        fecha_inicio = e['fecha_inicio_pub'] if 'fecha_inicio_pub' in e.keys() and e['fecha_inicio_pub'] else None
        fecha_fin = e['fecha_fin_pub'] if 'fecha_fin_pub' in e.keys() and e['fecha_fin_pub'] else None
        
        in_date_range = True
        if not is_preview:
            if fecha_inicio and current_date < fecha_inicio:
                in_date_range = False
            if fecha_fin and current_date > fecha_fin:
                in_date_range = False
            
        if is_active == 1 and in_date_range:
            eventos_semana.append(e)
    
    # Query for Colectivo Mexapedia (Latest active)
    mexapedia_record = conn.execute("SELECT * FROM colectivo_mexapedia WHERE is_active = 1 ORDER BY id DESC LIMIT 1").fetchone()
    
    # Existing content queries
    noticiero_items = conn.execute("SELECT * FROM content_items WHERE section = 'El Noticiero Nocturno' ORDER BY created_at DESC").fetchall()
    reseñas_items = conn.execute("SELECT * FROM content_items WHERE section = 'Reseñas de Conciertos' ORDER BY created_at DESC, id DESC").fetchall()
    entrevistas_items = conn.execute("SELECT * FROM content_items WHERE section = 'Entrevistas Under' ORDER BY created_at DESC, id DESC").fetchall()
    agenda_items = conn.execute("SELECT * FROM content_items WHERE section = 'Agenda Metalera' ORDER BY author ASC").fetchall()
    galeria_items = conn.execute("SELECT * FROM content_items WHERE section IN ('La Galería Nocturna', 'Caos Sonoro', 'Colaboraciones') ORDER BY created_at DESC, id DESC").fetchall()
    metalpulse_items = conn.execute("SELECT * FROM content_items WHERE section = 'Metal Pulse' ORDER BY created_at DESC, id DESC").fetchall()
    caossonoro_items = conn.execute("SELECT * FROM content_items WHERE section = 'Caos Sonoro' ORDER BY created_at DESC, id DESC").fetchall()
    
    # Filter Metal Pulse Tracks: exclude invalid/old tracks (like '.') and keep valid recent ones
    all_tracks = conn.execute("SELECT * FROM content_items WHERE section = 'Metal Pulse Tracks' AND full_desc != '.' ORDER BY id DESC").fetchall()
    
    hide_past_mp = settings.get('hide_past_metalpulse', '0') == '1'
    if hide_past_mp and all_tracks:
        # Determine the latest available month from existing records if current month has none
        months_es = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        now_mx = datetime.datetime.now(mexico_tz)
        cur_year = now_mx.year
        cur_month_idx = now_mx.month - 1
        
        valid_months = set()
        for i in range(24): # current and next 24 months
            m_idx = (cur_month_idx + i) % 12
            y = cur_year + (cur_month_idx + i) // 12
            valid_months.add(f"{months_es[m_idx]} {y}")
            
        filtered = [t for t in all_tracks if t['full_desc'] in valid_months]
        if filtered:
            metalpulse_tracks = filtered
        else:
            # Fallback to the latest available month's tracks
            latest_month = all_tracks[0]['full_desc']
            metalpulse_tracks = [t for t in all_tracks if t['full_desc'] == latest_month]
    else:
        metalpulse_tracks = all_tracks
        
    conn.close()
    
    # Group agenda items by month and year
    from collections import OrderedDict
    import datetime
    
    # Define spanish months manually to map from date string
    spanish_months = {
        '01': 'Ene', '02': 'Feb', '03': 'Mar', '04': 'Abr',
        '05': 'May', '06': 'Jun', '07': 'Jul', '08': 'Ago',
        '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dic'
    }
    
    agenda_grouped_2026 = OrderedDict()
    agenda_grouped_2027 = OrderedDict()
    current_date = (datetime.datetime.utcnow() - datetime.timedelta(hours=6)).strftime("%Y-%m-%d")
    
    for item in agenda_items:
        # author has 'YYYY-MM-DD'
        parts = item['author'].split('-') if item['author'] else ['2026', '05']
        year = parts[0] if len(parts) > 0 else '2026'
        month_num = parts[1] if len(parts) > 1 else '05'
        month_name = spanish_months.get(month_num, 'Mayo')
        
        target_group = agenda_grouped_2027 if year == '2027' else agenda_grouped_2026
        if month_name not in target_group:
            target_group[month_name] = []
        target_group[month_name].append(item)

    upcoming_agenda = [item for item in agenda_items if item['author'] >= current_date]

    return render_template('index.html', 
                           noticiero_items=noticiero_items,
                           reseñas_items=reseñas_items,
                           entrevistas_items=entrevistas_items,
                           galeria_items=galeria_items,
                           metalpulse_items=metalpulse_items,
                           metalpulse_tracks=metalpulse_tracks,
                           caossonoro_items=caossonoro_items,
                           agenda_grouped_2026=agenda_grouped_2026,
                           agenda_grouped_2027=agenda_grouped_2027,
                           agenda_items=agenda_items,
                           upcoming_agenda=upcoming_agenda,
                           current_date=current_date,
                           settings=get_settings(live=not is_preview),
                           bandas_semana=bandas_semana,
                           eventos_semana=eventos_semana,
                           mexapedia_record=mexapedia_record, is_preview=is_preview)

@app.route('/banda/<int:id>')
@app.route('/banda/<int:id>-<string:slug>')
def view_banda(id, slug=None):
    is_preview = request.args.get('preview') == '1'
    conn = get_db_connection(live=not is_preview)
    banda = conn.execute("SELECT * FROM banda_semana WHERE id = ?", (id,)).fetchone()
    conn.close()
    
    if not banda:
        return "Banda no encontrada", 404
        
    settings = get_settings(live=not is_preview)
    return render_template('banda.html', banda=banda, settings=settings, is_preview=is_preview)

@app.route('/evento/<int:id>')
@app.route('/evento/<int:id>-<string:slug>')
def view_evento(id, slug=None):
    is_preview = request.args.get('preview') == '1'
    conn = get_db_connection(live=not is_preview)
    evento = conn.execute("SELECT * FROM eventos_semana WHERE id = ?", (id,)).fetchone()
    conn.close()
    
    if not evento:
        return "Evento no encontrado", 404
        
    settings = get_settings(live=not is_preview)
    return render_template('evento.html', evento=evento, settings=settings, is_preview=is_preview)

@app.route('/mexapedia/<int:id>')
@app.route('/mexapedia/<int:id>-<string:slug>')
def view_mexapedia(id, slug=None):
    is_preview = request.args.get('preview') == '1'
    conn = get_db_connection(live=not is_preview)
    mexapedia_record = conn.execute("SELECT * FROM colectivo_mexapedia WHERE id = ?", (id,)).fetchone()
    conn.close()
    
    if not mexapedia_record:
        return "Registro no encontrado", 404
        
    settings = get_settings(live=not is_preview)
    return render_template('mexapedia.html', mexapedia_record=mexapedia_record, settings=settings, is_preview=is_preview)

@app.route('/articulo/<int:id>')
@app.route('/articulo/<int:id>-<string:slug>')
def view_articulo(id, slug=None):
    is_preview = request.args.get('preview') == '1'
    conn = get_db_connection(live=not is_preview)
    item = conn.execute("SELECT * FROM content_items WHERE id = ?", (id,)).fetchone()
    conn.close()
    
    if not item:
        return "Artículo no encontrado", 404
        
    settings = get_settings(live=not is_preview)
    return render_template('articulo.html', item=item, settings=settings, is_preview=is_preview)

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
        server = smtplib.SMTP_SSL(SMTP_SERVER, 465, timeout=10)
        if SENDER_PASSWORD:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        # Si se envió correctamente, puedes devolver a la página con un mensaje
        flash("¡Mensaje y material enviados exitosamente a contacto@gothprods.com!")
        return redirect('/#contact')
    except Exception as e:
        print(f"Error al enviar contacto: {e}")
        flash(f"Hubo un error al enviar el correo: {str(e)}")
        return redirect('/#contact')

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
            
        additional_images = request.files.getlist('additional_images')
        additional_filenames = []
        for extra_img in additional_images:
            if extra_img and extra_img.filename:
                extra_filename = optimize_and_save_image(extra_img, app.config['UPLOAD_FOLDER'], prefix="extra_")
                additional_filenames.append(extra_filename)
        import json
        additional_images_json = json.dumps(additional_filenames)
            
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
            (section, title, short_desc, full_desc, image_filename, yt_link, sp_link, ap_link, author, created_at, additional_images)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (section, title, short_desc, full_desc, image_filename, yt_link, sp_link, ap_link, author, pub_date, additional_images_json))
        conn.commit()
        conn.close()
            
        flash(f'¡Éxito! Archivos generados y página web actualizada automáticamente.', 'success')
        return redirect(url_for('admin_dashboard'))

    conn = get_db_connection()
    all_items = conn.execute("SELECT id, section, title, short_desc, full_desc, yt_link, sp_link, ap_link, created_at, additional_images FROM content_items WHERE section IN ('El Noticiero Nocturno', 'Reseñas de Conciertos', 'Metal Pulse Tracks') ORDER BY id DESC LIMIT 100").fetchall()
    todas_bandas = conn.execute("SELECT * FROM banda_semana ORDER BY id DESC").fetchall()
    todos_eventos = conn.execute("SELECT * FROM eventos_semana ORDER BY id DESC").fetchall()
    todos_mexapedia = conn.execute("SELECT * FROM colectivo_mexapedia ORDER BY id DESC").fetchall()
    all_users = conn.execute('SELECT id, nombre, username, email, role, is_active FROM users ORDER BY id DESC').fetchall() if session.get('role') in ['admin', 'root'] else []
    conn_live = get_db_connection(live=True)
    
    perf_range = request.args.get('range', 'all')
    perf_start = request.args.get('start', '')
    perf_end = request.args.get('end', '')
    
    perf_query = "SELECT * FROM performance_analytics WHERE page_url NOT LIKE '%localhost%' AND page_url NOT LIKE '%127.0.0.1%'"
    perf_params = []
    
    if perf_range == '7':
        perf_query += " AND created_at >= date('now', '-7 days')"
    elif perf_range == '30':
        perf_query += " AND created_at >= date('now', '-30 days')"
    elif perf_range == '90':
        perf_query += " AND created_at >= date('now', '-90 days')"
    elif perf_range == 'custom' and perf_start and perf_end:
        perf_query += " AND created_at >= ? AND created_at <= ?"
        perf_params = [perf_start + ' 00:00:00', perf_end + ' 23:59:59']
        
    perf_query += " ORDER BY id DESC"
    
    analytics_rows = conn_live.execute(perf_query, perf_params).fetchall()
    
    interactions_query = '''
    SELECT section, title, views, likes, 
           (SELECT COUNT(*) FROM comments WHERE item_id = content_items.id AND item_type = 'content') as comments_count
    FROM content_items 
    WHERE views > 0 OR likes > 0 OR (SELECT COUNT(*) FROM comments WHERE item_id = content_items.id AND item_type = 'content') > 0
    
    UNION ALL
    
    SELECT 'Banda de la Semana' as section, nombre as title, views, likes,
           (SELECT COUNT(*) FROM comments WHERE item_id = banda_semana.id AND item_type = 'banda') as comments_count
    FROM banda_semana
    WHERE views > 0 OR likes > 0 OR (SELECT COUNT(*) FROM comments WHERE item_id = banda_semana.id AND item_type = 'banda') > 0
    
    UNION ALL
    
    SELECT 'Agenda Metalera' as section, titulo_articulo as title, views, likes,
           (SELECT COUNT(*) FROM comments WHERE item_id = eventos_semana.id AND item_type = 'evento') as comments_count
    FROM eventos_semana
    WHERE views > 0 OR likes > 0 OR (SELECT COUNT(*) FROM comments WHERE item_id = eventos_semana.id AND item_type = 'evento') > 0
    
    ORDER BY views DESC, likes DESC
    '''
    interactions_rows = conn_live.execute(interactions_query).fetchall()
    
    conn_live.close()
    
    analytics_data = [dict(row) for row in analytics_rows]
    interactions_data = [dict(row) for row in interactions_rows]
    
    conn.close()

    return render_template('admin_dashboard.html', all_items=all_items, settings=get_settings(), todas_bandas=todas_bandas, todos_eventos=todos_eventos, todos_mexapedia=todos_mexapedia, all_users=all_users, analytics_data=analytics_data, interactions_data=interactions_data)

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
    show_el_pit = request.form.get('show_el_pit', '0')
    show_galeria_nocturna = request.form.get('show_galeria_nocturna', '0')
    show_contactanos = request.form.get('show_contactanos', '0')
    show_medios_aliados = request.form.get('show_medios_aliados', '0')
    show_el_equipo = request.form.get('show_el_equipo', '0')
    
    title_destacados = request.form.get('title_destacados')
    title_el_pit = request.form.get('title_el_pit')
    title_galeria = request.form.get('title_galeria')
    title_metalpulse = request.form.get('title_metalpulse')
    title_reviews = request.form.get('title_reviews')
    title_news = request.form.get('title_news')
    title_interviews = request.form.get('title_interviews')
    title_agenda = request.form.get('title_agenda')
    title_contacto = request.form.get('title_contacto')
    agenda_desc = request.form.get('agenda_desc')
    
    title_equipo = request.form.get('title_equipo')
    show_equipo_menu = request.form.get('show_equipo_menu', '0')
    
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
        ("INSERT OR REPLACE INTO settings (key, value) VALUES ('show_el_pit', ?)", (show_el_pit,)),
        ("INSERT OR REPLACE INTO settings (key, value) VALUES ('show_galeria_nocturna', ?)", (show_galeria_nocturna,)),
        ("INSERT OR REPLACE INTO settings (key, value) VALUES ('show_contactanos', ?)", (show_contactanos,)),
        ("INSERT OR REPLACE INTO settings (key, value) VALUES ('show_medios_aliados', ?)", (show_medios_aliados,)),
        ("INSERT OR REPLACE INTO settings (key, value) VALUES ('show_el_equipo', ?)", (show_el_equipo,)),
        ("INSERT OR REPLACE INTO settings (key, value) VALUES ('show_equipo_menu', ?)", (show_equipo_menu,)),
        ("INSERT OR REPLACE INTO settings (key, value) VALUES ('agenda_desc', ?)", (agenda_desc,))
    ]
    
    titles_dict = {
        'title_destacados': title_destacados,
        'title_el_pit': title_el_pit,
        'title_galeria': title_galeria,
        'title_metalpulse': title_metalpulse,
        'title_reviews': title_reviews,
        'title_news': title_news,
        'title_interviews': title_interviews,
        'title_agenda': title_agenda,
        'title_contacto': title_contacto,
        'title_equipo': title_equipo
    }
    for k, v in titles_dict.items():
        if v is not None:
            queries.append(("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (k, v)))
    
    file_keys = ['hero_bg', 'header_logo', 'galeria_bg', 'metalpulse_bg', 
                 'icon_destacados', 'icon_el_pit', 'icon_galeria', 'icon_metalpulse',
                 'icon_reviews', 'icon_news', 'icon_interviews', 'icon_agenda', 'icon_contacto', 'icon_equipo',
                 'logo_aliado_1', 'logo_aliado_2', 'logo_aliado_3', 'logo_aliado_4', 'logo_aliado_5',
                 'logo_aliado_6', 'logo_aliado_7', 'logo_aliado_8', 'logo_aliado_9', 'logo_aliado_10',
                 'team_img_1', 'team_img_2', 'team_img_3', 'team_img_4', 'team_img_5']
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

    # Extraer campos dinámicos de equipo e historia
    print("====== FORM SUBMITTED ======")
    print(request.form)
    print("============================")
    for key in request.form.keys():
        if key.startswith('team_name_') or key.startswith('team_role_') or key.startswith('team_bio_') or key.startswith('team_history_'):
            queries.append(("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, request.form[key])))

    for q, params in queries:
        conn.execute(q, params)
        
    posters = request.files.getlist('agenda_posters')
    poster_paths = []
    for file in posters:
        if file and file.filename != '':
            filename = optimize_and_save_image(file, app.config['UPLOAD_FOLDER'], prefix="agenda_poster_")
            poster_paths.append(f"updates/{filename}")
            
    if poster_paths:
        conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", ('agenda_poster', ','.join(poster_paths)))
        
    if request.form.get('remove_agenda_poster') == '1':
        conn.execute("DELETE FROM settings WHERE key='agenda_poster'")
        
    conn.commit()
    conn.close()
    flash('Look & Feel modificado. Es necesario validar en vista previa antes de liberar.', 'success')
    return redirect(url_for('admin_dashboard'))

import shutil

@app.route('/admin/go_live', methods=['POST'])
def go_live():
    if 'user_id' not in session: return redirect(url_for('admin_login'))
    
    live_data = {
        'content_items': {},
        'banda_semana': {},
        'eventos_semana': {},
        'comments': [],
        'performance_analytics': [],
        'settings': {}
    }
    
    if os.path.exists(DB_LIVE_FILE):
        try:
            live_conn = sqlite3.connect(DB_LIVE_FILE)
            live_conn.row_factory = sqlite3.Row
            
            for table in ['content_items', 'banda_semana', 'eventos_semana']:
                rows = live_conn.execute(f"SELECT id, likes, views FROM {table}").fetchall()
                for r in rows:
                    live_data[table][r['id']] = {'likes': r['likes'], 'views': r['views']}
                    
            comments_rows = live_conn.execute("SELECT * FROM comments").fetchall()
            if comments_rows:
                live_data['comments'] = [dict(r) for r in comments_rows]
                
            perf_rows = live_conn.execute("SELECT * FROM performance_analytics").fetchall()
            if perf_rows:
                live_data['performance_analytics'] = [dict(r) for r in perf_rows]
                
            # Preserve poster_likes and poster_views
            try:
                settings_rows = live_conn.execute("SELECT key, value FROM settings WHERE key IN ('poster_likes', 'poster_views')").fetchall()
                for r in settings_rows:
                    live_data['settings'][r['key']] = r['value']
            except Exception:
                pass
                
            live_conn.close()
        except Exception as e:
            print(f"Error extrayendo datos en vivo: {e}")
            
    shutil.copyfile(DB_FILE, DB_LIVE_FILE)
    
    try:
        new_live_conn = sqlite3.connect(DB_LIVE_FILE)
        new_preview_conn = sqlite3.connect(DB_FILE)
        
        for conn_obj in [new_live_conn, new_preview_conn]:
            for table in ['content_items', 'banda_semana', 'eventos_semana']:
                for item_id, stats in live_data[table].items():
                    conn_obj.execute(
                        f"UPDATE {table} SET likes = ?, views = ? WHERE id = ?",
                        (stats['likes'], stats['views'], item_id)
                    )
                    
            conn_obj.execute("DELETE FROM comments")
            for comment in live_data['comments']:
                cols = ', '.join(comment.keys())
                placeholders = ', '.join(['?' for _ in comment.values()])
                conn_obj.execute(
                    f"INSERT INTO comments ({cols}) VALUES ({placeholders})",
                    tuple(comment.values())
                )
                
            conn_obj.execute("DELETE FROM performance_analytics")
            for perf in live_data['performance_analytics']:
                cols = ', '.join(perf.keys())
                placeholders = ', '.join(['?' for _ in perf.values()])
                conn_obj.execute(
                    f"INSERT INTO performance_analytics ({cols}) VALUES ({placeholders})",
                    tuple(perf.values())
                )
                
            for k, v in live_data['settings'].items():
                conn_obj.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (k, v))
                
            conn_obj.commit()
            conn_obj.close()
    except Exception as e:
        print(f"Error restaurando datos en vivo: {e}")

    flash("¡El sitio ha sido actualizado! Los cambios están en vivo y la interacción de usuarios fue preservada.", "success")
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

@app.route('/admin/mexapedia/settings', methods=['POST'])
def update_mexapedia_settings():
    if 'user_id' not in session: return redirect(url_for('admin_login'))
    if session.get('role') not in ['admin', 'root']:
        return "Acceso denegado", 403

    show_mexapedia = request.form.get('show_mexapedia', '0')
    title_mexapedia = request.form.get('title_mexapedia')

    conn = get_db_connection()
    if title_mexapedia is not None:
        conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('title_mexapedia', ?)", (title_mexapedia,))
    conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('show_mexapedia', ?)", (show_mexapedia,))

    file = request.files.get('icon_mexapedia')
    if file and file.filename != '':
        filename = optimize_and_save_image(file, app.config['UPLOAD_FOLDER'], prefix="icon_mexapedia_")
        conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", ('icon_mexapedia', f"updates/{filename}"))

    conn.commit()
    conn.close()
    flash("Configuración del menú de Mexapedia guardada.")
    return redirect(url_for('admin_dashboard') + '#tab-mexapedia')

@app.route('/admin/mexapedia/add', methods=['POST'])
def add_mexapedia():
    if 'user_id' not in session: return redirect(url_for('admin_login'))
    
    titulo = request.form.get('titulo')
    descripcion = request.form.get('descripcion')
    is_active = request.form.get('is_active', '0')
    
    img_path = None
    file = request.files.get('mexapedia_art')
    if file and file.filename != '':
        if file.filename.lower().endswith(('.mp4', '.webm', '.gif')):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            img_path = f"updates/{filename}"
        else:
            filename = optimize_and_save_image(file, app.config['UPLOAD_FOLDER'], prefix="mexapedia_")
            img_path = f"updates/{filename}"

    conn = get_db_connection()
    conn.execute('''
        INSERT INTO colectivo_mexapedia (titulo, descripcion, img_path, is_active)
        VALUES (?, ?, ?, ?)
    ''', (titulo, descripcion, img_path, is_active))
    conn.commit()
    conn.close()
    flash("Registro de Mexapedia añadido exitosamente.")
    return redirect(url_for('admin_dashboard') + '#tab-mexapedia')

@app.route('/admin/mexapedia/edit/<int:id>', methods=['POST'])
def edit_mexapedia(id):
    if 'user_id' not in session: return redirect(url_for('admin_login'))
    
    titulo = request.form.get('titulo')
    descripcion = request.form.get('descripcion')
    is_active = request.form.get('is_active', '0')
    
    conn = get_db_connection()
    
    file = request.files.get('mexapedia_art')
    if file and file.filename != '':
        if file.filename.lower().endswith(('.mp4', '.webm', '.gif')):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            img_path = f"updates/{filename}"
        else:
            filename = optimize_and_save_image(file, app.config['UPLOAD_FOLDER'], prefix="mexapedia_")
            img_path = f"updates/{filename}"
            
        conn.execute('''
            UPDATE colectivo_mexapedia 
            SET titulo = ?, descripcion = ?, img_path = ?, is_active = ?
            WHERE id = ?
        ''', (titulo, descripcion, img_path, is_active, id))
    else:
        conn.execute('''
            UPDATE colectivo_mexapedia 
            SET titulo = ?, descripcion = ?, is_active = ?
            WHERE id = ?
        ''', (titulo, descripcion, is_active, id))
        
    conn.commit()
    conn.close()
    flash("Registro de Mexapedia editado exitosamente.")
    return redirect(url_for('admin_dashboard') + '#tab-mexapedia')

@app.route('/admin/mexapedia/delete/<int:id>', methods=['POST'])
def delete_mexapedia(id):
    if 'user_id' not in session: return redirect(url_for('admin_login'))
    if session.get('role') not in ['admin', 'root']: return "Acceso denegado", 403

    conn = get_db_connection()
    conn.execute('DELETE FROM colectivo_mexapedia WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash("Registro de Mexapedia eliminado.")
    return redirect(url_for('admin_dashboard') + '#tab-mexapedia')

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

@app.route('/admin/evento/delete/<int:id>', methods=['POST'])
def delete_evento(id):
    if 'user_id' not in session: return redirect(url_for('admin_login'))
    conn = get_db_connection()
    conn.execute('DELETE FROM eventos_semana WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Evento eliminado en borrador. Es necesario validar en vista previa antes de liberar.', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/eventos', methods=['POST'])
def add_evento():
    if 'user_id' not in session: return redirect(url_for('admin_login'))
    
    titulo_articulo = request.form.get('titulo_articulo', '')
    fecha_inicio_pub = request.form.get('fecha_inicio_pub', '')
    fecha_fin_pub = request.form.get('fecha_fin_pub', '')
    if fecha_inicio_pub == '': fecha_inicio_pub = None
    if fecha_fin_pub == '': fecha_fin_pub = None
    
    nombre_evento = request.form.get('nombre_evento', '')
    promotor = request.form.get('promotor', '')
    pais = request.form.get('pais', '')
    ciudad = request.form.get('ciudad', '')
    fecha_evento = request.form.get('fecha_evento', '')
    bio_corta = request.form.get('bio_corta', '')
    texto_articulo = request.form.get('texto_articulo', '')
    fb_link = request.form.get('fb_link', '')
    ig_link = request.form.get('ig_link', '')
    
    file = request.files.get('img_video_path')
    filename = ''
    if file and file.filename != '':
        optimized_name = optimize_and_save_image(file, app.config['UPLOAD_FOLDER'], prefix="evento_")
        filename = f"updates/{optimized_name}"
        
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO eventos_semana (titulo_articulo, fecha_inicio_pub, fecha_fin_pub, nombre_evento, promotor, img_video_path, pais, ciudad, fecha_evento, bio_corta, texto_articulo, fb_link, ig_link)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (titulo_articulo, fecha_inicio_pub, fecha_fin_pub, nombre_evento, promotor, filename, pais, ciudad, fecha_evento, bio_corta, texto_articulo, fb_link, ig_link))
    conn.commit()
    conn.close()
    
    flash('Evento guardado exitosamente.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/eventos/edit/<int:id>', methods=['POST'])
def edit_evento(id):
    if 'user_id' not in session: return redirect(url_for('admin_login'))
    
    titulo_articulo = request.form.get('titulo_articulo', '')
    fecha_inicio_pub = request.form.get('fecha_inicio_pub', '')
    fecha_fin_pub = request.form.get('fecha_fin_pub', '')
    if fecha_inicio_pub == '': fecha_inicio_pub = None
    if fecha_fin_pub == '': fecha_fin_pub = None
    
    nombre_evento = request.form.get('nombre_evento', '')
    promotor = request.form.get('promotor', '')
    pais = request.form.get('pais', '')
    ciudad = request.form.get('ciudad', '')
    fecha_evento = request.form.get('fecha_evento', '')
    bio_corta = request.form.get('bio_corta', '')
    texto_articulo = request.form.get('texto_articulo', '')
    fb_link = request.form.get('fb_link', '')
    ig_link = request.form.get('ig_link', '')

    conn = get_db_connection()
    
    file = request.files.get('img_video_path')
    if file and file.filename != '':
        optimized_name = optimize_and_save_image(file, app.config['UPLOAD_FOLDER'], prefix="evento_")
        filename = f"updates/{optimized_name}"
        conn.execute('''
            UPDATE eventos_semana SET titulo_articulo=?, fecha_inicio_pub=?, fecha_fin_pub=?, nombre_evento=?, promotor=?, img_video_path=?, pais=?, ciudad=?, fecha_evento=?, bio_corta=?, texto_articulo=?, fb_link=?, ig_link=?
            WHERE id=?
        ''', (titulo_articulo, fecha_inicio_pub, fecha_fin_pub, nombre_evento, promotor, filename, pais, ciudad, fecha_evento, bio_corta, texto_articulo, fb_link, ig_link, id))
    else:
        conn.execute('''
            UPDATE eventos_semana SET titulo_articulo=?, fecha_inicio_pub=?, fecha_fin_pub=?, nombre_evento=?, promotor=?, pais=?, ciudad=?, fecha_evento=?, bio_corta=?, texto_articulo=?, fb_link=?, ig_link=?
            WHERE id=?
        ''', (titulo_articulo, fecha_inicio_pub, fecha_fin_pub, nombre_evento, promotor, pais, ciudad, fecha_evento, bio_corta, texto_articulo, fb_link, ig_link, id))
        
    conn.commit()
    conn.close()
    
    flash('Evento actualizado exitosamente.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/eventos/toggle/<int:id>', methods=['POST'])
def toggle_evento(id):
    if 'user_id' not in session: return jsonify({"success": False, "error": "Unauthorized"}), 403
    conn = get_db_connection()
    e = conn.execute("SELECT is_active FROM eventos_semana WHERE id = ?", (id,)).fetchone()
    if e:
        new_status = 0 if e['is_active'] == 1 else 1
        conn.execute("UPDATE eventos_semana SET is_active = ? WHERE id = ?", (new_status, id))
        conn.commit()
    conn.close()
    return jsonify({"success": True})

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
        section = request.form.get('section')
        short_desc = request.form.get('short_desc')
        full_desc = request.form.get('full_desc')
        yt_link = request.form.get('yt_link', '')
        sp_link = request.form.get('sp_link', '')
        ap_link = request.form.get('ap_link', '')
        pub_date = request.form.get('pub_date')
        author = request.form.get('author')
        
        # Opcional imagen nueva
        image = request.files.get('image')
        if image and image.filename:
            image_filename = optimize_and_save_image(image, app.config['UPLOAD_FOLDER'], prefix="content_")
            conn.execute('''
                UPDATE content_items SET section=?, title=?, short_desc=?, full_desc=?, image_filename=?, yt_link=?, sp_link=?, ap_link=?, created_at=?, author=? WHERE id=?
            ''', (section, title, short_desc, full_desc, image_filename, yt_link, sp_link, ap_link, pub_date, author, id))
        else:
            conn.execute('''
                UPDATE content_items SET section=?, title=?, short_desc=?, full_desc=?, yt_link=?, sp_link=?, ap_link=?, created_at=?, author=? WHERE id=?
            ''', (section, title, short_desc, full_desc, yt_link, sp_link, ap_link, pub_date, author, id))
        
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
            band = ''
            song_or_album = og_title

            # Spotify track: "Song Name - song and lyrics by Band Name | Spotify"
            # Spotify album: "Album Name - Album by Band Name | Spotify"
            if ' by ' in og_title:
                parts = og_title.split(' by ')
                song_or_album = parts[0].replace(' - song and lyrics', '').replace(' - song', '').replace(' - Album', '').replace(' - Single', '').replace(' - EP', '').strip()
                band = parts[1].split('|')[0].replace('on Apple Music', '').strip()
            elif ' - ' in og_title:
                # Fallback splitting by dash if no " by "
                parts = og_title.split(' - ')
                if len(parts) >= 2:
                    song_or_album = parts[0].strip()
                    band = parts[1].split('|')[0].strip()

            return jsonify({'title': song_or_album, 'band': band})
            
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
    
    try:
        conn = get_db_connection()
        # Fetch existing agenda items to know which to keep and preserve their IDs
        # Key should include city to avoid overwriting duplicates like Megadeth CDMX vs Monterrey
        existing_rows = conn.execute("SELECT id, title, short_desc FROM content_items WHERE section = 'Agenda Metalera'").fetchall()
        existing_agenda = {f"{r['title'].lower()}|{r['short_desc'].split('|')[-1].strip().lower()}": r['id'] for r in existing_rows}
        seen_ids = set()

        def process_sheet(url, year):
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req) as response:
                    csv_data = response.read().decode('utf-8')
                    
                if "html" in csv_data[:100].lower() or "google" in csv_data[:100].lower():
                    return False
                    
                reader = csv.DictReader(io.StringIO(csv_data))
                months_map = {'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12, 'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4}
                
                for row in reader:
                    if 'Evento' not in row or not row['Evento'].strip(): continue
                    evento = row['Evento'].strip()
                    evento_lower = evento.lower()
                    ciudad = row.get('Ciudad', '').strip()
                    venue = row.get('Venue', '').strip()
                    fecha_raw = row.get('Fecha', '').strip()
                    gp = row.get('GP', 'N').strip()
                    tickets = row.get('Tickets', '').strip()
                    
                    month = 12
                    for m_name, m_num in months_map.items():
                        if m_name in fecha_raw.lower():
                            month = m_num
                            break
                            
                    day_match = re.search(r'\d+', fecha_raw)
                    day = int(day_match.group(0)) if day_match else 1
                    sort_date = f"{year}-{month:02d}-{day:02d}"
                    logo_filename = f"assets/logos/{evento.lower().replace(' ', '').replace('/', '')}.png"
                    
                    key = f"{evento_lower}|{ciudad.lower()}"
                    
                    if key in existing_agenda:
                        item_id = existing_agenda[key]
                        seen_ids.add(item_id)
                        conn.execute('''
                            UPDATE content_items SET title=?, short_desc=?, full_desc=?, image_filename=?, yt_link=?, sp_link=?, author=? WHERE id=?
                        ''', (evento, f"{venue} | {ciudad}", fecha_raw, logo_filename, gp, tickets, sort_date, item_id))
                    else:
                        cursor = conn.execute('''
                            INSERT INTO content_items (section, title, short_desc, full_desc, image_filename, yt_link, sp_link, author)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        ''', ("Agenda Metalera", evento, f"{venue} | {ciudad}", fecha_raw, logo_filename, gp, tickets, sort_date))
                        seen_ids.add(cursor.lastrowid)
                return True
            except Exception as e:
                print(f"Error processing sheet {year}:", e)
                return False

        success_2026 = process_sheet("https://docs.google.com/spreadsheets/d/1FTb-EzMtCGoxb0tAjoVQtTTeGJFd6qCP/export?format=csv&gid=2129987380", 2026)
        success_2027 = process_sheet("https://docs.google.com/spreadsheets/d/1FTb-EzMtCGoxb0tAjoVQtTTeGJFd6qCP/export?format=csv&gid=1993250078", 2027)
        
        if not success_2026 and not success_2027:
            flash('Error: El Google Sheet es PRIVADO o hubo un error de conexión.', 'error')
            conn.close()
            return redirect(url_for('admin_dashboard'))

        # Delete any items that were removed from BOTH Google Sheets
        for key, item_id in existing_agenda.items():
            if item_id not in seen_ids:
                conn.execute("DELETE FROM content_items WHERE id=?", (item_id,))
        
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
