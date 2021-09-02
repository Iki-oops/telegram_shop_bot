import sqlite3


class Database:
    def __init__(self, path_to_db='data/main.db'):
        self.path_to_db = path_to_db

    @staticmethod
    def logger(statement):
        print("-------------------------------------------\n"
              "Executing:\n"
              f"{statement}\n"
              "-------------------------------------------")

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    @staticmethod
    def format_args(sql: str, parameters: dict):
        sql += " AND ".join([f"{key}=?" for key in parameters])
        return sql, tuple(parameters.values())

    def execute(self, sql: str, parameters: tuple = None,
                fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = tuple()
        data = None
        connection = self.connection
        connection.set_trace_callback(self.logger)
        cursor = connection.cursor()
        cursor.execute(sql, parameters)
        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()
        return data

    # Команды для пользователей
    def create_table_users(self):
        sql = """
CREATE TABLE users (
telegram_id int NOT NULL,
name varchar(100) NOT NULL,
allowed BIT NOT NULL DEFAULT 0,
referrer int,
money int,
PRIMARY KEY (telegram_id)
);
        """
        self.execute(sql, commit=True)

    def add_user(self, telegram_id: int, name: str, allowed: int = 0, referrer: int = None, money: int = 0):
        sql = "INSERT INTO users VALUES (?, ?, ?, ?, ?);"
        parameters = (telegram_id, name, allowed, referrer, money)
        self.execute(sql, parameters, commit=True)

    def update_user(self, telegram_id: int, **kwargs):
        sql = "UPDATE users SET "
        sql += ', '.join([f'{item} = ?' for item in kwargs])
        sql += f" WHERE telegram_id = {telegram_id};"
        parameters = tuple(kwargs.values())
        return self.execute(sql, parameters, commit=True)

    def select_user(self, telegram_id: int):
        sql = "SELECT * FROM users WHERE telegram_id = ?;"
        return self.execute(sql, (telegram_id,), fetchone=True)

    def select_all_users(self):
        sql = "SELECT * FROM users;"
        return self.execute(sql, fetchall=True)

    # Команды для товаров
    def create_table_products(self):
        sql = """
CREATE TABLE products (
id int NOT NULL,
title varchar(100) NOT NULL,
description varchar(255) NOT NULL,
photo_url varchar(255) NOT NULL,
price int NOT NULL,
PRIMARY KEY (id)
);
        """
        self.execute(sql, commit=True)

    def add_product(self, id: int, title: str, description: str, photo_url: str, price: int):
        sql = "INSERT INTO products VALUES (?, ?, ?, ?, ?);"
        parameters = (id, title, description, photo_url, price)
        self.execute(sql, parameters, commit=True)

    def select_all_products(self):
        sql = "SELECT * FROM products ORDER BY title;"
        return self.execute(sql, fetchall=True)

    def select_product(self, **kwargs):
        sql = "SELECT * FROM products WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters, fetchone=True)

    def count_products(self):
        sql = "SELECT COUNT(*) FROM products;"
        return self.execute(sql, fetchone=True)

    def update_product(self, id: int, **kwargs):
        sql = "UPDATE products SET "
        sql += ', '.join([f'{item}=?' for item in kwargs])
        sql += f" WHERE id = {id}"
        parameters = tuple(kwargs.values())
        self.execute(sql, parameters, commit=True)

    def search_product(self, text: str):
        sql = f"SELECT * FROM products WHERE LOWER(title) LIKE LOWER('%{text}%') OR LOWER(description) LIKE LOWER('%{text}%')"
        return self.execute(sql, fetchall=True)

    # Удаление
    def delete_products(self):
        self.execute('DELETE FROM products WHERE TRUE;')
