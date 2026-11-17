from repositories import transaction_repository, account_repository, category_repository
from models.transaction import Transaction
from models.user import User

def add_transaction(amount: float, trans_type: str, account_id: int, category_id: int) -> Transaction:
    if amount <= 0:
        raise Exception("Сумма операции должна быть больше нуля.")
    if trans_type not in ("доход", "расход"):
        raise Exception("Тип операции должен быть строго 'доход' или 'расход'.")
        
    account = account_repository.get_by_id(account_id)
    if not account:
        raise Exception("Выбранный счет не найден.")
        
    category = category_repository.get_by_id(category_id)
    if not category:
        raise Exception("Выбранная категория не найдена.")
        
    if trans_type == "расход":
        if amount > account.balance:
            raise Exception(f"Недостаточно средств на счете '{account.name}'. Доступно: {account.balance} руб.")
        new_balance = account.balance - amount
    else:
        new_balance = account.balance + amount
        
    transaction = transaction_repository.create(amount, trans_type, account_id, category_id)
    account_repository.update_balance(account_id, new_balance)
    
    return transaction

def get_history() -> list[Transaction]:
    return transaction_repository.get_all()

def generate_summary_report(current_user: User) -> dict:
    if current_user.role_name != "Руководитель":
        raise Exception("Доступ запрещен: сводный отчет доступен только Руководителю.")
        
    transactions = transaction_repository.get_all()
    accounts = account_repository.get_all()
    
    total_income = sum(t.amount for t in transactions if t.type == "доход")
    total_expense = sum(t.amount for t in transactions if t.type == "расход")
    net_profit = total_income - total_expense
    total_balance = sum(a.balance for a in accounts)
    
    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_profit": net_profit,
        "total_balance": total_balance,
        "operations_count": len(transactions)
    }