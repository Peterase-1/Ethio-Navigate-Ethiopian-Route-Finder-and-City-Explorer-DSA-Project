import sqlite3
import os
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "ethio_navigator.db"
PASSWORD_FILE = Path(__file__).resolve().parent.parent / "data" / "password.txt"

def initialize_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS edges (
            from_city TEXT,
            to_city TEXT,
            distance INTEGER,
            PRIMARY KEY (from_city, to_city)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS heritages (
            name TEXT,
            city TEXT,
            PRIMARY KEY (name, city)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS visitors (
            city TEXT PRIMARY KEY,
            count INTEGER DEFAULT 0
        )
    """)
    # No need for password table since we're using password.txt
    conn.commit()
    conn.close()

def load_password():
    if PASSWORD_FILE.exists():
        with open(PASSWORD_FILE, "r") as f:
            password = f.read().strip()
            return password if password else ""
    return ""  # Default to empty string if file doesn't exist

def load_edges():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT from_city, to_city, distance FROM edges")
    edges = [(row[0], row[1], row[2]) for row in cursor.fetchall()]
    conn.close()
    return edges

def load_heritages():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, city FROM heritages")
    heritages = {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()
    return heritages

def load_visitors():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT city, count FROM visitors")
    visitors = {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()
    return visitors

def save_visitors(visitors):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executemany("INSERT OR REPLACE INTO visitors (city, count) VALUES (?, ?)", visitors.items())
    conn.commit()
    conn.close()

def reset_visitors():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM visitors")
    conn.commit()
    conn.close()

def save_heritage(name, city):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO heritages (name, city) VALUES (?, ?)", (name, city))
    conn.commit()
    conn.close()

def save_edges(edges):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executemany("INSERT OR REPLACE INTO edges (from_city, to_city, distance) VALUES (?, ?, ?)", edges)
    conn.commit()
    conn.close()

def backup_database(force=False):
    if not force and os.path.exists(f"{DB_PATH}.bak"):
        return False
    try:
        os.replace(DB_PATH, f"{DB_PATH}.bak")
        return True
    except Exception:
        return False

def restore_database():
    if os.path.exists(f"{DB_PATH}.bak"):
        try:
            os.replace(f"{DB_PATH}.bak", DB_PATH)
            return True
        except Exception:
            return False
    return False

def close_db_connection():
    pass  # Placeholder if needed