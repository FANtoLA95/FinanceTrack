import sqlite3
import os

def init_db():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, 'database', 'finance.db')
    schema_path = os.path.join(current_dir, 'database', 'schema.sql')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    print("Инициализация базы данных FinanceTrack...")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        with open(schema_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        cursor.executescript(sql_script)
        conn.commit()
        conn.close()
        print(f"Файл базы данных успешно создан: {db_path}")
    except Exception as e:
        print(f"Ошибка при инициализации базы данных: {e}")
if __name__ == "__main__":
    init_db()