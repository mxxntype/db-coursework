import os
import random
import string
from logging import Logger

import psycopg2 as postgresql
from log import create_named_logger


class DatabaseConnection:
    logger: Logger = create_named_logger("DB")
    db_connection: postgresql.extensions.connection

    def __init__(
        self,
        db_name: str = os.environ["DB_NAME"],
        db_user: str = os.environ["DB_USER"],
        db_passwd: str = os.environ["DB_PASSWORD"],
        db_host: str = "localhost",
        db_port: int = 5432,
    ) -> None:
        meta: str = f"'{db_user}@{db_host}:{db_port}'"
        self.logger.info(f"Logging into PostgreSQL: {meta}")
        try:
            self.db_connection = postgresql.connect(
                database=db_name,
                user=db_user,
                password=db_passwd,
                host=db_host,
                port=db_port,
            )
        except Exception as error:
            error = str(error).strip()
            self.logger.error(error)
            raise Exception(error)
        else:
            self.logger.info(f"Successfully connected to {meta}")
            self.logger.warning("Sanitizing the database")
            self.sanitize()
            self.logger.debug("Adding random authors")
            self.add_random_authors()
            self.logger.debug("Running sanity checks")
            self.sanity_checks()

    def sanity_checks(self):
        def to_list(dto_objects: list) -> list:
            return list(map(lambda object: object[0], dto_objects))

        tables = self.select(
            "SELECT tablename FROM pg_tables WHERE schemaname = 'public'"
        )
        self.logger.debug(f"Tables in the database: {to_list(tables)}")

        users: list = self.select(
            "SELECT rolname FROM pg_roles WHERE rolname NOT LIKE 'pg_%'"
        )
        self.logger.debug(f"Users in the database: {to_list(users)}")

    # Run a SQL query, returning all rows.
    def select(self, query: str) -> list[tuple]:
        cursor = self.db_connection.cursor()
        cursor.execute(query)
        self.db_connection.commit()
        return cursor.fetchall()

    # Run the startup migrations and delete all rows from all tables.
    def sanitize(self) -> None:
        cursor = self.db_connection.cursor()

        self.logger.debug("Running startup migrations")
        with open("migration.sql", "r") as txn:
            cursor.execute(txn.read())
        self.logger.info("Startup migrations finished")

        cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
        tables: list = [table[0] for table in cursor.fetchall()]
        for table in tables:
            cursor.execute(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;")

        self.db_connection.commit()

    # Append rows with random garbage to the `authors` table.
    def add_random_authors(self) -> None:
        cursor = self.db_connection.cursor()
        author_count: int = random.randint(5, 10)
        min: int = 5
        max: int = 15
        for _ in range(author_count):
            name: str = "".join(
                random.choice(string.ascii_letters)
                for _ in range(random.randint(min, max))
            )
            surname: str = "".join(
                random.choice(string.ascii_letters)
                for _ in range(random.randint(min, max))
            )
            middle_name: str = "".join(
                random.choice(string.ascii_letters)
                for _ in range(random.randint(min, max))
            )
            phone: str = "".join(random.choice(string.digits) for _ in range(11))
            query = "INSERT INTO authors (name, surname, middle_name, phone) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (name, surname, middle_name, phone))
        self.db_connection.commit()

    def upload_post(
        self, text: str, author_id: int, title: str = "New post", attachment_id=None
    ) -> None:
        cursor = self.db_connection.cursor()
        query = "INSERT INTO posts (text, title, author_id, attachment_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (text, title, author_id, attachment_id))
        self.db_connection.commit()
