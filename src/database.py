import sqlite3
from pathlib import Path

from src.config import DATA_DIR


DB_PATH = DATA_DIR / "metricmind.db"


def get_connection():
    """Create and return a database connection."""
    connection = sqlite3.connect(DB_PATH)
    return connection


def initialize_database():
    """Create the required database tables."""

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            value REAL NOT NULL,
            category TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    initialize_database()
    print(f"Database created successfully at: {DB_PATH}")