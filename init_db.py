import sqlite3
import os

DB_FILE = 'gothprods.db'

def init_db():
    if os.path.exists(DB_FILE):
        print("Database already exists. Initializing missing tables.")
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Table: users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT,
            role TEXT DEFAULT 'reader',
            is_verified INTEGER DEFAULT 0,
            verification_code TEXT
        )
    ''')

    # Table: section_permissions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS section_permissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            section_name TEXT,
            can_create INTEGER DEFAULT 0,
            can_edit INTEGER DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    # Table: records (For news, agenda, etc. pending approval)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pending_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author_id INTEGER,
            section_name TEXT,
            title TEXT,
            content TEXT,
            status TEXT DEFAULT 'pending', -- pending, approved, rejected
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(author_id) REFERENCES users(id)
        )
    ''')

    # Initialize Root User if not exists
    cursor.execute("SELECT id FROM users WHERE email = 'goth.prods@gmail.com'")
    root_user = cursor.fetchone()
    
    if not root_user:
        cursor.execute("INSERT INTO users (email, role, is_verified) VALUES ('goth.prods@gmail.com', 'root', 1)")
        print("Root user created: goth.prods@gmail.com. Password needs to be set on first login.")
    else:
        print("Root user already exists.")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialization complete.")
