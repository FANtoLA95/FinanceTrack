from database.database import get_connection
from models.role import UserRole

def _map(row) -> UserRole | None:
    if row is None:
        return None
    return UserRole(userroleID=row[0], name=row[1])

def get_all() -> list[UserRole]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT userroleID, name FROM roles")
    rows = cursor.fetchall()
    conn.close()
    return [_map(row) for row in rows]

def get_by_id(role_id: int) -> UserRole | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT userroleID, name FROM roles WHERE userroleID = ?", (role_id,))
    row = cursor.fetchone()
    conn.close()
    return _map(row)