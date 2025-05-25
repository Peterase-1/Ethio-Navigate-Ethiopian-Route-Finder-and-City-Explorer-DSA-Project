import sqlite3
import os
from pathlib import Path

# Database path
DB_PATH = Path(__file__).resolve().parent.parent / "ethio_navigator.db"

def initialize_database():
    """Initialize the database by creating necessary tables if they don't exist."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # Create edges table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS edges (
                from_city TEXT,
                to_city TEXT,
                distance INTEGER,
                PRIMARY KEY (from_city, to_city)
            )
        """)
        # Create heritages table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS heritages (
                name TEXT,
                city TEXT,
                PRIMARY KEY (name, city)
            )
        """)
        # Create visitors table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS visitors (
                city TEXT PRIMARY KEY,
                count INTEGER DEFAULT 0
            )
        """)
        # Create settings table for storing admin password
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        # Insert default admin password if it doesn't exist
        cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", ("admin_password", "admin123"))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")
    finally:
        conn.close()

def save_edges(edges):
    """
    Save edges to the database, ensuring each edge is stored only once.
    Args:
        edges: List of tuples (from_city, to_city, distance)
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # Clear existing edges
        cursor.execute("DELETE FROM edges")
        # Normalize edges: store only one direction (from_city < to_city)
        unique_edges = []
        seen = set()
        for from_city, to_city, distance in edges:
            # Sort the cities to ensure consistent direction
            city_pair = tuple(sorted([from_city, to_city]))
            if city_pair not in seen:
                seen.add(city_pair)
                # Ensure from_city is lexicographically less than to_city
                if from_city < to_city:
                    unique_edges.append((from_city, to_city, distance))
                else:
                    unique_edges.append((to_city, from_city, distance))
        # Insert normalized edges
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
    """Load edges from the database, duplicating them for undirected graph."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT from_city, to_city, distance FROM edges")
        edges = cursor.fetchall()
        # Since edges are stored in one direction, duplicate them for undirected graph
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
    """Save a heritage site to the database."""
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
    """Load heritage sites from the database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name, city FROM heritages")
        heritages = cursor.fetchall()
        return heritages
    except sqlite3.Error as e:
        print(f"Error loading heritages: {e}")
        return []
    finally:
        conn.close()

def load_visitors():
    """Load visitor counts from the database."""
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
    """Save visitor counts to the database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # Clear existing visitor counts
        cursor.execute("DELETE FROM visitors")
        # Insert updated counts
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
    """Reset visitor counts in the database."""
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
    """Load the admin password from the database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = 'admin_password'")
        result = cursor.fetchone()
        return result[0] if result else "admin123"  # Default password if not found
    except sqlite3.Error as e:
        print(f"Error loading password: {e}")
        return "admin123"  # Fallback to default
    finally:
        conn.close()

def backup_database(force=False):
    """Backup the database."""
    return True  # Placeholder

def restore_database():
    """Restore the database."""
    return True  # Placeholder

def close_db_connection():
    """Close the database connection (not needed since we close in each function)."""
    pass  # Placeholder