from flask import Flask, send_from_directory, request, session, redirect, url_for, render_template, flash, jsonify
import sqlite3
import os
import random
import string
import smtplib
import threading
import datetime
from datetime import timedelta

MEXICO_TZ = datetime.timezone(datetime.timedelta(hours=-6))

def get_mexico_now():
    """Retorna datetime actual en zona horaria de Mexico (UTC-6)."""
    return datetime.datetime.now(MEXICO_TZ)

def get_mexico_now_str():
    """Retorna fecha y hora actual formateada como YYYY-MM-DD HH:MM:SS en hora de Mexico."""
    return get_mexico_now().strftime("%Y-%m-%d %H:%M:%S")

def get_mexico_today_str():
    """Retorna la fecha actual como YYYY-MM-DD en hora de Mexico."""
    return get_mexico_now().strftime("%Y-%m-%d")

def is_ajax_request(req):
    """Detecta si la peticion HTTP espera una respuesta JSON (AJAX / fetch / API)."""
    if not req: return False
    accept = req.headers.get('Accept', '')
    x_requested_with = req.headers.get('X-Requested-With', '')
    return (
        req.is_json or 
        'application/json' in accept or 
        x_requested_with == 'XMLHttpRequest' or
        req.args.get('format') == 'json'
    )

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import email.utils
from email.header import Header
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
            # Encontrar el índice donde empiezan las "Fuentes Consultadas"
            fuentes_idx = len(paragraphs)
            for i, p in enumerate(paragraphs):
                if "fuentes consultadas" in p.lower():
                    fuentes_idx = i
                    break
            
            # Solo intercalamos imágenes en los párrafos ANTES de las fuentes
            paragraphs_for_images = paragraphs[:fuentes_idx]
            paragraphs_after = paragraphs[fuentes_idx:]
            
            new_paragraphs = []
            img_idx = 0
            
            if len(paragraphs_for_images) > 0:
                gap_count = max(1, len(paragraphs_for_images) - 1)
                gap_step = max(1, gap_count // len(unused_list))
                
                for i, p in enumerate(paragraphs_for_images):
                    new_paragraphs.append(p)
                    # No añadimos imagen si estamos en el último párrafo antes de las fuentes, para evitar que flote a un lado
                    if i < len(paragraphs_for_images) - 1 and img_idx < len(unused_list) and (i + 1) % gap_step == 0:
                        img = unused_list[img_idx]
                        img_path = img if img.startswith('http') or img.startswith('assets') else 'updates/' + img
                        
                        float_dir = "right" if img_idx % 2 == 0 else "left"
                        margin_dir = "margin: 10px 0px 10px 20px;" if float_dir == "right" else "margin: 10px 20px 10px 0px;"
                        
                        img_html = f'<img loading="lazy" src="{img_path}" style="float: {float_dir}; width: 45%; max-width: 350px; {margin_dir} border-radius: 8px; border: 1px solid #333;" alt="Imagen de artículo">'
                        new_paragraphs.append(img_html)
                        
                        original_idx = images.index(img)
                        used_indices.add(original_idx)
                        img_idx += 1
                        
            # Añadimos clear both antes de las fuentes para asegurar que no haya solapamiento
            if paragraphs_after:
                new_paragraphs.append('<div style="clear: both; padding-top: 20px;"></div>')
            new_paragraphs.extend(paragraphs_after)
            
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
            'bio_larga', 'is_active', 'fecha_inicio', 'fecha_fin', 'updated_at'
        ]
        
        for col in required_columns:
            if col not in columns:
                if col == 'is_active':
                    cursor.execute(f"ALTER TABLE banda_semana ADD COLUMN {col} INTEGER DEFAULT 1")
                elif col == 'updated_at':
                    cursor.execute(f"ALTER TABLE banda_semana ADD COLUMN {col} TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
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
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
                created_at TIMESTAMP DEFAULT (datetime('now', '-6 hours'))
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

    # Auto-migrate and sanitize performance_analytics
    try:
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(performance_analytics)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'section_times' not in columns:
            cursor.execute("ALTER TABLE performance_analytics ADD COLUMN section_times TEXT DEFAULT '{}'")
        # Sanitize inflated historical session times (cap at 300s if distorted)
        cursor.execute("UPDATE performance_analytics SET time_on_page = 300 WHERE time_on_page > 600")
        # Normalize Mexico / Unknown to México in Spanish
        cursor.execute("UPDATE performance_analytics SET country = 'México' WHERE country IN ('Mexico', 'Unknown', 'Detecting', 'Desconocido', '')")
        conn.commit()
    except Exception as e_perf:
        print("Schema migration/cleanup error (performance_analytics):", e_perf)

    # Auto-adjust existing UTC timestamps in newsletter_subscribers if they were stored in UTC
    try:
        cursor = conn.cursor()
        mexico_now_check = get_mexico_now_str()
        cursor.execute("""
            UPDATE newsletter_subscribers 
            SET created_at = datetime(created_at, '-6 hours') 
            WHERE created_at > ?
        """, (mexico_now_check,))
        conn.commit()
    except Exception as e_time:
        pass

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
SENDER_PASSWORD = os.getenv('GMAIL_APP_PASSWORD') or "vywvezpzobnwurdd"

def send_goth_email(to_email, subject, html_content, text_content=None, reply_to="contacto@gothprods.com"):
    """
    Envio robusto y compatible con RFC/DKIM/SPF para correos de Goth Productions.
    - Adjunta multipart/alternative (text/plain y text/html) para evitar filtros antispam (iCloud, Gmail, Outlook).
    - Agrega Message-ID, Date, X-Mailer, List-Unsubscribe y Reply-To con formato RFC 2822.
    - Soporta fallback multinivel: Gmail SSL (465) -> Gmail TLS (587) -> Hostinger SSL (465) -> Hostinger TLS (587).
    """
    to_email = (to_email or '').strip()
    if not to_email or '@' not in to_email:
        print(f"[ERROR] Correo de destino invalido: '{to_email}'")
        return False

    if not text_content:
        text_content = f"""¡Bienvenido! Ahora eres un Berserker.

Has recibido un comunicado oficial de Goth Productions.

- Portal Web: https://gothprods.com

Para cualquier duda o gestión de tu suscripción, contáctanos a: {reply_to}
GOTH PRODUCTIONS • MEDIO MEXICANO DE DIVULGACIÓN DEL GÉNERO MÁS FEROZ DEL PLANETA
"""

    using_hostinger = bool(os.getenv('MAIL_PASSWORD'))
    hostinger_server = os.getenv('MAIL_SERVER', 'smtp.hostinger.com')
    hostinger_user = os.getenv('MAIL_USERNAME', 'contacto@gothprods.com')
    hostinger_pass = os.getenv('MAIL_PASSWORD')

    gmail_server = "smtp.gmail.com"
    gmail_user = "goth.prods@gmail.com"
    gmail_pass = os.getenv('GMAIL_APP_PASSWORD') or "vywvezpzobnwurdd"

    def _build_mime(from_addr):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = email.utils.formataddr(("Goth Productions", from_addr))
        msg['To'] = to_email
        msg['Reply-To'] = reply_to
        msg['Date'] = email.utils.formatdate(localtime=True)
        if '@' in from_addr:
            msg_domain = from_addr.split('@')[-1]
            msg['Message-ID'] = email.utils.make_msgid(domain=msg_domain)
        else:
            msg['Message-ID'] = email.utils.make_msgid()
        msg['X-Mailer'] = 'GothProds Mailer/3.0'
        msg['List-Unsubscribe'] = f'<mailto:{reply_to}?subject=Unsubscribe>'
        msg.attach(MIMEText(text_content, 'plain', 'utf-8'))
        msg.attach(MIMEText(html_content, 'html', 'utf-8'))
        return msg

    attempts = []
    # Primary reliable SMTP: Gmail SSL (465) & TLS (587)
    if gmail_pass:
        attempts.append(('Gmail SSL:465', gmail_server, 465, gmail_user, gmail_pass, True))
        attempts.append(('Gmail TLS:587', gmail_server, 587, gmail_user, gmail_pass, False))

    # Secondary / Custom domain SMTP: Hostinger
    if using_hostinger and hostinger_pass:
        attempts.append(('Hostinger SSL:465', hostinger_server, 465, hostinger_user, hostinger_pass, True))
        attempts.append(('Hostinger TLS:587', hostinger_server, 587, hostinger_user, hostinger_pass, False))

    for label, s_host, s_port, s_user, s_pass, is_ssl in attempts:
        try:
            msg = _build_mime(s_user)
            if is_ssl:
                server = smtplib.SMTP_SSL(s_host, s_port, timeout=15)
            else:
                server = smtplib.SMTP(s_host, s_port, timeout=15)
                server.starttls()
            server.login(s_user, s_pass)
            server.sendmail(s_user, [to_email], msg.as_string())
            server.quit()
            print(f"[SUCCESS] Email sent to {to_email} via {label} ({s_host}:{s_port})")
            return True
        except Exception as e_att:
            print(f"[WARNING] SMTP attempt {label} failed for {to_email}: {e_att}")

    print(f"[ERROR] All SMTP delivery attempts failed for {to_email}")
    return False

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

# --- FRONTEND ANALYTICS ---
COUNTRY_CODE_MAP = {
    'MX': 'México', 'US': 'Estados Unidos', 'ES': 'España', 'CO': 'Colombia',
    'AR': 'Argentina', 'CL': 'Chile', 'PE': 'Perú', 'EC': 'Ecuador',
    'GT': 'Guatemala', 'CR': 'Costa Rica', 'PA': 'Panamá', 'DE': 'Alemania',
    'FR': 'Francia', 'GB': 'Reino Unido', 'CA': 'Canadá', 'BR': 'Brasil',
    'IT': 'Italia', 'SE': 'Suecia', 'NO': 'Noruega', 'FI': 'Finlandia',
    'UY': 'Uruguay', 'BO': 'Bolivia', 'PY': 'Paraguay', 'VE': 'Venezuela',
    'SV': 'El Salvador', 'HN': 'Honduras', 'NI': 'Nicaragua', 'DO': 'República Dominicana',
    'PR': 'Puerto Rico'
}

@app.route('/api/analytics/init', methods=['POST'])
def init_analytics():
    data = request.get_json(force=True, silent=True)
    if not data and request.data:
        try:
            import json
            data = json.loads(request.data.decode('utf-8'))
        except Exception:
            data = {}
    data = data or {}

    session_id = data.get('session_id')
    user_id = data.get('user_id')
    page_url = data.get('page_url')
    device_type = data.get('device_type')
    country = data.get('country', '').strip()
    referrer = data.get('referrer')
    is_new_user = 1 if data.get('is_new_user') else 0
    
    # Check headers for Cloudflare / proxy country code
    cf_country = request.headers.get('CF-IPCountry') or request.headers.get('X-Country-Code') or request.headers.get('X-Appengine-Country')
    if cf_country and cf_country.upper() in COUNTRY_CODE_MAP:
        country = COUNTRY_CODE_MAP[cf_country.upper()]
    elif cf_country and cf_country not in ('XX', 'T1', 'ZZ'):
        country = cf_country

    if country == 'Mexico':
        country = 'México'

    if not country or country in ('Unknown', 'Detecting', 'Desconocido', ''):
        client_ip = request.headers.get('CF-Connecting-IP') or \
                    request.headers.get('X-Real-IP') or \
                    request.headers.get('X-Forwarded-For', request.remote_addr)
        if client_ip:
            client_ip = client_ip.split(',')[0].strip()
            if client_ip not in ('127.0.0.1', '::1', 'localhost'):
                try:
                    import urllib.request, json
                    req = urllib.request.Request(f'http://ip-api.com/json/{client_ip}', headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req, timeout=1.5) as response:
                        ip_data = json.loads(response.read().decode())
                        if ip_data.get('status') == 'success':
                            raw_c = ip_data.get('country', 'México')
                            country = 'México' if raw_c == 'Mexico' else raw_c
                except Exception:
                    country = 'México'
            else:
                country = 'México'
        else:
            country = 'México'

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
    
    return jsonify({"success": True, "record_id": record_id, "country": country})

@app.route('/api/analytics/update', methods=['POST'])
def update_analytics():
    data = request.get_json(force=True, silent=True)
    if not data and request.data:
        try:
            import json
            data = json.loads(request.data.decode('utf-8'))
        except Exception:
            data = {}
    data = data or {}

    record_id = data.get('record_id')
    scroll_depth = int(data.get('scroll_depth', 0) or 0)
    time_on_page = int(data.get('time_on_page', 0) or 0)
    time_on_page = min(max(time_on_page, 0), 600) # Cap at 10 min to avoid corrupted or abandoned tabs
    section_times = data.get('section_times', {})
    country = data.get('country', '').strip()
    if country == 'Mexico':
        country = 'México'
    
    if not record_id:
        return jsonify({"success": False}), 400
        
    conn = get_db_connection(live=True)
    cursor = conn.cursor()
    
    import json
    # Filter and cap section times
    clean_section_times = {}
    if isinstance(section_times, dict):
        for sec, t in section_times.items():
            try:
                clean_section_times[str(sec)] = min(max(int(t), 0), 600)
            except Exception:
                pass
    section_times_str = json.dumps(clean_section_times)
    
    if country and country not in ('Unknown', 'Detecting', 'Desconocido', ''):
        cursor.execute('''
            UPDATE performance_analytics 
            SET scroll_depth = MIN(MAX(scroll_depth, ?), 100), 
                time_on_page = MIN(MAX(time_on_page, ?), 600), 
                section_times = ?,
                country = CASE WHEN country IN ('Detecting', 'Unknown', 'Desconocido', '', 'Mexico') THEN ? ELSE country END
            WHERE id = ?
        ''', (scroll_depth, time_on_page, section_times_str, country, record_id))
    else:
        cursor.execute('''
            UPDATE performance_analytics 
            SET scroll_depth = MIN(MAX(scroll_depth, ?), 100), 
                time_on_page = MIN(MAX(time_on_page, ?), 600), 
                section_times = ?
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

    radar_items = []
    seen_bands = set()
    
    # Query for the latest Banda de la Semana
    raw_bandas = conn.execute("SELECT * FROM banda_semana ORDER BY id DESC").fetchall()
    for b in raw_bandas:
        b = dict(b) # Convert sqlite3.Row to dict to add new keys
        is_active = b.get('is_active', 1)
        fecha_inicio = b.get('fecha_inicio')
        fecha_fin = b.get('fecha_fin')
        
        in_date_range = True
        if fecha_fin and current_date > fecha_fin:
            in_date_range = False
        if not is_preview:
            if fecha_inicio and current_date < fecha_inicio:
                in_date_range = False
            
        if is_active == 1 and in_date_range and b['nombre'] not in seen_bands:
            seen_bands.add(b['nombre'])
            b['radar_type'] = 'banda'
            b['sort_date'] = fecha_inicio or "1970-01-01"
            radar_items.append(b)
                
    # Query for Eventos de la Semana
    raw_eventos = conn.execute("SELECT * FROM eventos_semana ORDER BY id DESC").fetchall()
    for e in raw_eventos:
        e = dict(e)
        is_active = e.get('is_active', 1)
        fecha_inicio = e.get('fecha_inicio_pub')
        fecha_fin = e.get('fecha_fin_pub')
        
        in_date_range = True
        if fecha_fin and current_date > fecha_fin:
            in_date_range = False
        if not is_preview:
            if fecha_inicio and current_date < fecha_inicio:
                in_date_range = False
            
        if is_active == 1 and in_date_range:
            e['radar_type'] = 'evento'
            e['sort_date'] = fecha_inicio or "1970-01-01"
            radar_items.append(e)
    
    # Query for Colectivo Mexapedia (Latest active)
    mexapedia_record = conn.execute("SELECT * FROM colectivo_mexapedia WHERE is_active = 1 ORDER BY id DESC LIMIT 1").fetchone()
    if mexapedia_record:
        m = dict(mexapedia_record)
        m['radar_type'] = 'mexapedia'
        m['sort_date'] = "2099-12-31" # Always first? Or maybe use current date so it mixes in? Actually, the prompt says 5 eventos o/y bandas. Mexapedia is separate or included? Let's give it the current date.
        m['sort_date'] = current_date
        # Wait, the user said "5 eventos o/y bandas". Let's let Mexapedia be handled separately in the template as it was, to not break its logic, OR put it in radar_items. 
        # The template has a separate block for Mexapedia at the end. Let's keep Mexapedia separate.
        pass

    # Sort all radar items descending by updated_at or created_at (most recently posted first)
    radar_items.sort(key=lambda x: (x.get('updated_at') or x.get('created_at') or x['sort_date'], x['id']), reverse=True)
    
    # Limit to 15 items so there is enough content to scroll through
    radar_items = radar_items[:15]
    
    # Re-extract the lists for the modals to use
    bandas_semana = [item for item in radar_items if item.get('radar_type') == 'banda']
    eventos_semana = [item for item in radar_items if item.get('radar_type') == 'evento']
    
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
                           radar_items=radar_items,
                           bandas_semana=bandas_semana,
                           eventos_semana=eventos_semana,
                           mexapedia_record=mexapedia_record, is_preview=is_preview)

@app.route('/banda/<int:id>')
@app.route('/banda/<int:id>-<string:slug>')
def view_banda(id, slug=None):
    is_preview = request.args.get('preview') == '1'
    conn = get_db_connection(live=not is_preview)
    if not is_preview:
        conn.execute("UPDATE banda_semana SET views = COALESCE(views, 0) + 1 WHERE id = ?", (id,))
        conn.commit()
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
    if not is_preview:
        conn.execute("UPDATE eventos_semana SET views = COALESCE(views, 0) + 1 WHERE id = ?", (id,))
        conn.commit()
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
    if not is_preview:
        conn.execute("UPDATE content_items SET views = COALESCE(views, 0) + 1 WHERE id = ?", (id,))
        conn.commit()
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
    
    perf_query = "SELECT * FROM performance_analytics WHERE page_url NOT LIKE '%/admin%'"
    perf_params = []
    
    if perf_range == '7':
        perf_query += " AND created_at >= datetime('now', '-7 days')"
    elif perf_range == '30':
        perf_query += " AND created_at >= datetime('now', '-30 days')"
    elif perf_range == '90':
        perf_query += " AND created_at >= datetime('now', '-90 days')"
    elif perf_range == 'custom' and perf_start and perf_end:
        perf_query += " AND created_at >= ? AND created_at <= ?"
        perf_params = [perf_start + ' 00:00:00', perf_end + ' 23:59:59']
        
    perf_query += " ORDER BY id DESC"
    
    analytics_rows = conn_live.execute(perf_query, perf_params).fetchall()
    
    interactions_query = '''
    SELECT id, section, title, COALESCE(views, 0) as views, COALESCE(likes, 0) as likes, 
           (SELECT COUNT(*) FROM comments WHERE item_id = content_items.id AND item_type = 'content') as comments_count,
           created_at, 'content' as item_type
    FROM content_items 
    
    UNION ALL
    
    SELECT id, 'Banda de la Semana' as section, nombre as title, COALESCE(views, 0) as views, COALESCE(likes, 0) as likes,
           (SELECT COUNT(*) FROM comments WHERE item_id = banda_semana.id AND item_type = 'banda') as comments_count,
           created_at, 'banda' as item_type
    FROM banda_semana
    
    UNION ALL
    
    SELECT id, 'Agenda Metalera' as section, titulo_articulo as title, COALESCE(views, 0) as views, COALESCE(likes, 0) as likes,
           (SELECT COUNT(*) FROM comments WHERE item_id = eventos_semana.id AND item_type = 'evento') as comments_count,
           created_at, 'evento' as item_type
    FROM eventos_semana
    
    UNION ALL
    
    SELECT id, 'Colectivo Mexapedia' as section, titulo as title, 0 as views, 0 as likes,
           0 as comments_count,
           created_at, 'mexapedia' as item_type
    FROM colectivo_mexapedia
    
    ORDER BY id DESC, created_at DESC
    '''
    interactions_rows = conn.execute(interactions_query).fetchall()
    
    conn_live.close()
    
    analytics_data = [dict(row) for row in analytics_rows]
    interactions_data = [dict(row) for row in interactions_rows]
    # Cargar suscriptores de Newsletter (todos, ordenados por los mas recientes)
    suscriptores = conn.execute("SELECT * FROM newsletter_subscribers WHERE is_active >= 0 ORDER BY id DESC").fetchall()

    conn.close()

    return render_template('admin_dashboard.html', all_items=all_items, settings=get_settings(), todas_bandas=todas_bandas, todos_eventos=todos_eventos, todos_mexapedia=todos_mexapedia, all_users=all_users, analytics_data=analytics_data, interactions_data=interactions_data, suscriptores=suscriptores)

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
    
    file_keys = ['hero_bg', 'header_logo', 'icon_home', 'galeria_bg', 'metalpulse_bg', 
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
            
    temp_live_file = DB_LIVE_FILE + ".tmp"
    shutil.copyfile(DB_FILE, temp_live_file)
    os.replace(temp_live_file, DB_LIVE_FILE)
    
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
    temp_file = DB_FILE + ".tmp"
    shutil.copyfile(DB_LIVE_FILE, temp_file)
    os.replace(temp_file, DB_FILE)
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
    
    if not nombre.strip():
        flash('El nombre de la banda es obligatorio.', 'error')
        return redirect(url_for('admin_dashboard'))
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
            UPDATE banda_semana SET nombre=?, pais=?, ciudad=?, bio_corta=?, img_video_path=?, ig_link=?, fb_link=?, tk_link=?, sp_link=?, ap_link=?, yt_link=?, ano_formacion=?, line_up=?, titulo_resena=?, texto_resena=?, discografia=?, ultimo_lanzamiento_titulo=?, ultimo_lanzamiento_tipo=?, ultimo_lanzamiento_sp_link=?, ultimo_lanzamiento_ap_link=?, fecha_inicio=?, fecha_fin=?, updated_at=CURRENT_TIMESTAMP
            WHERE id=?
        ''', (nombre, pais, ciudad, bio_corta, filename, ig_link, fb_link, tk_link, sp_link, ap_link, yt_link, ano_formacion, line_up, titulo_resena, texto_resena, discografia, ultimo_lanzamiento_titulo, ultimo_lanzamiento_tipo, ultimo_lanzamiento_sp_link, ultimo_lanzamiento_ap_link, fecha_inicio, fecha_fin, id))
    else:
        conn.execute('''
            UPDATE banda_semana SET nombre=?, pais=?, ciudad=?, bio_corta=?, ig_link=?, fb_link=?, tk_link=?, sp_link=?, ap_link=?, yt_link=?, ano_formacion=?, line_up=?, titulo_resena=?, texto_resena=?, discografia=?, ultimo_lanzamiento_titulo=?, ultimo_lanzamiento_tipo=?, ultimo_lanzamiento_sp_link=?, ultimo_lanzamiento_ap_link=?, fecha_inicio=?, fecha_fin=?, updated_at=CURRENT_TIMESTAMP
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
        conn.execute("UPDATE banda_semana SET is_active = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (new_status, id))
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
    
    if not nombre_evento.strip() or not titulo_articulo.strip():
        flash('El título y el nombre del evento son obligatorios.', 'error')
        return redirect(url_for('admin_dashboard'))
    
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
            UPDATE eventos_semana SET titulo_articulo=?, fecha_inicio_pub=?, fecha_fin_pub=?, nombre_evento=?, promotor=?, img_video_path=?, pais=?, ciudad=?, fecha_evento=?, bio_corta=?, texto_articulo=?, fb_link=?, ig_link=?, updated_at=CURRENT_TIMESTAMP
            WHERE id=?
        ''', (titulo_articulo, fecha_inicio_pub, fecha_fin_pub, nombre_evento, promotor, filename, pais, ciudad, fecha_evento, bio_corta, texto_articulo, fb_link, ig_link, id))
    else:
        conn.execute('''
            UPDATE eventos_semana SET titulo_articulo=?, fecha_inicio_pub=?, fecha_fin_pub=?, nombre_evento=?, promotor=?, pais=?, ciudad=?, fecha_evento=?, bio_corta=?, texto_articulo=?, fb_link=?, ig_link=?, updated_at=CURRENT_TIMESTAMP
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
        conn.execute("UPDATE eventos_semana SET is_active = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (new_status, id))
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

# --- RUTAS DE NEWSLETTER ---

def build_welcome_email_html(nombre="Berserker"):
    """Genera el HTML para el correo de bienvenida de GothProds con fondo negro y estilo Berserker a prueba de clientes de correo."""
    display_name = nombre.strip() if nombre and nombre.strip() else "Berserker"
    logo_url = "https://gothprods.com/assets/logo.png"

    return f"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="es">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="color-scheme" content="light dark" />
    <meta name="supported-color-schemes" content="light dark" />
    <title>Bienvenido a GothProds</title>
    <style type="text/css">
        :root {{
            color-scheme: dark;
            supported-color-schemes: dark;
        }}
        body, table, td, p, a, span, h1, h2, h3 {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
            -webkit-font-smoothing: antialiased;
        }}
        body {{
            background-color: #000000 !important;
            margin: 0 !important;
            padding: 0 !important;
            width: 100% !important;
            min-width: 100% !important;
            color: #ffffff !important;
        }}
        @media (prefers-color-scheme: light) {{
            .darkmode-bg {{ background-color: #000000 !important; }}
            .darkmode-card {{ background-color: #080808 !important; }}
            .darkmode-inner {{ background-color: #0d0d0d !important; }}
            .darkmode-text {{ color: #ffffff !important; }}
            .darkmode-title {{ color: #716d4a !important; }}
        }}
        @media (prefers-color-scheme: dark) {{
            .darkmode-bg {{ background-color: #000000 !important; }}
            .darkmode-card {{ background-color: #080808 !important; }}
            .darkmode-inner {{ background-color: #0d0d0d !important; }}
            .darkmode-text {{ color: #ffffff !important; }}
            .darkmode-title {{ color: #716d4a !important; }}
        }}
    </style>
</head>
<body bgcolor="#000000" class="darkmode-bg" style="margin: 0; padding: 0; background-color: #000000 !important; background: #000000 !important; color: #ffffff !important; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%;">
    <!-- WRAPPER TABLE -->
    <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#000000" class="darkmode-bg" style="width: 100% !important; background-color: #000000 !important; background: #000000 !important; margin: 0; padding: 25px 10px;">
        <tr>
            <td align="center" bgcolor="#000000" class="darkmode-bg" style="background-color: #000000 !important; padding: 0;">
                <!-- MAIN CARD -->
                <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#080808" class="darkmode-card" style="max-width: 620px; width: 100% !important; background-color: #080808 !important; background: #080808 !important; border: 1px solid #716d4a; border-radius: 8px; overflow: hidden;">
                    
                    <!-- HEADER -->
                    <tr>
                        <td align="center" bgcolor="#000000" style="background-color: #000000 !important; background: #000000 !important; padding: 32px 20px 24px 20px; border-bottom: 2px solid #716d4a;">
                            <a href="https://gothprods.com" target="_blank" style="text-decoration: none; display: block;">
                                <img src="{logo_url}" width="190" alt="GOTH PRODUCTIONS" style="display: block; width: 190px; max-width: 190px; height: auto; margin: 0 auto 12px auto; border: 0;" />
                                <h1 class="darkmode-title" style="color: #716d4a !important; font-size: 24px; font-weight: 900; letter-spacing: 2px; text-transform: uppercase; margin: 0 0 10px 0; line-height: 1.2;">
                                    GOTH PRODUCTIONS
                                </h1>
                            </a>
                            <div style="margin-top: 8px;">
                                <table role="presentation" border="0" cellspacing="0" cellpadding="0" align="center">
                                    <tr>
                                        <td bgcolor="#716d4a" style="background-color: #716d4a !important; border-radius: 4px; padding: 5px 14px;">
                                            <span style="color: #ffffff !important; font-size: 11px; font-weight: bold; letter-spacing: 1.5px; text-transform: uppercase; display: inline-block;">
                                                ⚔️ PACTO OFICIAL CONFIRMADO ⚔️
                                            </span>
                                        </td>
                                    </tr>
                                </table>
                            </div>
                        </td>
                    </tr>

                    <!-- CONTENT BODY -->
                    <tr>
                        <td bgcolor="#080808" class="darkmode-card" style="background-color: #080808 !important; background: #080808 !important; padding: 30px 25px 20px 25px;">
                            <h2 class="darkmode-title" style="color: #716d4a !important; font-size: 20px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; margin: 0 0 16px 0; line-height: 1.3;">
                                ¡Bienvenido, {display_name}! Ahora eres un Berserker
                            </h2>
                            <p class="darkmode-text" style="color: #ffffff !important; font-size: 14px; line-height: 1.6; margin: 0 0 14px 0;">
                                Tu suscripción ha sido confirmada exitosamente. A partir de este momento formas parte de <strong style="color: #ffffff !important;">GothProds</strong>.
                            </p>
                            <p class="darkmode-text" style="color: #ffffff !important; font-size: 14px; line-height: 1.6; margin: 0 0 18px 0;">
                                Como Berserker oficial de Goth Productions, recibirás en tu correo:
                            </p>

                            <!-- BENEFICIOS BOX -->
                            <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#0d0d0d" class="darkmode-inner" style="background-color: #0d0d0d !important; background: #0d0d0d !important; border: 1px solid #716d4a; border-radius: 6px; margin-bottom: 24px;">
                                <tr>
                                    <td bgcolor="#0d0d0d" class="darkmode-inner" style="background-color: #0d0d0d !important; background: #0d0d0d !important; padding: 16px 18px; color: #ffffff !important;">
                                        <div style="color: #ffffff !important; font-size: 13px; line-height: 1.8;">
                                            <span style="color: #716d4a !important; font-weight: bold;">• El Noticiero Nocturno:</span> <span style="color: #ffffff !important;">Novedades, lanzamientos y coberturas de la escena underground.</span><br />
                                            <span style="color: #716d4a !important; font-weight: bold;">• Agenda Metalera:</span> <span style="color: #ffffff !important;">Cartelera mensual anticipada con los mejores conciertos y festivales.</span><br />
                                            <span style="color: #716d4a !important; font-weight: bold;">• Reseñas & Entrevistas:</span> <span style="color: #ffffff !important;">Críticas de álbumes y entrevistas exclusivas con las bandas más brutales.</span><br />
                                            <span style="color: #716d4a !important; font-weight: bold;">• Metal Pulse & Galería:</span> <span style="color: #ffffff !important;">Lo mejor de nuestros playlists de Spotify y producciones audiovisuales.</span>
                                        </div>
                                    </td>
                                </tr>
                            </table>

                            <!-- CTA BUTTON -->
                            <table role="presentation" border="0" cellspacing="0" cellpadding="0" align="center" style="margin: 25px auto 15px auto;">
                                <tr>
                                    <td align="center" bgcolor="#716d4a" style="background-color: #716d4a !important; border-radius: 4px; padding: 13px 28px;">
                                        <a href="https://gothprods.com" target="_blank" style="color: #ffffff !important; font-size: 14px; font-weight: bold; text-decoration: none; text-transform: uppercase; letter-spacing: 1px; display: inline-block;">
                                            EXPLORAR GOTHPRODS.COM &rarr;
                                        </a>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>

                    <!-- FOOTER -->
                    <tr>
                        <td align="center" bgcolor="#000000" style="background-color: #000000 !important; background: #000000 !important; border-top: 1px solid #716d4a; padding: 22px 20px; text-align: center;">
                            <p class="darkmode-title" style="color: #716d4a !important; font-size: 12px; font-weight: bold; letter-spacing: 1px; text-transform: uppercase; margin: 0 0 8px 0;">
                                GOTH PRODUCTIONS &bull; MEDIO MEXICANO DE DIVULGACIÓN DEL GÉNERO MÁS FEROZ DEL PLANETA
                            </p>
                            <p style="color: #777777 !important; font-size: 11px; margin: 0; line-height: 1.4;">
                                Has recibido este correo porque te registraste en nuestra comunidad de Berserkers. Si deseas gestionar tu suscripción, contáctanos a <a href="mailto:contacto@gothprods.com" style="color: #716d4a !important; text-decoration: none;">contacto@gothprods.com</a>.
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>"""


def send_newsletter_welcome_email(to_email, nombre="Berserker"):
    """Envía un correo de confirmación y bienvenida con branding oficial de GothProds de manera síncrona y robusta."""
    try:
        display_name = nombre.strip() if nombre and nombre.strip() else "Berserker"
        subject = f"⚔️ ¡Bienvenido a GothProds, {display_name}! Ahora eres un Berserker ⚔️"
        html_body = build_welcome_email_html(nombre=display_name)
        text_body = f"""¡Bienvenido, {display_name}! Ahora eres un Berserker.

Tu suscripción a Goth Productions ha sido confirmada con éxito.

- Portal Web Oficial: https://gothprods.com

Para cualquier duda o gestión de tu suscripción, contáctanos a: contacto@gothprods.com
GOTH PRODUCTIONS • MEDIO MEXICANO DE DIVULGACIÓN DEL GÉNERO MÁS FEROZ DEL PLANETA
"""
        success = send_goth_email(to_email, subject, html_body, text_body)
        if success:
            print(f"[SUCCESS] Welcome email delivered to {to_email} ({display_name})")
        else:
            print(f"[ERROR] Failed to deliver welcome email to {to_email}")
        return success
    except Exception as e:
        print(f"[EXCEPTION] Could not send welcome email to {to_email}: {e}")
        return False


@app.route('/subscribe_newsletter', methods=['POST'])
def subscribe_newsletter():
    data = request.get_json() or {}
    nombre = data.get('nombre', '').strip()
    email = data.get('email', '').strip().lower()

    if not email or '@' not in email:
        return jsonify({'success': False, 'message': 'Por favor ingresa un correo electrónico válido.'})

    conn = get_db_connection()
    try:
        cur = conn.execute("SELECT id, is_active, nombre FROM newsletter_subscribers WHERE email = ?", (email,))
        existing = cur.fetchone()
        if existing:
            active_name = existing['nombre'] if existing['nombre'] and existing['nombre'] != 'Berserker' else (nombre or 'Berserker')
            if existing['is_active'] == 1:
                conn.close()
                # threading.Thread(target=send_newsletter_welcome_email, args=(email, active_name)).start()
                nombre_text = f", {active_name}" if active_name and active_name != 'Berserker' else ""
                return jsonify({
                    'success': True,
                    'is_existing': True,
                    'message': f'¡Bienvenido! Ahora eres un Berserker{nombre_text}. Te enviaremos un correo de bienvenida oficial.'
                })
            else:
                conn.execute("UPDATE newsletter_subscribers SET is_active = 1, nombre = ? WHERE id = ?", (active_name, existing['id']))
                conn.commit()
                conn.close()
                # threading.Thread(target=send_newsletter_welcome_email, args=(email, active_name)).start()
                return jsonify({
                    'success': True,
                    'is_existing': False,
                    'message': '¡Tu suscripción ha sido reactivada exitosamente! Te enviaremos un correo de bienvenida oficial.'
                })
        
        conn.execute("INSERT INTO newsletter_subscribers (nombre, email, created_at) VALUES (?, ?, ?)", (nombre or 'Berserker', email, get_mexico_now_str()))
        conn.commit()
        conn.close()
        
        # threading.Thread(target=send_newsletter_welcome_email, args=(email, nombre or 'Berserker')).start()

        nombre_saludo = f", {nombre}" if nombre else ""
        return jsonify({
            'success': True,
            'is_existing': False,
            'message': f'¡Bienvenido! Ahora eres un Berserker{nombre_saludo}. Te has suscrito exitosamente. Te enviaremos un correo de bienvenida oficial.'
        })
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': 'Hubo un inconveniente al procesar tu registro. Por favor intenta más tarde.'})


def build_newsletter_html(asunto, mensaje_intro, target_month="2026-07", live=False, base_url_override=None):
    """Genera el HTML del boletín mensual con tablas compatibles con clientes de correo y fondo negro obligatorio."""
    conn = get_db_connection(live=live)
    import datetime, re
    mexico_tz = datetime.timezone(datetime.timedelta(hours=-6))
    now_mx = datetime.datetime.now(mexico_tz)
    base_url = base_url_override if base_url_override else "https://gothprods.com"
    
    # Process target month
    month_names = {
        "01": "Enero", "02": "Febrero", "03": "Marzo", "04": "Abril",
        "05": "Mayo", "06": "Junio", "07": "Julio", "08": "Agosto",
        "09": "Septiembre", "10": "Octubre", "11": "Noviembre", "12": "Diciembre"
    }
    
    if not target_month or '-' not in target_month:
        target_month = "2026-07"
        
    parts = target_month.split('-')
    year_str = parts[0]
    month_str = parts[1]
    y = int(year_str)
    m = int(month_str)
    month_name = month_names.get(month_str, "Julio")
    month_label = f"{month_name} {year_str}"
    
    # Agenda metalera corresponde siempre al MES SIGUIENTE
    if m == 12:
        next_y = y + 1
        next_m = 1
    else:
        next_y = y
        next_m = m + 1
    next_month_str = f"{next_y:04d}-{next_m:02d}"
    next_month_name = month_names.get(f"{next_m:02d}", "Próximo Mes")
    next_month_label = f"{next_month_name} {next_y}"
    
    # 1. Bandas y Eventos (Radar del Caos & El Pit)
    bandas = conn.execute("SELECT * FROM banda_semana WHERE is_active = 1 AND created_at LIKE ? ORDER BY id DESC ", (f"{target_month}%",)).fetchall()
    eventos = conn.execute("SELECT * FROM eventos_semana WHERE is_active = 1 AND created_at LIKE ? ORDER BY id DESC ", (f"{target_month}%",)).fetchall()
    
    # 2. El Noticiero Nocturno (Filtrado por mes objetivo)
    noticiero = conn.execute("SELECT * FROM content_items WHERE section = 'El Noticiero Nocturno' AND created_at LIKE ? ORDER BY created_at DESC, id DESC", (f"{target_month}%",)).fetchall()
        
    # 3. Reseñas de Conciertos (Filtrado por mes objetivo)
    reseñas = conn.execute("SELECT * FROM content_items WHERE section = 'Reseñas de Conciertos' AND created_at LIKE ? ORDER BY created_at DESC, id DESC", (f"{target_month}%",)).fetchall()
        
    # 4. Entrevistas Under (Filtrado por mes objetivo)
    entrevistas = conn.execute("SELECT * FROM content_items WHERE section = 'Entrevistas Under' AND created_at LIKE ? ORDER BY created_at DESC, id DESC", (f"{target_month}%",)).fetchall()
        
    # 5. La Galería Nocturna & Caos Sonoro (Filtrado por mes objetivo)
    galeria = conn.execute("SELECT * FROM content_items WHERE section IN ('La Galería Nocturna', 'Caos Sonoro') AND created_at LIKE ? ORDER BY created_at DESC, id DESC", (f"{target_month}%",)).fetchall()
        
    # 6. Metal Pulse Tracks (Tomar la lista activa en la pagina)
    all_tracks = conn.execute("SELECT * FROM content_items WHERE section = 'Metal Pulse Tracks' AND full_desc != '.' ORDER BY id DESC").fetchall()
    settings_rows = conn.execute('SELECT key, value FROM settings').fetchall()
    settings = {row['key']: row['value'] for row in settings_rows}
    hide_past_mp = settings.get('hide_past_metalpulse', '0') == '1'
    if hide_past_mp and all_tracks:
        months_es = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        cur_year = now_mx.year
        cur_month_idx = now_mx.month - 1
        valid_months = set()
        for i in range(24):
            m_idx = (cur_month_idx + i) % 12
            y_i = cur_year + (cur_month_idx + i) // 12
            valid_months.add(f"{months_es[m_idx]} {y_i}")
        filtered = [t for t in all_tracks if t['full_desc'] in valid_months]
        if filtered:
            pulse_tracks = filtered
        else:
            latest_month = all_tracks[0]['full_desc']
            pulse_tracks = [t for t in all_tracks if t['full_desc'] == latest_month]
    else:
        pulse_tracks = all_tracks
        
    # 7. Agenda Metalera (Conciertos en el MES SIGUIENTE)
    agenda = conn.execute("SELECT * FROM content_items WHERE section = 'Agenda Metalera' AND author LIKE ? ORDER BY author ASC", (f"{next_month_str}%",)).fetchall()
            
    conn.close()

    def get_full_img_url(path, default_img="assets/logo.png", band_title=None, sec=None):
        if not path or str(path).strip() == '':
            if sec == 'Agenda Metalera':
                return f"{base_url}/assets/agenda_icon.png"
            return f"{base_url}/{default_img}"
            
        path_str = str(path).strip()
        
        # YouTube URLs
        if 'youtube.com' in path_str or 'youtu.be' in path_str or 'ytimg.com' in path_str:
            m = re.search(r"vi/([a-zA-Z0-9_-]+)", path_str)
            if m:
                return f"https://img.youtube.com/vi/{m.group(1)}/hqdefault.jpg"
            return path_str
            
        if path_str.startswith('http://') or path_str.startswith('https://'):
            return path_str
            
        clean_path = path_str.lstrip('/')
        if not clean_path.startswith('assets/') and not clean_path.startswith('updates/'):
            clean_path = f"updates/{clean_path}"
            
        if os.path.exists(clean_path):
            return f"{base_url}/{clean_path}"
            
        base, ext = os.path.splitext(clean_path)
        for alt_ext in ['.png', '.webp', '.jpg', '.jpeg']:
            alt_path = base + alt_ext
            if os.path.exists(alt_path):
                return f"{base_url}/{alt_path}"
                
        if band_title:
            title_clean = re.sub(r'[^a-zA-Z0-9]', '', band_title).lower()
            if os.path.exists('assets/logos'):
                for lf in os.listdir('assets/logos'):
                    lf_clean = re.sub(r'[^a-zA-Z0-9]', '', os.path.splitext(lf)[0]).lower()
                    if lf_clean and (lf_clean == title_clean or lf_clean in title_clean or title_clean in lf_clean):
                        return f"{base_url}/assets/logos/{lf}"
                        
        if sec == 'Agenda Metalera':
            return f"{base_url}/assets/agenda_icon.png"
        return f"{base_url}/{default_img}"

    # Tarjetas con estructura de tabla sólida a prueba de clientes de correo
    noticiero_cards = "".join([f"""
    <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#0d0d0d" class="darkmode-inner" style="background-color: #0d0d0d !important; border: 1px solid #716d4a; border-radius: 6px; overflow: hidden; margin-bottom: 10px;">
        <tr>
            <td width="110" valign="top" bgcolor="#0d0d0d" style="background-color: #0d0d0d !important; padding: 0;">
                <img src="{get_full_img_url(n['image_filename'], band_title=n['title'], sec='El Noticiero Nocturno')}" alt="{n['title']}" style="width: 110px; height: 110px; object-fit: cover; display: block; border-right: 1px solid #716d4a;" />
            </td>
            <td valign="top" bgcolor="#0d0d0d" style="background-color: #0d0d0d !important; padding: 10px 12px; color: #ffffff !important;">
                <div style="margin-bottom: 4px;">
                    <span style="background-color: #716d4a !important; color: #ffffff !important; font-weight: bold; font-size: 9px; padding: 2px 5px; border-radius: 2px; text-transform: uppercase;">Noticia</span>
                    <span style="color: #ffffff !important; font-size: 10px; margin-left: 6px;">📅 {n['created_at'][:10] if n['created_at'] else ''}</span>
                </div>
                <h3 style="color: #716d4a !important; margin: 0 0 4px 0; font-size: 14px; line-height: 1.2; font-weight: bold;">{n['title']}</h3>
                <p style="color: #ffffff !important; font-size: 11px; line-height: 1.3; margin: 0 0 6px 0;">{(n['short_desc'] or n['full_desc'] or '')[:90]}...</p>
                <a href="https://gothprods.com" target="_blank" style="color: #716d4a !important; font-size: 11px; font-weight: bold; text-decoration: underline;">Leer Nota &rarr;</a>
            </td>
        </tr>
    </table>
    """ for n in noticiero])

    reseñas_cards = "".join([f"""
    <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#0d0d0d" class="darkmode-inner" style="background-color: #0d0d0d !important; border: 1px solid #716d4a; border-radius: 6px; overflow: hidden; margin-bottom: 10px;">
        <tr>
            <td width="110" valign="top" bgcolor="#0d0d0d" style="background-color: #0d0d0d !important; padding: 0;">
                <img src="{get_full_img_url(r['image_filename'], band_title=r['title'], sec='Reseñas de Conciertos')}" alt="{r['title']}" style="width: 110px; height: 110px; object-fit: cover; display: block; border-right: 1px solid #716d4a;" />
            </td>
            <td valign="top" bgcolor="#0d0d0d" style="background-color: #0d0d0d !important; padding: 10px 12px; color: #ffffff !important;">
                <div style="margin-bottom: 4px;">
                    <span style="background-color: #716d4a !important; color: #ffffff !important; font-weight: bold; font-size: 9px; padding: 2px 5px; border-radius: 2px; text-transform: uppercase;">Reseña</span>
                    <span style="color: #ffffff !important; font-size: 10px; margin-left: 6px;">📅 {r['created_at'][:10] if r['created_at'] else ''}</span>
                </div>
                <h3 style="color: #716d4a !important; margin: 0 0 4px 0; font-size: 14px; line-height: 1.2; font-weight: bold;">{r['title']}</h3>
                <p style="color: #ffffff !important; font-size: 11px; line-height: 1.3; margin: 0 0 6px 0;">{(r['short_desc'] or r['full_desc'] or '')[:90]}...</p>
                <a href="https://gothprods.com" target="_blank" style="color: #716d4a !important; font-size: 11px; font-weight: bold; text-decoration: underline;">Leer Reseña &rarr;</a>
            </td>
        </tr>
    </table>
    """ for r in reseñas])

    entrevistas_cards = "".join([f"""
    <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#0d0d0d" class="darkmode-inner" style="background-color: #0d0d0d !important; border: 1px solid #716d4a; border-radius: 6px; overflow: hidden; margin-bottom: 10px;">
        <tr>
            <td width="110" valign="top" bgcolor="#0d0d0d" style="background-color: #0d0d0d !important; padding: 0;">
                <img src="{get_full_img_url(e['image_filename'], band_title=e['title'], sec='Entrevistas Under')}" alt="{e['title']}" style="width: 110px; height: 110px; object-fit: cover; display: block; border-right: 1px solid #716d4a;" />
            </td>
            <td valign="top" bgcolor="#0d0d0d" style="background-color: #0d0d0d !important; padding: 10px 12px; color: #ffffff !important;">
                <div style="margin-bottom: 4px;">
                    <span style="background-color: #716d4a !important; color: #ffffff !important; font-weight: bold; font-size: 9px; padding: 2px 5px; border-radius: 2px; text-transform: uppercase;">Entrevista</span>
                    <span style="color: #ffffff !important; font-size: 10px; margin-left: 6px;">📅 {e['created_at'][:10] if e['created_at'] else ''}</span>
                </div>
                <h3 style="color: #716d4a !important; margin: 0 0 4px 0; font-size: 14px; line-height: 1.2; font-weight: bold;">{e['title']}</h3>
                <p style="color: #ffffff !important; font-size: 11px; line-height: 1.3; margin: 0 0 6px 0;">{(e['short_desc'] or e['full_desc'] or '')[:90]}...</p>
                <a href="https://gothprods.com" target="_blank" style="color: #716d4a !important; font-size: 11px; font-weight: bold; text-decoration: underline;">Ver Entrevista &rarr;</a>
            </td>
        </tr>
    </table>
    """ for e in entrevistas])

    galeria_cards = "".join([f"""
    <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#0d0d0d" class="darkmode-inner" style="background-color: #0d0d0d !important; border: 1px solid #716d4a; border-radius: 6px; overflow: hidden; margin-bottom: 10px;">
        <tr>
            <td width="110" valign="top" bgcolor="#0d0d0d" style="background-color: #0d0d0d !important; padding: 0;">
                <img src="{get_full_img_url(g['image_filename'], band_title=g['title'], sec='La Galería Nocturna')}" alt="{g['title']}" style="width: 110px; height: 110px; object-fit: cover; display: block; border-right: 1px solid #716d4a;" />
            </td>
            <td valign="top" bgcolor="#0d0d0d" style="background-color: #0d0d0d !important; padding: 10px 12px; color: #ffffff !important;">
                <div style="margin-bottom: 4px;">
                    <span style="background-color: #716d4a !important; color: #ffffff !important; font-weight: bold; font-size: 9px; padding: 2px 5px; border-radius: 2px; text-transform: uppercase;">Podcast</span>
                    <span style="color: #ffffff !important; font-size: 10px; margin-left: 6px;">📅 {g['created_at'][:10] if g['created_at'] else ''}</span>
                </div>
                <h3 style="color: #716d4a !important; margin: 0 0 4px 0; font-size: 14px; line-height: 1.2; font-weight: bold;">{g['title']}</h3>
                <p style="color: #ffffff !important; font-size: 11px; line-height: 1.3; margin: 0 0 6px 0;">{(g['short_desc'] or g['full_desc'] or '')[:90]}...</p>
                <a href="https://gothprods.com" target="_blank" style="color: #716d4a !important; font-size: 11px; font-weight: bold; text-decoration: underline;">Reproducir &rarr;</a>
            </td>
        </tr>
    </table>
    """ for g in galeria])

    pulse_items = "".join([f"""
    <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#0d0d0d" class="darkmode-inner" style="background-color: #0d0d0d !important; border: 1px solid #716d4a; border-radius: 6px; margin-bottom: 8px;">
        <tr>
            <td style="padding: 10px 14px; vertical-align: middle;">
                <table role="presentation" border="0" cellspacing="0" cellpadding="0">
                    <tr>
                        <td width="26" valign="top" style="padding-top: 3px;">
                            <div style="background-color: #716d4a !important; color: #ffffff !important; font-weight: 900; width: 26px; height: 26px; line-height: 26px; text-align: center; border-radius: 50%; font-size: 12px; margin: 0;">
                                {idx + 1}
                            </div>
                        </td>
                        <td style="padding-left: 12px;">
                            <strong style="color: #716d4a !important; font-size: 14px; display: block;">{t['title']}</strong>
                            <span style="color: #ffffff !important; font-size: 12px; display: block; margin-bottom: 2px;">{t['short_desc']}</span>
                            {f'''<a href="{t["sp_link"]}" target="_blank" style="color: #1DB954 !important; font-size: 11px; text-decoration: none; font-weight: bold;">Escuchar en Spotify &rarr;</a>''' if t["sp_link"] else ""}
                        </td>
                    </tr>
                </table>
            </td>
            <td align="right" style="padding: 10px 14px; vertical-align: middle; white-space: nowrap;">
                <span style="color: #ffffff !important; font-weight: bold; font-size: 11px; background-color: #191812 !important; border: 1px solid #716d4a; padding: 4px 8px; border-radius: 3px; display: inline-block;">{t['full_desc']}</span>
            </td>
        </tr>
    </table>
    """ for idx, t in enumerate(pulse_tracks[:10])])

    # Agenda Metalera: Solo Bandas (con link directo), Venues y Fecha (sin emojis)
    agenda_cards = "".join([f"""
    <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#0d0d0d" class="darkmode-inner" style="background-color: #0d0d0d !important; border: 1px solid #716d4a; border-radius: 6px; margin-bottom: 10px;">
        <tr>
            <td bgcolor="#0d0d0d" style="background-color: #0d0d0d !important; padding: 12px 16px; vertical-align: middle;">
                <div style="margin-bottom: 4px;">
                    <a href="https://gothprods.com#agenda" target="_blank" style="color: #ffffff !important; font-size: 16px; font-weight: bold; text-decoration: underline; text-underline-offset: 3px;">
                        {a['title']}
                    </a>
                </div>
                <div style="color: #ffffff !important; font-size: 13px; line-height: 1.4;">
                    Venue: <span style="color: #ffffff !important; font-weight: bold;">{(a['short_desc'] or 'Por confirmar').replace(chr(10), ' - ')}</span>
                </div>
            </td>
            <td bgcolor="#0d0d0d" align="right" style="background-color: #0d0d0d !important; padding: 12px 16px; width: 130px; vertical-align: middle;">
                <div style="background-color: #191812 !important; border: 1px solid #716d4a; color: #ffffff !important; padding: 6px 10px; border-radius: 4px; font-size: 12px; font-weight: bold; text-align: center; display: inline-block; white-space: nowrap;">
                    {a['author']}
                </div>
            </td>
        </tr>
    </table>
    """ for a in agenda])

    bandas_eventos_cards = ""
    if bandas or eventos:
        b_html = "".join([f"""
        <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#0d0d0d" class="darkmode-inner" style="background-color: #0d0d0d !important; border: 1px solid #716d4a; border-radius: 6px; overflow: hidden; margin-bottom: 10px;">
            <tr>
                <td width="110" valign="top" bgcolor="#0d0d0d" style="background-color: #0d0d0d !important; padding: 0;">
                    <img src="{get_full_img_url(b['img_video_path'] or b['ultimo_lanzamiento_url'])}" style="width: 110px; height: 100px; object-fit: cover; display: block; border-right: 1px solid #716d4a;" />
                </td>
                <td valign="top" bgcolor="#0d0d0d" style="background-color: #0d0d0d !important; padding: 10px 12px; color: #ffffff !important;">
                    <span style="background-color: #716d4a !important; color: #ffffff !important; font-weight: bold; font-size: 9px; padding: 2px 5px; border-radius: 2px; text-transform: uppercase; display: inline-block;">Banda Destacada</span>
                    <h3 style="color: #716d4a !important; margin: 4px 0; font-size: 14px; font-weight: bold;">{b['nombre']} ({b['pais'] or 'Underground'})</h3>
                    {f'''<h4 style="font-size: 11px; color: #716d4a !important; margin: 0 0 4px 0; font-style: italic;">"{b["titulo_resena"]}"</h4>''' if b["titulo_resena"] else ""}
                    <p style="color: #ffffff !important; font-size: 11px; margin: 0; line-height: 1.3;">{(b['texto_resena'] or b['bio_larga'] or '')[:90]}...</p>
                </td>
            </tr>
        </table>
        """ for b in bandas])
        e_html = "".join([f"""
        <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#0d0d0d" class="darkmode-inner" style="background-color: #0d0d0d !important; border: 1px solid #716d4a; border-radius: 6px; overflow: hidden; margin-bottom: 10px;">
            <tr>
                <td width="110" valign="top" bgcolor="#0d0d0d" style="background-color: #0d0d0d !important; padding: 0;">
                    <img src="{get_full_img_url(e['img_video_path'])}" style="width: 110px; height: 100px; object-fit: cover; display: block; border-right: 1px solid #716d4a;" />
                </td>
                <td valign="top" bgcolor="#0d0d0d" style="background-color: #0d0d0d !important; padding: 10px 12px; color: #ffffff !important;">
                    <span style="background-color: #716d4a !important; color: #ffffff !important; font-weight: bold; font-size: 9px; padding: 2px 5px; border-radius: 2px; text-transform: uppercase; display: inline-block;">Evento Destacado</span>
                    <h3 style="color: #716d4a !important; margin: 4px 0; font-size: 14px; font-weight: bold;">{e['titulo_articulo'] if e['titulo_articulo'] else e['nombre_evento']}</h3>
                    {f'''<p style="color: #716d4a !important; font-size: 11px; margin: 0 0 4px 0; font-weight: bold;">{e["nombre_evento"]}</p>''' if e["titulo_articulo"] and e["titulo_articulo"] != e["nombre_evento"] else ""}
                    <p style="color: #ffffff !important; font-size: 11px; margin: 0; line-height: 1.3;">📍 {e['ciudad']}, {e['pais']} <br/> 📅 {e['fecha_evento']}</p>
                </td>
            </tr>
        </table>
        """ for e in eventos])
        bandas_eventos_cards = b_html + e_html

    default_intro = f"Les presentamos la recopilación oficial de {month_label} con lo más destacado de El Noticiero Nocturno, Reseñas de Conciertos, Entrevistas Under, Metal Pulse, La Galería Nocturna y la Agenda Metalera."

    logo_img_url = get_full_img_url('assets/logo.png')
    noticiero_icon_url = get_full_img_url('assets/noticiero_icon.png')
    resenas_icon_url = get_full_img_url('assets/resenas_icon.png')
    entrevistas_icon_url = get_full_img_url('assets/entrevistas_icon.png')
    metal_pulse_icon_url = get_full_img_url('assets/metal_pulse_icon.jpg')
    galeria_icon_url = get_full_img_url('assets/galeria_nocturna_icon.jpg')
    agenda_icon_url = get_full_img_url('assets/agenda_icon.png')
    destacados_icon_url = get_full_img_url('assets/destacados_icon.png')

    html = f"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="es">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="color-scheme" content="light dark" />
    <meta name="supported-color-schemes" content="light dark" />
    <title>{asunto}</title>
    <style type="text/css">
        :root {{
            color-scheme: dark;
            supported-color-schemes: dark;
        }}
        body, table, td, p, a, span, h1, h2, h3 {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
            -webkit-font-smoothing: antialiased;
        }}
        body {{
            background-color: #000000 !important;
            margin: 0 !important;
            padding: 0 !important;
            width: 100% !important;
            color: #ffffff !important;
        }}
        @media (prefers-color-scheme: light) {{
            .darkmode-bg {{ background-color: #000000 !important; }}
            .darkmode-card {{ background-color: #080808 !important; }}
            .darkmode-inner {{ background-color: #0d0d0d !important; }}
            .darkmode-text {{ color: #ffffff !important; }}
            .darkmode-title {{ color: #716d4a !important; }}
        }}
        @media (prefers-color-scheme: dark) {{
            .darkmode-bg {{ background-color: #000000 !important; }}
            .darkmode-card {{ background-color: #080808 !important; }}
            .darkmode-inner {{ background-color: #0d0d0d !important; }}
            .darkmode-text {{ color: #ffffff !important; }}
            .darkmode-title {{ color: #716d4a !important; }}
        }}
        @media print {{
            body {{ -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; background-color: #000000 !important; color: #ffffff !important; margin: 0 !important; padding: 0 !important; }}
            .darkmode-card {{ border: none !important; box-shadow: none !important; margin: 0 auto !important; max-width: 100% !important; }}
        }}
    </style>
</head>
<body bgcolor="#000000" class="darkmode-bg" style="margin: 0; padding: 0; background-color: #000000 !important; background: #000000 !important; color: #ffffff !important;">
    <!-- FULL WRAPPER TABLE -->
    <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#000000" class="darkmode-bg" style="width: 100% !important; background-color: #000000 !important; background: #000000 !important; margin: 0; padding: 20px 10px;">
        <tr>
            <td align="center" bgcolor="#000000" class="darkmode-bg" style="background-color: #000000 !important; padding: 0;">
                
                <!-- CONTAINER CARD -->
                <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#080808" class="darkmode-card" style="max-width: 660px; width: 100% !important; background-color: #080808 !important; background: #080808 !important; border: 1px solid #716d4a; border-radius: 8px; overflow: hidden;">
                    
                    <!-- TOP BANNER -->
                    <tr>
                        <td align="center" bgcolor="#000000" style="background-color: #000000 !important; border-bottom: 2px solid #716d4a; padding: 10px 15px; color: #716d4a !important; font-weight: 900; letter-spacing: 2px; font-size: 11px; text-transform: uppercase;">
                            ⚔️ GOTH PRODUCTIONS &bull; COMUNIDAD BERSERKERS ⚔️
                        </td>
                    </tr>

                    <!-- HEADER -->
                    <tr>
                        <td align="center" bgcolor="#000000" style="background-color: #000000 !important; padding: 30px 20px 24px 20px; border-bottom: 2px solid #716d4a;">
                            <img src="{logo_img_url}" width="150" alt="Goth Prods Logo" style="display: block; width: 150px; max-width: 150px; height: auto; margin: 0 auto 12px auto; border: 0;" />
                            <h1 style="color: #716d4a !important; margin: 0 0 10px 0; font-size: 22px; text-transform: uppercase; letter-spacing: 2px; font-weight: 900; line-height: 1.2;">
                                Newsletter
                            </h1>
                            <table role="presentation" border="0" cellspacing="0" cellpadding="0" align="center">
                                <tr>
                                    <td bgcolor="#000000" style="border: 1px solid #716d4a; border-radius: 20px; padding: 4px 16px;">
                                        <span style="color: #ffffff !important; font-size: 12px; font-weight: bold; letter-spacing: 1px; text-transform: uppercase;">
                                            🔥 EDICIÓN OFICIAL: {month_label.upper()} 🔥
                                        </span>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>

                    <!-- INTRO -->
                    <tr>
                        <td bgcolor="#0a0a0a" style="background-color: #0a0a0a !important; padding: 22px 25px; border-bottom: 1px solid #222222; border-left: 4px solid #716d4a; color: #ffffff !important;">
                            <strong style="color: #716d4a !important; font-size: 16px; display: block; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px;">SALUDOS BERSERKERS</strong>
                            <p style="color: #ffffff !important; font-size: 14px; line-height: 1.6; margin: 0;">
                                {mensaje_intro if mensaje_intro else default_intro}
                            </p>
                        </td>
                    </tr>

                    <!-- RADAR DEL CAOS & EL PIT -->
                    {f'''
                    <tr>
                        <td bgcolor="#080808" style="background-color: #080808 !important; padding: 24px 25px; border-bottom: 1px solid #1a1a1a;">
                            <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" style="border-bottom: 1px solid #716d4a; margin-bottom: 18px; padding-bottom: 10px;">
                                <tr>
                                    <td style="vertical-align: middle;">
                                        <img src="{destacados_icon_url}" width="32" height="32" style="width: 32px; height: 32px; border-radius: 50%; border: 1px solid #716d4a; vertical-align: middle; margin-right: 10px; object-fit: cover;" />
                                        <h2 style="color: #716d4a !important; font-size: 19px; text-transform: uppercase; margin: 0; letter-spacing: 1px; font-weight: 900; display: inline-block; vertical-align: middle;">Radar del Caos & El Pit</h2>
                                    </td>
                                </tr>
                            </table>
                            {bandas_eventos_cards}
                        </td>
                    </tr>
                    ''' if bandas_eventos_cards else ''}

                    <!-- EL NOTICIERO NOCTURNO -->
                    {f'''
                    <tr>
                        <td bgcolor="#080808" style="background-color: #080808 !important; padding: 24px 25px; border-bottom: 1px solid #1a1a1a;">
                            <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" style="border-bottom: 1px solid #716d4a; margin-bottom: 18px; padding-bottom: 10px;">
                                <tr>
                                    <td style="vertical-align: middle;">
                                        <img src="{noticiero_icon_url}" width="32" height="32" style="width: 32px; height: 32px; border-radius: 50%; border: 1px solid #716d4a; vertical-align: middle; margin-right: 10px; object-fit: cover;" />
                                        <h2 style="color: #716d4a !important; font-size: 19px; text-transform: uppercase; margin: 0; letter-spacing: 1px; font-weight: 900; display: inline-block; vertical-align: middle;">El Noticiero Nocturno</h2>
                                    </td>
                                </tr>
                            </table>
                            {noticiero_cards}
                        </td>
                    </tr>
                    ''' if noticiero_cards else ''}

                    <!-- RESEÑAS DE CONCIERTOS -->
                    {f'''
                    <tr>
                        <td bgcolor="#080808" style="background-color: #080808 !important; padding: 24px 25px; border-bottom: 1px solid #1a1a1a;">
                            <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" style="border-bottom: 1px solid #716d4a; margin-bottom: 18px; padding-bottom: 10px;">
                                <tr>
                                    <td style="vertical-align: middle;">
                                        <img src="{resenas_icon_url}" width="32" height="32" style="width: 32px; height: 32px; border-radius: 50%; border: 1px solid #716d4a; vertical-align: middle; margin-right: 10px; object-fit: cover;" />
                                        <h2 style="color: #716d4a !important; font-size: 19px; text-transform: uppercase; margin: 0; letter-spacing: 1px; font-weight: 900; display: inline-block; vertical-align: middle;">Reseñas de Conciertos</h2>
                                    </td>
                                </tr>
                            </table>
                            {reseñas_cards}
                        </td>
                    </tr>
                    ''' if reseñas_cards else ''}

                    <!-- TOP 10 METAL PULSE -->
                    {f'''
                    <tr>
                        <td bgcolor="#080808" style="background-color: #080808 !important; padding: 24px 25px; border-bottom: 1px solid #1a1a1a;">
                            <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" style="border-bottom: 1px solid #716d4a; margin-bottom: 18px; padding-bottom: 10px;">
                                <tr>
                                    <td style="vertical-align: middle;">
                                        <img src="{metal_pulse_icon_url}" width="32" height="32" style="width: 32px; height: 32px; border-radius: 50%; border: 1px solid #716d4a; vertical-align: middle; margin-right: 10px; object-fit: cover;" />
                                        <h2 style="color: #716d4a !important; font-size: 19px; text-transform: uppercase; margin: 0; letter-spacing: 1px; font-weight: 900; display: inline-block; vertical-align: middle;">Metal Pulse - Los Favoritos de {month_label}</h2>
                                    </td>
                                </tr>
                            </table>
                            <div style="margin-bottom: 15px;">
                                {pulse_items}
                            </div>
                        </td>
                    </tr>
                    ''' if pulse_items else ''}

                    <!-- ENTREVISTAS UNDER -->
                    {f'''
                    <tr>
                        <td bgcolor="#080808" style="background-color: #080808 !important; padding: 24px 25px; border-bottom: 1px solid #1a1a1a;">
                            <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" style="border-bottom: 1px solid #716d4a; margin-bottom: 18px; padding-bottom: 10px;">
                                <tr>
                                    <td style="vertical-align: middle;">
                                        <img src="{entrevistas_icon_url}" width="32" height="32" style="width: 32px; height: 32px; border-radius: 50%; border: 1px solid #716d4a; vertical-align: middle; margin-right: 10px; object-fit: cover;" />
                                        <h2 style="color: #716d4a !important; font-size: 19px; text-transform: uppercase; margin: 0; letter-spacing: 1px; font-weight: 900; display: inline-block; vertical-align: middle;">Entrevistas Under</h2>
                                    </td>
                                </tr>
                            </table>
                            {entrevistas_cards}
                        </td>
                    </tr>
                    ''' if entrevistas_cards else ''}

                    <!-- AGENDA METALERA (DEL MES SIGUIENTE) -->
                    {f'''
                    <tr>
                        <td bgcolor="#080808" style="background-color: #080808 !important; padding: 24px 25px; border-bottom: 1px solid #1a1a1a;">
                            <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" style="border-bottom: 1px solid #716d4a; margin-bottom: 18px; padding-bottom: 10px;">
                                <tr>
                                    <td style="vertical-align: middle;">
                                        <img src="{agenda_icon_url}" width="32" height="32" style="width: 32px; height: 32px; border-radius: 50%; border: 1px solid #716d4a; vertical-align: middle; margin-right: 10px; object-fit: cover;" />
                                        <h2 style="color: #716d4a !important; font-size: 19px; text-transform: uppercase; margin: 0; letter-spacing: 1px; font-weight: 900; display: inline-block; vertical-align: middle;">Agenda Metalera ({next_month_label})</h2>
                                    </td>
                                </tr>
                            </table>
                            {agenda_cards}
                        </td>
                    </tr>
                    ''' if agenda_cards else ''}

                    <!-- LA GALERÍA NOCTURNA & CAOS SONORO -->
                    {f'''
                    <tr>
                        <td bgcolor="#080808" style="background-color: #080808 !important; padding: 24px 25px; border-bottom: 1px solid #1a1a1a;">
                            <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" style="border-bottom: 1px solid #716d4a; margin-bottom: 18px; padding-bottom: 10px;">
                                <tr>
                                    <td style="vertical-align: middle;">
                                        <img src="{galeria_icon_url}" width="32" height="32" style="width: 32px; height: 32px; border-radius: 50%; border: 1px solid #716d4a; vertical-align: middle; margin-right: 10px; object-fit: cover;" />
                                        <h2 style="color: #716d4a !important; font-size: 19px; text-transform: uppercase; margin: 0; letter-spacing: 1px; font-weight: 900; display: inline-block; vertical-align: middle;">La Galería Nocturna & Caos Sonoro</h2>
                                    </td>
                                </tr>
                            </table>
                            {galeria_cards}
                        </td>
                    </tr>
                    ''' if galeria_cards else ''}

                    <!-- CTA WEB -->
                    <tr>
                        <td align="center" bgcolor="#000000" style="background-color: #000000 !important; padding: 30px 20px; border-bottom: 1px solid #1a1a1a;">
                            <table role="presentation" border="0" cellspacing="0" cellpadding="0" align="center">
                                <tr>
                                    <td bgcolor="#716d4a" style="background-color: #716d4a !important; border-radius: 4px; padding: 12px 28px;">
                                        <a href="https://gothprods.com" target="_blank" style="color: #ffffff !important; font-size: 14px; font-weight: 900; text-decoration: none; text-transform: uppercase; letter-spacing: 1.5px; display: inline-block;">
                                            VISITAR GOTHPRODS.COM &rarr;
                                        </a>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>

                    <!-- FOOTER -->
                    <tr>
                        <td align="center" bgcolor="#000000" style="background-color: #000000 !important; padding: 30px 20px; text-align: center; border-top: 2px solid #716d4a; color: #ffffff !important;">
                            <img src="{logo_img_url}" width="60" style="display: block; width: 60px; height: auto; margin: 0 auto 12px auto; opacity: 0.9;" />
                            <p style="color: #716d4a !important; font-weight: bold; margin: 0 0 8px 0; font-size: 13px; letter-spacing: 1px; text-transform: uppercase;">
                                ⚔️ ERES PARTE DE LA COMUNIDAD BERSERKERS ⚔️
                            </p>
                            <p style="margin: 4px 0; color: #ffffff !important; font-size: 12px;">&copy; 2026 Goth Productions &bull; Medio Mexicano de Divulgación del Género Más Feroz del Planeta</p>
                            <p style="margin: 4px 0; color: #aaaaaa !important; font-size: 11px;">Estás recibiendo este correo oficial porque eres un Berserker en <a href="https://gothprods.com" target="_blank" style="color: #aaaaaa !important; text-decoration: underline;">gothprods.com</a></p>
                        </td>
                    </tr>

                </table>
            </td>
        </tr>
    </table>
</body>
</html>"""
    return html


@app.route('/admin/newsletter/preview', methods=['POST'])
def admin_newsletter_preview():
    if session.get('role') not in ['admin', 'root']:
        return jsonify({'error': 'Unauthorized'}), 403
    data = request.get_json() or {}
    asunto = data.get('asunto', 'GothProds Newsletter')
    intro = data.get('intro', '')
    target_month = data.get('target_month', '2026-07')
    host_base = request.host_url.rstrip('/') if request.host_url else None
    html = build_newsletter_html(asunto, intro, target_month=target_month, base_url_override=host_base)
    return html


@app.route('/admin/newsletter/send', methods=['POST'])
def admin_newsletter_send():
    if session.get('role') not in ['admin', 'root']:
        flash('Acceso denegado', 'error')
        return redirect(url_for('admin_dashboard'))

    asunto = request.form.get('asunto', 'GothProds Newsletter')
    mensaje_intro = request.form.get('mensaje_intro', '')
    target_month = request.form.get('target_month', '2026-07')

    conn = get_db_connection()
    subs = conn.execute("SELECT email, nombre FROM newsletter_subscribers WHERE is_active = 1").fetchall()
    conn.close()

    if not subs:
        flash('No hay suscriptores activos registrados para enviar el boletín.', 'error')
        return redirect(url_for('admin_dashboard'))

    html_content = build_newsletter_html(asunto, mensaje_intro, target_month=target_month)
    
    sent_count = 0
    for sub in subs:
        sub_email = sub['email']
        sub_name = sub['nombre'] or 'Berserker'
        text_content = f"""¡Saludos Berserker {sub_name}!

{mensaje_intro if mensaje_intro else 'Te compartimos las novedades más destacadas y los próximos conciertos en nuestra agenda metalera.'}

- Portal Web: https://gothprods.com
- Agenda Metalera: https://gothprods.com#agenda

GOTH PRODUCTIONS • MEDIO MEXICANO DE DIVULGACIÓN DEL GÉNERO MÁS FEROZ DEL PLANETA
"""
        if send_goth_email(sub_email, asunto, html_content, text_content):
            sent_count += 1

    if sent_count > 0:
        flash(f'¡Newsletter enviado exitosamente a {sent_count} suscriptor(es)!', 'success')
    else:
        flash(f'No se pudo entregar el newsletter a los suscriptores. Revisa la configuración SMTP.', 'error')

    return redirect(url_for('admin_dashboard'))

@app.route('/admin/newsletter/export_csv')
def admin_newsletter_export_csv():
    if session.get('role') not in ['admin', 'root']:
        return redirect(url_for('admin_dashboard'))

    conn = get_db_connection()
    subs = conn.execute("SELECT id, nombre, email, created_at FROM newsletter_subscribers WHERE is_active = 1 ORDER BY id DESC").fetchall()
    conn.close()

    import io, csv
    from flask import Response

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Nombre', 'Email', 'Fecha Registro'])
    for s in subs:
        writer.writerow([s['id'], s['nombre'], s['email'], s['created_at']])

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=suscriptores_gothprods.csv"}
    )

@app.route('/admin/newsletter/subscriber/add', methods=['POST'])
def admin_newsletter_subscriber_add():
    if session.get('role') not in ['admin', 'root']:
        if is_ajax_request(request):
            return jsonify({'status': 'error', 'message': 'Acceso denegado'}), 403
        flash('Acceso denegado', 'error')
        return redirect(url_for('admin_dashboard'))

    if request.is_json:
        data = request.get_json() or {}
        nombre = data.get('nombre', '').strip()
        email = data.get('email', '').strip().lower()
        send_welcome = data.get('send_welcome', False)
    else:
        nombre = request.form.get('nombre', '').strip()
        email = request.form.get('email', '').strip().lower()
        send_welcome = request.form.get('send_welcome') == 'on'

    if not email or '@' not in email:
        msg = 'Por favor ingresa un correo electrónico válido.'
        if is_ajax_request(request):
            return jsonify({'status': 'error', 'message': msg}), 400
        flash(msg, 'error')
        return redirect(url_for('admin_dashboard') + '#tab-newsletter')

    conn = get_db_connection()
    try:
        cur = conn.execute("SELECT id FROM newsletter_subscribers WHERE email = ?", (email,))
        existing = cur.fetchone()
        if existing:
            welcome_val = 1 if send_welcome else 0
            conn.execute("UPDATE newsletter_subscribers SET is_active = 1, nombre = ?, welcome_sent = MAX(welcome_sent, ?) WHERE id = ?", (nombre or 'Berserker', welcome_val, existing['id']))
            conn.commit()
            sub_id = existing['id']
            msg = f'Suscriptor {email} reactivado/actualizado exitosamente.'
        else:
            cur = conn.execute("INSERT INTO newsletter_subscribers (nombre, email, created_at, welcome_sent) VALUES (?, ?, ?, ?)", (nombre or 'Berserker', email, get_mexico_now_str(), 1 if send_welcome else 0))
            conn.commit()
            sub_id = cur.lastrowid
            msg = f'Suscriptor {nombre or email} registrado exitosamente.'
        
        if send_welcome:
            threading.Thread(target=send_newsletter_welcome_email, args=(email, nombre or 'Berserker')).start()

        if is_ajax_request(request):
            return jsonify({
                'status': 'success',
                'message': msg,
                'subscriber': {
                    'id': sub_id,
                    'nombre': nombre or 'Berserker',
                    'email': email,
                    'is_active': 1,
                    'created_at': get_mexico_now_str()[:10]
                }
            })
        flash(msg, 'success')
    except Exception as e:
        msg = f'Error al registrar suscriptor: {e}'
        if is_ajax_request(request):
            return jsonify({'status': 'error', 'message': msg}), 500
        flash(msg, 'error')
    finally:
        conn.close()

    return redirect(url_for('admin_dashboard') + '#tab-newsletter')

@app.route('/admin/newsletter/subscriber/edit/<int:id>', methods=['POST'])
def admin_newsletter_subscriber_edit(id):
    if session.get('role') not in ['admin', 'root']:
        if is_ajax_request(request):
            return jsonify({'status': 'error', 'message': 'Acceso denegado'}), 403
        flash('Acceso denegado', 'error')
        return redirect(url_for('admin_dashboard'))

    if request.is_json:
        data = request.get_json() or {}
        nombre = data.get('nombre', '').strip()
        email = data.get('email', '').strip().lower()
        is_active = 1 if data.get('is_active', 1) in [1, '1', True, 'true', 'on'] else 0
    else:
        nombre = request.form.get('nombre', '').strip()
        email = request.form.get('email', '').strip().lower()
        is_active = 1 if request.form.get('is_active') in ['1', 'on', 'true', True] else 0

    if not email or '@' not in email:
        msg = 'Por favor ingresa un correo electrónico válido.'
        if is_ajax_request(request):
            return jsonify({'status': 'error', 'message': msg}), 400
        flash(msg, 'error')
        return redirect(url_for('admin_dashboard') + '#tab-newsletter')

    conn = get_db_connection()
    try:
        # Check if email is already taken by another subscriber
        existing = conn.execute("SELECT id FROM newsletter_subscribers WHERE email = ? AND id != ?", (email, id)).fetchone()
        if existing:
            msg = 'Este correo electrónico ya está registrado en otro suscriptor.'
            if is_ajax_request(request):
                return jsonify({'status': 'error', 'message': msg}), 400
            flash(msg, 'error')
            return redirect(url_for('admin_dashboard') + '#tab-newsletter')

        conn.execute("UPDATE newsletter_subscribers SET nombre = ?, email = ?, is_active = ? WHERE id = ?", (nombre or 'Berserker', email, is_active, id))
        conn.commit()
        msg = f'Suscriptor {email} actualizado exitosamente.'
        if is_ajax_request(request):
            return jsonify({
                'status': 'success',
                'message': msg,
                'subscriber': {
                    'id': id,
                    'nombre': nombre or 'Berserker',
                    'email': email,
                    'is_active': is_active
                }
            })
        flash(msg, 'success')
    except Exception as e:
        msg = f'Error al actualizar suscriptor: {e}'
        if is_ajax_request(request):
            return jsonify({'status': 'error', 'message': msg}), 500
        flash(msg, 'error')
    finally:
        conn.close()

    return redirect(url_for('admin_dashboard') + '#tab-newsletter')

@app.route('/admin/newsletter/view', methods=['GET'])
def admin_newsletter_view():
    if session.get('role') not in ['admin', 'root']:
        return redirect(url_for('admin_login'))

    target_month = request.args.get('month', '2026-07')
    asunto = request.args.get('asunto', f'⚔️ GothProds Newsletter - Resumen Berserkers ({target_month})')
    intro = request.args.get('intro', '')
    host_base = request.host_url.rstrip('/') if request.host_url else None
    
    html_content = build_newsletter_html(asunto, intro, target_month=target_month, live=False, base_url_override=host_base)
    return html_content

@app.route('/admin/newsletter/resend_welcome/<int:id>', methods=['POST'])
def admin_newsletter_resend_welcome(id):
    if session.get('role') not in ['admin', 'root']:
        if is_ajax_request(request):
            return jsonify({'status': 'error', 'message': 'Acceso denegado'}), 403
        flash('Acceso denegado', 'error')
        return redirect(url_for('admin_dashboard'))

    conn = get_db_connection()
    sub = conn.execute("SELECT id, nombre, email FROM newsletter_subscribers WHERE id = ?", (id,)).fetchone()

    if not sub:
        conn.close()
        if is_ajax_request(request):
            return jsonify({'status': 'error', 'message': 'Suscriptor no encontrado.'}), 404
        flash('Suscriptor no encontrado.', 'error')
        return redirect(url_for('admin_dashboard'))

    conn.execute("UPDATE newsletter_subscribers SET welcome_sent = 1 WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    threading.Thread(target=send_newsletter_welcome_email, args=(sub['email'], sub['nombre'] or 'Berserker')).start()
    msg = f"⚔️ El envío del correo oficial de bienvenida a {sub['email']} se ha iniciado en segundo plano."
    if is_ajax_request(request):
        return jsonify({'status': 'success', 'message': msg})
    flash(msg, 'success')

    return redirect(url_for('admin_dashboard') + '#tab-newsletter')

@app.route('/admin/newsletter/bulk_welcome', methods=['POST'])
def admin_newsletter_bulk_welcome():
    if session.get('role') not in ['admin', 'root']:
        return jsonify({'status': 'error', 'message': 'Acceso denegado'}), 403

    data = request.get_json()
    if not data or 'ids' not in data:
        return jsonify({'status': 'error', 'message': 'Datos inválidos.'}), 400

    ids = data['ids']
    if not isinstance(ids, list) or not ids:
        return jsonify({'status': 'error', 'message': 'No se seleccionaron suscriptores.'}), 400

    conn = get_db_connection()
    subs = conn.execute(f"SELECT id, nombre, email FROM newsletter_subscribers WHERE id IN ({','.join(['?']*len(ids))})", tuple(ids)).fetchall()
    
    if not subs:
        conn.close()
        return jsonify({'status': 'error', 'message': 'No se encontraron los suscriptores seleccionados.'}), 404

    # Marcar como enviados en BD
    conn.execute(f"UPDATE newsletter_subscribers SET welcome_sent = 1 WHERE id IN ({','.join(['?']*len(ids))})", tuple(ids))
    conn.commit()
    conn.close()

    # Enviar correos
    for sub in subs:
        threading.Thread(target=send_newsletter_welcome_email, args=(sub['email'], sub['nombre'] or 'Berserker')).start()

    return jsonify({'status': 'success', 'message': f'Se enviarán {len(subs)} correos de bienvenida en segundo plano.'})

@app.route('/admin/newsletter/delete/<int:id>', methods=['POST'])
def admin_newsletter_delete(id):
    if session.get('role') not in ['admin', 'root']:
        if is_ajax_request(request):
            return jsonify({'status': 'error', 'message': 'Acceso denegado'}), 403
        flash('Acceso denegado', 'error')
        return redirect(url_for('admin_dashboard'))

    conn = get_db_connection()
    conn.execute("UPDATE newsletter_subscribers SET is_active = -1 WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    
    if is_ajax_request(request):
        return jsonify({'status': 'success', 'message': 'Suscriptor eliminado correctamente.', 'deleted_id': id})

    flash('Suscriptor eliminado correctamente.', 'success')
    return redirect(url_for('admin_dashboard') + '#tab-newsletter')

@app.route('/admin/newsletter/delete_bulk', methods=['POST'])
def admin_newsletter_delete_bulk():
    if session.get('role') not in ['admin', 'root']:
        if is_ajax_request(request):
            return jsonify({'status': 'error', 'message': 'Acceso denegado'}), 403
        flash('Acceso denegado', 'error')
        return redirect(url_for('admin_dashboard'))

    ids = []
    if request.is_json:
        data = request.get_json() or {}
        ids = data.get('ids', [])
    else:
        ids = request.form.getlist('ids')
        if not ids and request.form.get('ids'):
            ids = [x.strip() for x in request.form.get('ids').split(',') if x.strip()]

    clean_ids = [int(i) for i in ids if str(i).isdigit()]
    if not clean_ids:
        msg = 'No se seleccionó ningún suscriptor para eliminar.'
        if is_ajax_request(request):
            return jsonify({'status': 'error', 'message': msg}), 400
        flash(msg, 'error')
        return redirect(url_for('admin_dashboard') + '#tab-newsletter')

    conn = get_db_connection()
    placeholders = ','.join(['?'] * len(clean_ids))
    conn.execute(f"UPDATE newsletter_subscribers SET is_active = -1 WHERE id IN ({placeholders})", tuple(clean_ids))
    conn.commit()
    conn.close()

    msg = f'Se eliminaron {len(clean_ids)} suscriptor(es) correctamente.'
    if is_ajax_request(request):
        return jsonify({'status': 'success', 'message': msg, 'deleted_count': len(clean_ids), 'deleted_ids': clean_ids})

    flash(msg, 'success')
    return redirect(url_for('admin_dashboard') + '#tab-newsletter')

@app.route('/admin/newsletter/test_smtp', methods=['POST'])
def admin_newsletter_test_smtp():
    if session.get('role') not in ['admin', 'root']:
        return jsonify({'status': 'error', 'message': 'Acceso denegado'}), 403

    data = request.get_json(silent=True) or {}
    test_email = (data.get('test_email') or session.get('user_email') or 'goth.prods@gmail.com').strip()
    
    if not test_email or '@' not in test_email:
        return jsonify({'status': 'error', 'message': 'Ingresa un correo destino válido para la prueba.'}), 400

    subject = "🧪 [DIAGNÓSTICO] Prueba de Conexión SMTP - Goth Productions"
    html_content = f"""
    <div style="background:#0a0a0a; color:#f0f0f0; padding:25px; font-family:Arial,sans-serif; border:1px solid #cca85b; border-radius:8px;">
        <h2 style="color:#cca85b; margin-top:0;">⚡ Diagnóstico de Conexión SMTP Exitoso</h2>
        <p>Este correo confirma que el servidor de correo de <strong>Goth Productions</strong> está transmitiendo correctamente.</p>
        <hr style="border:0; border-top:1px solid #333; margin:15px 0;">
        <p style="font-size:0.9rem; color:#aaa;"><strong>Servidor:</strong> smtp.gmail.com:465 / 587<br><strong>Fecha (CDMX):</strong> {get_mexico_now_str()}<br><strong>Destinatario:</strong> {test_email}</p>
        <p style="margin-top:20px; font-size:0.8rem; color:#888;">GOTH PRODUCTIONS • SISTEMA AUTOMATIZADO</p>
    </div>
    """
    text_content = f"Prueba SMTP Goth Productions exitosa para {test_email} a las {get_mexico_now_str()}."

    success = send_goth_email(test_email, subject, html_content, text_content)
    if success:
        return jsonify({'status': 'success', 'message': f'¡Prueba exitosa! Correo de diagnóstico entregado correctamente a {test_email}.'})
    else:
        return jsonify({'status': 'error', 'message': f'Falló el envío de prueba hacia {test_email}. Revisa las credenciales SMTP.'}), 500


@app.route('/api/sync/subscribers', methods=['GET', 'POST'])
def api_sync_subscribers():
    # Permitir autenticación mediante token en header, parámetro GET/POST o sesión de admin
    token = request.headers.get('X-Sync-Token') or request.args.get('token') or request.form.get('token')
    if not token and request.is_json:
        token = request.get_json().get('token')
        
    expected_token = os.getenv('SYNC_TOKEN', 'gothprods_berserkers_sync_2026')
    
    is_admin = session.get('role') in ['admin', 'root']
    
    if (not token or token != expected_token) and not is_admin:
        return jsonify({'error': 'Unauthorized', 'message': 'Token de sincronización inválido o no proporcionado.'}), 401
        
    conn = get_db_connection()
    try:
        cur = conn.execute("SELECT id, nombre, email, is_active, created_at FROM newsletter_subscribers ORDER BY id ASC")
        rows = cur.fetchall()
        data = [dict(r) for r in rows]
        return jsonify({
            'status': 'success',
            'count': len(data),
            'subscribers': data
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        conn.close()

@app.route('/admin/newsletter/sync_remote', methods=['POST'])
def admin_newsletter_sync_remote():
    if session.get('role') not in ['admin', 'root']:
        flash('Acceso denegado', 'error')
        return redirect(url_for('admin_dashboard'))

    remote_url = request.form.get('remote_url', '').strip().rstrip('/')
    sync_token = request.form.get('sync_token', '').strip() or os.getenv('SYNC_TOKEN', 'gothprods_berserkers_sync_2026')
    admin_email = request.form.get('admin_email', '').strip()
    admin_password = request.form.get('admin_password', '').strip()

    if not remote_url:
        remote_url = 'https://gothprods.com'

    if not remote_url.startswith('http://') and not remote_url.startswith('https://'):
        remote_url = 'https://' + remote_url

    import urllib.request
    import urllib.parse
    import http.cookiejar
    import json
    import ssl
    import csv
    import io
    import re

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(cj),
        urllib.request.HTTPSHandler(context=ctx)
    )

    subscribers = []
    sync_source = None
    last_error = None

    # ESTRATEGIA 1: Probar endpoint directo de API con token
    try:
        endpoint = f"{remote_url}/api/sync/subscribers"
        req = urllib.request.Request(
            endpoint,
            headers={
                'X-Sync-Token': sync_token,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) GothProds-Sync/1.0'
            }
        )
        with opener.open(req, timeout=10) as response:
            if response.status == 200:
                payload = json.loads(response.read().decode('utf-8'))
                subscribers = payload.get('subscribers', [])
                sync_source = 'API en vivo'
    except urllib.error.HTTPError as e:
        last_error = f"Código HTTP {e.code}"
    except Exception as e:
        last_error = str(e)

    # ESTRATEGIA 2: Si la API dio 404 (porque aún no se subió app.py a producción) y el usuario ingresó credenciales de admin
    if not subscribers and admin_email and admin_password:
        try:
            login_url = f"{remote_url}/admin/login"
            login_data = urllib.parse.urlencode({'email': admin_email, 'password': admin_password}).encode('utf-8')
            login_req = urllib.request.Request(
                login_url,
                data=login_data,
                headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
            )
            with opener.open(login_req, timeout=12) as login_resp:
                pass

            # Intentar descargar CSV de suscriptores con la sesión iniciada
            csv_url = f"{remote_url}/admin/newsletter/export_csv"
            csv_req = urllib.request.Request(csv_url, headers={'User-Agent': 'Mozilla/5.0'})
            try:
                with opener.open(csv_req, timeout=12) as csv_resp:
                    content_type = csv_resp.headers.get('Content-Type', '')
                    if csv_resp.status == 200 and ('csv' in content_type or 'text' in content_type):
                        csv_text = csv_resp.read().decode('utf-8', errors='ignore')
                        if 'Email' in csv_text or 'Correo' in csv_text or '@' in csv_text:
                            reader = csv.reader(io.StringIO(csv_text))
                            headers = next(reader, None)
                            for row in reader:
                                if len(row) >= 3 and '@' in row[2]:
                                    subscribers.append({'nombre': row[1], 'email': row[2], 'created_at': row[3] if len(row) > 3 else None})
                            if subscribers:
                                sync_source = 'Exportación CSV autenticada'
            except Exception:
                pass

            # Si no se obtuvo por CSV, scrapear la tabla de suscriptores del panel de control
            if not subscribers:
                dash_url = f"{remote_url}/admin"
                dash_req = urllib.request.Request(dash_url, headers={'User-Agent': 'Mozilla/5.0'})
                with opener.open(dash_req, timeout=12) as dash_resp:
                    dash_html = dash_resp.read().decode('utf-8', errors='ignore')
                    # Extraer filas con correos
                    matches = re.findall(r'<tr[^>]*>\s*<td[^>]*>#?(\d+)</td>\s*<td[^>]*>(?:<strong>)?(.*?)(?:</strong>)?</td>\s*<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>', dash_html, re.DOTALL)
                    for m in matches:
                        email_cand = m[2].strip()
                        if '@' in email_cand:
                            # Limpiar posibles tags html residuales
                            email_clean = re.sub(r'<[^>]+>', '', email_cand)
                            nombre_clean = re.sub(r'<[^>]+>', '', m[1].strip())
                            fecha_clean = re.sub(r'<[^>]+>', '', m[3].strip())
                            subscribers.append({'nombre': nombre_clean, 'email': email_clean, 'created_at': fecha_clean})
                    if subscribers:
                        sync_source = 'Panel de Administración en vivo'
        except Exception as e:
            last_error = f"Error al conectar con credenciales: {str(e)}"

    if not subscribers:
        if not admin_email or not admin_password:
            err_msg = f'No se pudo sincronizar automáticamente con {remote_url} (Ruta API no encontrada o no autorizada). Asegúrate de que el token de sincronización sea correcto y que los últimos cambios estén desplegados en Render.'
        else:
            err_msg = f'No se pudieron obtener suscriptores desde {remote_url}. Verifica que las credenciales de administrador de la página en vivo sean correctas. ({last_error})'
        
        if request.is_json or request.headers.get('Accept') == 'application/json':
            return jsonify({'status': 'error', 'message': err_msg}), 400
        flash(err_msg, 'error')
        return redirect(url_for('admin_dashboard') + '#sec-sync-remote')

    # Guardar en base de datos local
    conn = get_db_connection()
    added = 0
    updated = 0

    for sub in subscribers:
        email = (sub.get('email') or '').strip().lower()
        if not email or '@' not in email:
            continue

        nombre = (sub.get('nombre') or 'Berserker').strip()
        is_active = sub.get('is_active', 1)
        created_at = sub.get('created_at')

        cur = conn.execute("SELECT id, is_active FROM newsletter_subscribers WHERE email = ?", (email,))
        existing = cur.fetchone()
        if existing:
            # Always respect the remote's is_active status so re-subscriptions are synced back correctly
            conn.execute("UPDATE newsletter_subscribers SET nombre = ?, is_active = ? WHERE id = ?", (nombre, is_active, existing['id']))
            updated += 1
        else:
            if created_at:
                conn.execute("INSERT INTO newsletter_subscribers (nombre, email, is_active, created_at) VALUES (?, ?, ?, ?)", (nombre, email, is_active, created_at))
            else:
                conn.execute("INSERT INTO newsletter_subscribers (nombre, email, is_active, created_at) VALUES (?, ?, ?, ?)", (nombre, email, is_active, get_mexico_now_str()))
            added += 1

    conn.commit()
    conn.close()

    success_msg = f'¡Sincronización completada con éxito vía {sync_source}! Se descargaron {added} suscriptores nuevos y se actualizaron {updated} existentes desde {remote_url}.'
    if request.is_json or request.headers.get('Accept') == 'application/json':
        return jsonify({'status': 'success', 'message': success_msg, 'added': added, 'updated': updated, 'total': len(subscribers)})

    flash(success_msg, 'success')
    return redirect(url_for('admin_dashboard') + '#sec-sync-remote')


@app.route('/admin/newsletter/import_csv', methods=['POST'])
def admin_newsletter_import_csv():
    if session.get('role') not in ['admin', 'root']:
        flash('Acceso denegado', 'error')
        return redirect(url_for('admin_dashboard'))

    if 'csv_file' not in request.files:
        flash('Por favor selecciona un archivo CSV.', 'error')
        return redirect(url_for('admin_dashboard') + '#tab-newsletter')

    file = request.files['csv_file']
    if not file or file.filename == '':
        flash('Por favor selecciona un archivo CSV válido.', 'error')
        return redirect(url_for('admin_dashboard') + '#tab-newsletter')

    import csv
    import io

    try:
        content = file.stream.read().decode('utf-8', errors='ignore')
        stream = io.StringIO(content, newline=None)
        reader = csv.reader(stream)

        headers = next(reader, None)
        if not headers:
            flash('El archivo CSV está vacío.', 'error')
            return redirect(url_for('admin_dashboard') + '#tab-newsletter')

        email_idx = -1
        name_idx = -1
        date_idx = -1

        for i, h in enumerate(headers):
            h_clean = h.strip().lower()
            if 'email' in h_clean or 'correo' in h_clean:
                email_idx = i
            elif 'nombre' in h_clean or 'name' in h_clean or 'usuario' in h_clean:
                name_idx = i
            elif 'fecha' in h_clean or 'date' in h_clean or 'created' in h_clean:
                date_idx = i

        rows_to_process = []
        # Si la cabecera es en realidad una fila con datos (ej. contiene un correo)
        if any('@' in cell for cell in headers):
            rows_to_process.append(headers)
            if email_idx == -1:
                for idx, cell in enumerate(headers):
                    if '@' in cell:
                        email_idx = idx
                        break

        if email_idx == -1:
            if len(headers) >= 3 and '@' in headers[2]:
                email_idx = 2
                name_idx = 1
            elif len(headers) >= 2 and '@' in headers[1]:
                email_idx = 1
                name_idx = 0
            else:
                email_idx = 0

        for row in reader:
            if row:
                rows_to_process.append(row)

        conn = get_db_connection()
        added = 0
        updated = 0

        for r in rows_to_process:
            if len(r) <= email_idx:
                continue
            email = r[email_idx].strip().lower()
            if not email or '@' not in email:
                continue

            nombre = r[name_idx].strip() if name_idx >= 0 and len(r) > name_idx and r[name_idx].strip() else 'Berserker'
            created_at = r[date_idx].strip() if date_idx >= 0 and len(r) > date_idx and r[date_idx].strip() else None

            cur = conn.execute("SELECT id FROM newsletter_subscribers WHERE email = ?", (email,))
            existing = cur.fetchone()
            if existing:
                conn.execute("UPDATE newsletter_subscribers SET nombre = ?, is_active = 1 WHERE id = ?", (nombre, existing['id']))
                updated += 1
            else:
                if created_at:
                    conn.execute("INSERT INTO newsletter_subscribers (nombre, email, is_active, created_at) VALUES (?, ?, 1, ?)", (nombre, email, created_at))
                else:
                    conn.execute("INSERT INTO newsletter_subscribers (nombre, email, is_active, created_at) VALUES (?, ?, 1, ?)", (nombre, email, get_mexico_now_str()))
                added += 1

        conn.commit()
        conn.close()

        flash(f'¡Importación completada! Se registraron {added} nuevos suscriptores y se actualizaron {updated}.', 'success')
    except Exception as e:
        flash(f'Error al procesar el archivo CSV: {str(e)}', 'error')

    return redirect(url_for('admin_dashboard') + '#tab-newsletter')

if __name__ == '__main__':
    app.run(debug=True, port=5001)

