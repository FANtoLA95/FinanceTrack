from database.database import get_connection
from models.category import Category

def _map(row) -> Category | None:
    if row is None:
        return None
    return Category(categoryID=row[0], name=row[1])

def create(name: str) -> Category:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))
    cat_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return get_by_id(cat_id)

def get_by_id(category_id: int) -> Category | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT categoryID, name FROM categories WHERE categoryID = ?", (category_id,))
    row = cursor.fetchone()
    conn.close()
    return _map(row)

def get_by_name(name: str) -> Category | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT categoryID, name FROM categories WHERE name = ?", (name,))
    row = cursor.fetchone()
    conn.close()
    return _map(row)

def get_all() -> list[Category]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT categoryID, name FROM categories")
    rows = cursor.fetchall()
    conn.close()
    return [_map(row) for row in rows]

def delete(category_id: int) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM categories WHERE categoryID = ?", (category_id,))
    conn.commit()
    conn.close()