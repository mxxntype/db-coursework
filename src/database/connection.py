import random
import string

import psycopg2 as postgresql
from database.log import log_function_call


class DatabaseConnection:
    def __init__(
        self,
        database: str = "coursework",
        user: str = "user",
        password: str = "password",
        host: str = "localhost",
        port: int = 5432,
    ) -> None:
        self.db_connection = postgresql.connect(
            database=database,
            user=user,
            password=password,
            host=host,
            port=port,
        )

        self.sanitize()
        self.add_random_authors()

    # Run a SQL query, returning all rows.
    @log_function_call
    def select(self, query: str) -> list[tuple]:
        cursor = self.db_connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    # Run the startup migrations and delete all rows from all tables.
    def sanitize(self) -> None:
        cursor = self.db_connection.cursor()
        with open("migrations/001.sql", "r") as txn:
            cursor.execute(txn.read())
        cursor.execute(
            """
               DELETE FROM ratings WHERE true;
               DELETE FROM posts WHERE true;
               DELETE FROM authors WHERE true;
               DELETE FROM attachments WHERE true;
           """
        )

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

    @log_function_call
    def upload_post(
        self, text: str, author_id: int, title: str = "New post", attachment_id=None
    ) -> None:
        cursor = self.db_connection.cursor()
        query = "INSERT INTO posts (text, title, author_id, attachment_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (text, title, author_id, attachment_id))
        self.db_connection.commit()
