import sqlite3
import hashlib
import os
import datetime

def get_db_connection():
    conn = sqlite3.connect('user_database.db')
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        salt TEXT NOT NULL,
        is_admin BOOLEAN DEFAULT 0,
        status TEXT DEFAULT 'active',
        expiration_date TEXT DEFAULT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    
    cursor.execute("SELECT COUNT(*) FROM users WHERE is_admin = 1")
    admin_count = cursor.fetchone()[0]
    
    if admin_count == 0:
        create_admin_user(conn)
    
    conn.close()

def create_admin_user(conn=None):
    should_close = False
    if conn is None:
        conn = get_db_connection()
        should_close = True
    
    cursor = conn.cursor()
    
    admin_username = "admin"
    admin_password = "admin123"
    
    cursor.execute("SELECT username FROM users WHERE username = ?", (admin_username,))
    if cursor.fetchone():
        if should_close:
            conn.close()
        return
    
    password_hash, salt = hash_password(admin_password)
    
    cursor.execute(
        "INSERT INTO users (username, password_hash, salt, is_admin) VALUES (?, ?, ?, 1)",
        (admin_username, password_hash, salt)
    )
    
    conn.commit()
    if should_close:
        conn.close()

def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(32)
    
    password_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000
    )
    
    return password_hash.hex(), salt.hex()

def create_user(username, password, is_admin=False, expiration_days=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            conn.close()
            return False, "Username already exists"
        
        password_hash, salt = hash_password(password)
        
        expiration_date = None
        if expiration_days:
            expiration_date = (datetime.datetime.now() + datetime.timedelta(days=expiration_days)).strftime('%Y-%m-%d')
        
        cursor.execute(
            "INSERT INTO users (username, password_hash, salt, is_admin, expiration_date) VALUES (?, ?, ?, ?, ?)",
            (username, password_hash, salt, 1 if is_admin else 0, expiration_date)
        )
        
        conn.commit()
        conn.close()
        return True, "User created successfully"
    
    except Exception as e:
        conn.close()
        return False, f"Error: {str(e)}"

def authenticate_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "SELECT id, password_hash, salt, is_admin, status, expiration_date FROM users WHERE username = ?",
            (username,)
        )
        
        user = cursor.fetchone()
        
        if not user:
            conn.close()
            return False, "Invalid username or password", None
        
        if user['status'] == 'banned':
            conn.close()
            return False, "Your account has been banned", None
        
        if user['expiration_date']:
            expiration_date = datetime.datetime.strptime(user['expiration_date'], '%Y-%m-%d')
            if datetime.datetime.now() > expiration_date:
                cursor.execute("UPDATE users SET status = 'expired' WHERE id = ?", (user['id'],))
                conn.commit()
                conn.close()
                return False, "Your account has expired", None
        
        stored_password_hash = user['password_hash']
        salt = bytes.fromhex(user['salt'])
        is_admin = bool(user['is_admin'])
        
        calculated_hash, _ = hash_password(password, salt)
        
        if calculated_hash == stored_password_hash:
            conn.close()
            return True, "Authentication successful", is_admin
        else:
            conn.close()
            return False, "Invalid username or password", None
    
    except Exception as e:
        conn.close()
        return False, f"Error: {str(e)}", None

def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "SELECT id, username, is_admin, status, expiration_date, created_at FROM users ORDER BY username"
        )
        
        users = cursor.fetchall()
        conn.close()
        
        return users
    
    except Exception as e:
        conn.close()
        return []

def update_user_status(username, status):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("UPDATE users SET status = ? WHERE username = ?", (status, username))
        conn.commit()
        conn.close()
        return True, f"User status updated to {status}"
    
    except Exception as e:
        conn.close()
        return False, f"Error: {str(e)}"

def update_user_expiration(username, expiration_days):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        expiration_date = None
        if expiration_days:
            expiration_date = (datetime.datetime.now() + datetime.timedelta(days=expiration_days)).strftime('%Y-%m-%d')
        
        cursor.execute("UPDATE users SET expiration_date = ? WHERE username = ?", (expiration_date, username))
        conn.commit()
        conn.close()
        
        if expiration_date:
            return True, f"User expiration set to {expiration_date}"
        else:
            return True, "User expiration removed"
    
    except Exception as e:
        conn.close()
        return False, f"Error: {str(e)}"

def delete_user(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if not user:
            conn.close()
            return False, "User not found"

        cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        conn.commit()
        conn.close()
        
        return True, f"User {username} has been deleted"
    
    except Exception as e:
        conn.close()
        return False, f"Error: {str(e)}"
