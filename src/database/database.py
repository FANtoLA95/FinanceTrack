import sqlite3
import os

def get_connection():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, 'finance.db')
    return sqlite3.connect(db_path)