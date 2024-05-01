import psycopg2 as postgresql


class DatabaseConnection:
    def __init__(self, database: str, user: str, password: str, host: str, port: int):
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
        rows = cursor.fetchall()
        return rows


def main() -> None:
    db_connection = DatabaseConnection(
        database="coursework",
        user="user",
        password="password",
        host="localhost",
        port=5432,
    )
    db_connection.run_query("SELECT * FROM authors")


if __name__ == "__main__":
    main()
