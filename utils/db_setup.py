import sqlite3
from pathlib import Path

def setup_database():
    project_root = Path(__file__).resolve().parent.parent
    db_path = project_root / "data" / "ethio_navigator.db"
    db_path.parent.mkdir(exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cities (
            from_city TEXT,
            to_city TEXT,
            distance INTEGER,
            PRIMARY KEY (from_city, to_city)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS heritages (
            name TEXT,
            city TEXT,
            PRIMARY KEY (name, city)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS visitors (
            city TEXT PRIMARY KEY,
            count INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin_password (
            password TEXT PRIMARY KEY
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            operation TEXT,
            details TEXT,
            timestamp TEXT
        )
    ''')

    # Add indexes for performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_cities_from_city ON cities(from_city)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_cities_to_city ON cities(to_city)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_heritages_city ON heritages(city)')

    # Insert a default admin password if none exists
    cursor.execute("INSERT OR IGNORE INTO admin_password (password) VALUES (?)", ("admin123",))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()