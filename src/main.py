import os
import sqlite3
from ui.menu import auth_menu, main_menu

def ensure_db_initialized():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, 'database', 'finance.db')
    schema_path = os.path.join(current_dir, 'database', 'schema.sql')

    if not os.path.exists(db_path):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        conn = sqlite3.connect(db_path)
        with open(schema_path, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()

def run():
    ensure_db_initialized()
    while True:
        user = auth_menu()
        if user is None:
            print("Работа приложения завершена.")
            break
        main_menu(user)

if __name__ == "__main__":
    run()