from dataclasses import dataclass

@dataclass
class User:
    iduserID: int
    login: str
    password_hash: str
    salary: float
    userrole: int
    role_name: str | None = None