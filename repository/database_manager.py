import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'school.db')
SCHEMA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'schema.sql')

class DatabaseManager:
    @staticmethod
    def get_connection():
        # Ensures that the database folder exists
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def initialize_database():
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        if not os.path.exists(DB_PATH):
            conn = DatabaseManager.get_connection()
            with open(SCHEMA_PATH, 'r') as f:
                conn.executescript(f.read())
            conn.commit()
            conn.close()
