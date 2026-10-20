DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS accounts;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS roles;

CREATE TABLE roles (
    userroleID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE accounts (
    accountID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    balance REAL NOT NULL DEFAULT 0.0
);

CREATE TABLE categories (
    categoryID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE users (
    iduserID INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    salary REAL NOT NULL DEFAULT 0.0,
    userrole INTEGER NOT NULL,
    FOREIGN KEY (userrole) REFERENCES roles (userroleID)
);

CREATE TABLE transactions (
    transactionID INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL,
    type TEXT NOT NULL CHECK(type IN ('доход', 'расход')),
    createdAt TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    accountID INTEGER NOT NULL,
    categoryID INTEGER NOT NULL,
    FOREIGN KEY (accountID) REFERENCES accounts (accountID),
    FOREIGN KEY (categoryID) REFERENCES categories (categoryID)
);

INSERT INTO roles (name) VALUES ('Руководитель'), ('Бухгалтер');

INSERT INTO users (login, password_hash, salary, userrole) VALUES 
('boss', 'hash_admin123', 150000.0, 1),
('accountant', 'hash_cashier777', 85000.0, 2);

INSERT INTO accounts (name, balance) VALUES 
('Основной расчетный счет', 500000.0),
('Касса офиса', 50000.0);

INSERT INTO categories (name) VALUES 
('Выплата зарплаты'),
('Аренда офиса'),
('Поступление от клиентов');

INSERT INTO transactions (amount, type, account_id, category_id) VALUES 
(120000.0, 'доход', 1, 3),
(45000.0, 'расход', 1, 2);
