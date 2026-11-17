from database.database import get_connection
from models.account import Account

def _map(row) -> Account | None:
    if row is None:
        return None
    return Account(accountID=row[0], name=row[1], balance=row[2])

def create(name: str, balance: float = 0.0) -> Account:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO accounts (name, balance) VALUES (?, ?)", (name, balance))
    acc_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return get_by_id(acc_id)

def get_by_id(account_id: int) -> Account | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT accountID, name, balance FROM accounts WHERE accountID = ?", (account_id,))
    row = cursor.fetchone()
    conn.close()
    return _map(row)

def get_by_name(name: str) -> Account | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT accountID, name, balance FROM accounts WHERE name = ?", (name,))
    row = cursor.fetchone()
    conn.close()
    return _map(row)

def get_all() -> list[Account]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT accountID, name, balance FROM accounts")
    rows = cursor.fetchall()
    conn.close()
    return [_map(row) for row in rows]

def update_balance(account_id: int, new_balance: float) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE accounts SET balance = ? WHERE accountID = ?", (new_balance, account_id))
    conn.commit()
    conn.close()

def delete(account_id: int) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM accounts WHERE accountID = ?", (account_id,))
    conn.commit()
    conn.close()