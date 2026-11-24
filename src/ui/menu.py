from services import user_service, catalog_service, transaction_service
from repositories import role_repository
from models.user import User
from services import user_service, catalog_service, transaction_service, export_service

def auth_menu() -> User | None:
    while True:
        print("\n=== СИСТЕМА FINANCETRACK ===")
        print("1. Войти в систему")
        print("2. Регистрация нового руководителя")
        print("0. Выход")
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            login_str = input("Введите логин: ").strip()
            password = input("Введите пароль: ").strip()
            try:
                user = user_service.login(login_str, password)
                print(f"\nДобро пожаловать, {user.login}! Ваша роль: {user.role_name}")
                return user
            except Exception as e:
                print(f"\n[Ошибка входа]: {e}")

        elif choice == "2":
            login_str = input("Придумайте логин: ").strip()
            password = input("Придумайте пароль: ").strip()
            try:
                salary = float(input("Укажите оклад (руб.): "))
                temp_admin = User(0, "system", "", 0.0, 1, "Руководитель")
                user = user_service.register_employee(temp_admin, login_str, password, salary, 1)
                print(f"\nРуководитель '{user.login}' успешно зарегистрирован! Теперь войдите в систему.")
            except ValueError:
                print("\n[Ошибка]: Оклад должен быть числом.")
            except Exception as e:
                print(f"\n[Ошибка регистрации]: {e}")

        elif choice == "0":
            return None
        else:
            print("Неверный ввод. Попробуйте снова.")

def main_menu(current_user: User):
    while True:
        print(f"\n--- ГЛАВНОЕ МЕНЮ ({current_user.login} | {current_user.role_name}) ---")
        print("1. Меню транзакций (доходы/расходы и история)")
        print("2. Меню справочников и счетов")

        if current_user.role_name == "Руководитель":
            print("3. Сформировать сводный отчёт")
            print("4. Управлять пользователями (персоналом)")

        print("5. Экспорт транзакций (JSON, CSV, XML, YAML)")
        print("0. Выйти из аккаунта")
        choice = input("Выберите раздел: ").strip()

        if choice == "1":
            transactions_menu()
        elif choice == "2":
            catalogs_menu()
        elif choice == "3" and current_user.role_name == "Руководитель":
            show_report(current_user)
        elif choice == "4" and current_user.role_name == "Руководитель":
            users_menu(current_user)
        elif choice == "5":
            try:
                out_path = export_service.export_all_formats()
                print(f"\n[Успех]: Файлы data.json, data.csv, data.xml и data.yaml созданы в папке:\n{out_path}")
            except Exception as e:
                print(f"\n[Ошибка экспорта]: {e}")
        elif choice == "0":
            print("Выход из аккаунта...")
            break
        else:
            print("Неверный выбор или недостаточно прав доступа.")

def transactions_menu():
    while True:
        print("\n--- МЕНЮ ТРАНЗАКЦИЙ ---")
        print("1. Внести доход или расход")
        print("2. Просмотреть историю операций")
        print("0. Назад")
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            try:
                accounts = catalog_service.get_all_accounts()
                if not accounts:
                    print("Сначала создайте хотя бы один счет в меню справочников!")
                    continue
                print("\nДоступные счета:")
                for acc in accounts:
                    print(f"  ID: {acc.accountID} | {acc.name} (Баланс: {acc.balance} руб.)")
                acc_id = int(input("Введите ID счета: "))

                categories = catalog_service.get_all_categories()
                if not categories:
                    print("Сначала создайте хотя бы одну категорию!")
                    continue
                print("\nДоступные категории:")
                for cat in categories:
                    print(f"  ID: {cat.categoryID} | {cat.name}")
                cat_id = int(input("Введите ID категории: "))

                t_type = input("Тип операции (введите 'доход' или 'расход'): ").strip().lower()
                amount = float(input("Введите сумму: "))

                transaction_service.add_transaction(amount, t_type, acc_id, cat_id)
                print("\n[Успех]: Операция успешно проведена!")
            except ValueError:
                print("\n[Ошибка]: ID и сумма должны быть числами.")
            except Exception as e:
                print(f"\n[Ошибка операции]: {e}")

        elif choice == "2":
            history = transaction_service.get_history()
            print("\n--- ИСТОРИЯ ОПЕРАЦИЙ ---")
            if not history:
                print("Операций пока нет.")
            for t in history:
                print(f"[{t.createdAt}] {t.type.upper()}: {t.amount} руб. | Счет: {t.account_name} | Категория: {t.category_name}")

        elif choice == "0":
            break

def catalogs_menu():
    while True:
        print("\n--- СПРАВОЧНИКИ И СЧЕТА ---")
        print("1. Просмотреть баланс счетов")
        print("2. Создать внутренний счет")
        print("3. Добавить новую категорию")
        print("4. Показать все категории")
        print("0. Назад")
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            accounts = catalog_service.get_all_accounts()
            print("\n--- ТЕКУЩИЕ СЧЕТА ---")
            for acc in accounts:
                print(f"ID: {acc.accountID} | {acc.name} — {acc.balance} руб.")

        elif choice == "2":
            name = input("Введите название нового счета: ")
            try:
                balance = float(input("Введите начальный баланс (руб.): "))
                acc = catalog_service.create_account(name, balance)
                print(f"\n[Успех]: Счет '{acc.name}' создан!")
            except ValueError:
                print("\n[Ошибка]: Баланс должен быть числом.")
            except Exception as e:
                print(f"\n[Ошибка]: {e}")

        elif choice == "3":
            name = input("Введите название новой категории: ")
            try:
                cat = catalog_service.create_category(name)
                print(f"\n[Успех]: Категория '{cat.name}' добавлена!")
            except Exception as e:
                print(f"\n[Ошибка]: {e}")

        elif choice == "4":
            categories = catalog_service.get_all_categories()
            print("\n--- КАТЕГОРИИ ---")
            for cat in categories:
                print(f"ID: {cat.categoryID} | {cat.name}")

        elif choice == "0":
            break

def show_report(current_user: User):
    try:
        report = transaction_service.generate_summary_report(current_user)
        print("\n=== СВОДНЫЙ ФИНАНСОВЫЙ ОТЧЁТ ===")
        print(f"Всего операций проведено: {report['operations_count']}")
        print(f"Общие доходы:             +{report['total_income']} руб.")
        print(f"Общие расходы:            -{report['total_expense']} руб.")
        print(f"Чистая прибыль:           {report['net_profit']} руб.")
        print(f"Общий остаток на счетах:  {report['total_balance']} руб.")
    except Exception as e:
        print(f"\n[Ошибка]: {e}")

def users_menu(current_user: User):
    while True:
        print("\n--- УПРАВЛЕНИЕ ПЕРСОНАЛОМ ---")
        print("1. Список сотрудников")
        print("2. Добавить нового сотрудника")
        print("3. Удалить сотрудника")
        print("0. Назад")
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            try:
                users = user_service.get_all_employees(current_user)
                print("\n--- СОТРУДНИКИ ---")
                for u in users:
                    print(f"ID: {u.iduserID} | Логин: {u.login} | Роль: {u.role_name} | Оклад: {u.salary} руб.")
            except Exception as e:
                print(f"\n[Ошибка]: {e}")

        elif choice == "2":
            try:
                roles = role_repository.get_all()
                print("\nДоступные роли:")
                for r in roles:
                    print(f"  ID: {r.userroleID} | {r.name}")
                role_id = int(input("Введите ID роли: "))
                login_str = input("Введите логин сотрудника: ").strip()
                password = input("Введите пароль: ").strip()
                salary = float(input("Введите оклад (руб.): "))

                new_user = user_service.register_employee(current_user, login_str, password, salary, role_id)
                print(f"\n[Успех]: Сотрудник '{new_user.login}' добавлен!")
            except ValueError:
                print("\n[Ошибка]: ID роли и оклад должны быть числами.")
            except Exception as e:
                print(f"\n[Ошибка]: {e}")

        elif choice == "3":
            try:
                target_id = int(input("Введите ID сотрудника для удаления: "))
                user_service.delete_employee(current_user, target_id)
                print("\n[Успех]: Сотрудник удалён из системы.")
            except ValueError:
                print("\n[Ошибка]: ID должен быть числом.")
            except Exception as e:
                print(f"\n[Ошибка]: {e}")

        elif choice == "0":
            break