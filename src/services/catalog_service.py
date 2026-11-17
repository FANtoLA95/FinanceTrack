from repositories import account_repository, category_repository
from models.account import Account
from models.category import Category

def create_account(name: str, initial_balance: float = 0.0) -> Account:
    if not name or not name.strip():
        raise Exception("Название счета не может быть пустым.")
    if initial_balance < 0:
        raise Exception("Начальный баланс не может быть отрицательным.")
    if account_repository.get_by_name(name):
        raise Exception(f"Счет с названием '{name}' уже существует.")
        
    return account_repository.create(name.strip(), initial_balance)

def get_all_accounts() -> list[Account]:
    return account_repository.get_all()

def create_category(name: str) -> Category:
    if not name or not name.strip():
        raise Exception("Название категории не может быть пустым.")
    if category_repository.get_by_name(name):
        raise Exception(f"Категория '{name}' уже существует.")
        
    return category_repository.create(name.strip())

def get_all_categories() -> list[Category]:
    return category_repository.get_all()