from database.database import get_connection
from models.transaction import Transaction

def _map(row) -> Transaction | None:
    if row is None:
        return None
    return Transaction(
        transactionID=row[0],
        amount=row[1],
        type=row[2],
        createdAt=row[3],
        accountID=row[4],
        categoryID=row[5],
        account_name=row[6] if len(row) > 6 else None,
        category_name=row[7] if len(row) > 7 else None
    )

def create(amount: float, trans_type: str, account_id: int, category_id: int) -> Transaction:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO transactions (amount, type, accountID, categoryID) VALUES (?, ?, ?, ?)",
        (amount, trans_type, account_id, category_id)
    )
    trans_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return get_by_id(trans_id)

def get_by_id(trans_id: int) -> Transaction | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.transactionID, t.amount, t.type, t.createdAt, t.accountID, t.categoryID,
               a.name, c.name
        FROM transactions t
        JOIN accounts a ON t.accountID = a.accountID
        JOIN categories c ON t.categoryID = c.categoryID
        WHERE t.transactionID = ?
    """, (trans_id,))
    row = cursor.fetchone()
    conn.close()
    return _map(row)

def get_all() -> list[Transaction]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.transactionID, t.amount, t.type, t.createdAt, t.accountID, t.categoryID,
               a.name, c.name
        FROM transactions t
        JOIN accounts a ON t.accountID = a.accountID
        JOIN categories c ON t.categoryID = c.categoryID
        ORDER BY t.createdAt DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [_map(row) for row in rows]

def delete(trans_id: int) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE transactionID = ?", (trans_id,))
    conn.commit()
    conn.close()