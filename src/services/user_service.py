from repositories import user_repository, role_repository
from models.user import User

def login(login_str: str, password: str) -> User:
    if not login_str or not password:
        raise Exception("Логин и пароль не могут быть пустыми.")
    
    user = user_repository.get_by_login(login_str)
    if not user:
        raise Exception("Пользователь с таким логином не найден.")
    
    if user.password_hash != password and user.password_hash != f"hash_{password}":
        raise Exception("Неверный пароль.")
    
    return user

def register_employee(current_user: User, new_login: str, password: str, salary: float, role_id: int) -> User:
    if current_user.role_name != "Руководитель":
        raise Exception("Доступ запрещен: добавлять сотрудников может только Руководитель.")
    
    if not new_login or not password:
        raise Exception("Логин и пароль обязательны для заполнения.")
    
    if salary < 0:
        raise Exception("Оклад не может быть отрицательным.")
        
    if user_repository.get_by_login(new_login):
        raise Exception(f"Пользователь с логином '{new_login}' уже существует.")
        
    role = role_repository.get_by_id(role_id)
    if not role:
        raise Exception("Указанная роль не существует.")
        
    return user_repository.create(new_login, f"hash_{password}", salary, role_id)

def get_all_employees(current_user: User) -> list[User]:
    if current_user.role_name != "Руководитель":
        raise Exception("Доступ запрещен: просматривать список персонала может только Руководитель.")
    return user_repository.get_all()

def delete_employee(current_user: User, target_user_id: int) -> None:
    if current_user.role_name != "Руководитель":
        raise Exception("Доступ запрещен: удалять сотрудников может только Руководитель.")
        
    if current_user.iduserID == target_user_id:
        raise Exception("Нельзя удалить самого себя.")
        
    target_user = user_repository.get_by_id(target_user_id)
    if not target_user:
        raise Exception("Сотрудник с таким ID не найден.")
        
    user_repository.delete(target_user_id)