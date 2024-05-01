import psycopg2 as postgresql
import string
import random


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
               DELETE FROM authors WHERE true;
               DELETE FROM posts WHERE true;
               DELETE FROM attachments WHERE true;
               DELETE FROM ratings WHERE true;
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
            cursor.execute(
                f"INSERT INTO authors (name, surname, middle_name, phone) VALUES ('{name}', '{surname}', '{middle_name}', '+{phone}')"
            )
