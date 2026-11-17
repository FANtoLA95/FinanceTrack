from dataclasses import dataclass

@dataclass
class Transaction:
    transactionID: int
    amount: float
    type: str
    createdAt: str
    accountID: int
    categoryID: int
    account_name: str | None = None
    category_name: str | None = None