from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Union[None, Pool] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False):
        async with self.pool.acquire() as connection:
            connection: Connection
            result = None
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    @staticmethod
    def format_args(sql: str, parameters: dict):
        sql += ' AND '.join(
            [f"{arg} = ${val}" for val, arg in enumerate(parameters, start=1)]
        )
        return sql, tuple(parameters.values())

# Пользователи
    async def create_table_users(self):
        sql = """
CREATE TABLE IF NOT EXISTS Users (
id SERIAL PRIMARY KEY,
telegram_id int UNIQUE NOT NULL,
name varchar(255) NOT NULL,
allowed boolean NOT NULL default False,
money int default 0,
referrer int
);
    """
        await self.execute(sql, execute=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users;"
        return await self.execute(sql, fetch=True)

    async def select_user(self, telegram_id: int):
        sql = "SELECT * FROM Users WHERE telegram_id=$1"
        return await self.execute(sql, telegram_id, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users;"
        return await self.execute(sql, fetchval=True)

    async def add_user(self,
                       telegram_id: int,
                       name: str,
                       allowed: bool = False,
                       money: int = 10,
                       referrer: int = None):
        sql = "INSERT INTO Users (telegram_id, name, allowed, money, referrer) VALUES ($1, $2, $3, $4, $5)"
        await self.execute(sql, telegram_id, name, allowed, money, referrer, execute=True)

    async def update_user(self, telegram_id, **kwargs):
        sql = "UPDATE Users SET "
        sql += ", ".join([f"{arg}=${val}" for val, arg in enumerate(kwargs, start=1)])
        sql += f" WHERE telegram_id={telegram_id}"
        parameters = tuple(kwargs.values())
        await self.execute(sql, *parameters, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE True;", execute=True)

    async def drop_table_users(self):
        await self.execute("DROP TABLE Users;", execute=True)

# Продукты
    async def create_table_products(self):
        sql = """
CREATE TABLE IF NOT EXISTS Products (
id SERIAL PRIMARY KEY,
title VARCHAR(255) NOT NULL,
description VARCHAR(255) NOT NULL,
photo_url VARCHAR(255) NOT NULL,
price INT NOT NULL
);
        """
        await self.execute(sql, execute=True)

    async def select_all_products(self):
        sql = "SELECT * FROM Products;"
        return await self.execute(sql, fetch=True)

    async def select_product(self, **kwargs):
        sql = "SELECT * FROM Products WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_product(self):
        return await self.execute(
            "SELECT COUNT(*) FROM Products;", fetchval=True
        )

    async def add_product(self,
                          title: str,
                          description: str,
                          photo_url: str,
                          price: int):
        sql = "INSERT INTO Products (title, description, photo_url, price) VALUES ($1, $2, $3, $4);"
        await self.execute(sql, title, description, photo_url, price, execute=True)

    async def update_product(self, id, **kwargs):
        sql = "UPDATE Products SET title=$1 WHERE id=$2"
        sql += ", ".join([f"{arg}=${val}" for val, arg in kwargs])
        sql += f" WHERE id={id}"
        parameters = tuple(kwargs.values())
        await self.execute(sql, *parameters, execute=True)

    async def search_product(self, text: str):
        sql = (f"SELECT * FROM Products WHERE LOWER(title) LIKE LOWER('%{text}%')"
               f"OR LOWER(description) LIKE LOWER('%{text}%')")
        return await self.execute(sql, fetch=True)

    async def delete_products(self):
        await self.execute("DELETE Products WHERE True;", execute=True)

    async def drop_table_products(self):
        await self.execute("DROP TABLE Products;", execute=True)
