import psycopg2 as postgresql


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

    def run_query(self, query: str) -> list[tuple]:
        cursor = self.db_connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()
