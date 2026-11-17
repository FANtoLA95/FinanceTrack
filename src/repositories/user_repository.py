from database.database import get_connection
from models.user import User

def _map(row) -> User | None:
    if row is None:
        return None
    return User(
        iduserID=row[0],
        login=row[1],
        password_hash=row[2],
        salary=row[3],
        userrole=row[4],
        role_name=row[5] if len(row) > 5 else None
    )

def create(login: str, password_hash: str, salary: float, role_id: int) -> User:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (login, password_hash, salary, userrole) VALUES (?, ?, ?, ?)",
        (login, password_hash, salary, role_id)
    )
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return get_by_id(user_id)

def get_by_id(user_id: int) -> User | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.iduserID, u.login, u.password_hash, u.salary, u.userrole, r.name 
        FROM users u
        JOIN roles r ON u.userrole = r.userroleID
        WHERE u.iduserID = ?
    """, (user_id,))
    row = cursor.fetchone()
    conn.close()
    return _map(row)

def get_by_login(login: str) -> User | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.iduserID, u.login, u.password_hash, u.salary, u.userrole, r.name 
        FROM users u
        JOIN roles r ON u.userrole = r.userroleID
        WHERE u.login = ?
    """, (login,))
    row = cursor.fetchone()
    conn.close()
    return _map(row)

def get_all() -> list[User]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.iduserID, u.login, u.password_hash, u.salary, u.userrole, r.name 
        FROM users u
        JOIN roles r ON u.userrole = r.userroleID
    """)
    rows = cursor.fetchall()
    conn.close()
    return [_map(row) for row in rows]

def update_salary(user_id: int, new_salary: float) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET salary = ? WHERE iduserID = ?", (new_salary, user_id))
    conn.commit()
    conn.close()

def delete(user_id: int) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE iduserID = ?", (user_id,))
    conn.commit()
    conn.close()