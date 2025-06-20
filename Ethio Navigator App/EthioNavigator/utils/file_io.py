import sqlite3
import os
from pathlib import Path
import shutil

DB_PATH = Path(__file__).resolve().parent.parent / "ethio_navigator.db"

def initialize_database():
    try:
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
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", ("admin_password", "admin123"))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")
    finally:
        conn.close()

def save_edges(edges):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM edges")
        unique_edges = []
        seen = set()
        for from_city, to_city, distance in edges:
            city_pair = tuple(sorted([from_city, to_city]))
            if city_pair not in seen:
                seen.add(city_pair)
                if from_city < to_city:
                    unique_edges.append((from_city, to_city, distance))
                else:
                    unique_edges.append((to_city, from_city, distance))
        cursor.executemany(
            "INSERT INTO edges (from_city, to_city, distance) VALUES (?, ?, ?)",
            unique_edges
        )
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error saving edges: {e}")
    finally:
        conn.close()

def load_edges():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT from_city, to_city, distance FROM edges")
        edges = cursor.fetchall()
        undirected_edges = []
        for from_city, to_city, distance in edges:
            undirected_edges.append((from_city, to_city, distance))
            undirected_edges.append((to_city, from_city, distance))
        return undirected_edges
    except sqlite3.Error as e:
        print(f"Error loading edges: {e}")
        return []
    finally:
        conn.close()

def save_heritage(name, city):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO heritages (name, city) VALUES (?, ?)",
            (name, city)
        )
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error saving heritage: {e}")
    finally:
        conn.close()

def load_heritages():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name, city FROM heritages")
        heritages = cursor.fetchall()
        return {city: [name for name, c in heritages if c == city] for city in set(c for _, c in heritages)}
    except sqlite3.Error as e:
        print(f"Error loading heritages: {e}")
        return {}
    finally:
        conn.close()

def load_visitors():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT city, count FROM visitors")
        visitors = dict(cursor.fetchall())
        return visitors
    except sqlite3.Error as e:
        print(f"Error loading visitors: {e}")
        return {}
    finally:
        conn.close()

def save_visitors(visitors):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM visitors")
        cursor.executemany(
            "INSERT INTO visitors (city, count) VALUES (?, ?)",
            [(city, count) for city, count in visitors.items()]
        )
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error saving visitors: {e}")
    finally:
        conn.close()

def reset_visitors():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE visitors SET count = 0")
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error resetting visitors: {e}")
    finally:
        conn.close()

def load_password():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = 'admin_password'")
        result = cursor.fetchone()
        return result[0] if result else "admin123"
    except sqlite3.Error as e:
        print(f"Error loading password: {e}")
        return "admin123"
    finally:
        conn.close()

def backup_database(force=False):
    try:
        backup_path = DB_PATH.with_name(f"ethio_navigator_backup_{Path(__file__).stem}.db")
        if force or not backup_path.exists():
            shutil.copy2(DB_PATH, backup_path)
            return True
        return False
    except Exception as e:
        print(f"Error backing up database: {e}")
        return False

def restore_database():
    try:
        backup_path = DB_PATH.with_name(f"ethio_navigator_backup_{Path(__file__).stem}.db")
        if backup_path.exists():
            shutil.copy2(backup_path, DB_PATH)
            return True
        return False
    except Exception as e:
        print(f"Error restoring database: {e}")
        return False

def close_db_connection():
    pass