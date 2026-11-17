from dataclasses import dataclass

@dataclass
class Account:
    accountID: int
    name: str
    balance: float