from logging import Logger

import psycopg2 as postgresql
from database.credentials import Credentials
from log.main import create_named_logger
from psycopg2.sql import Composable
from PyQt6.QtCore import QObject, pyqtSignal


class PgDatabase(QObject):
    # Internals.
    logger: Logger = create_named_logger("DATABASE")
    db: postgresql.extensions.connection | None = None
    credentials: Credentials

    # Signals and state.
    on_connect = pyqtSignal(str)
    on_disconnect = pyqtSignal(str)
    connected: bool = False

    def __init__(self) -> None:
        super().__init__()
        self.on_connect.connect(self.on_connect_handler)
        self.on_disconnect.connect(self.on_disconnect_handler)

    def login(self, credentials: Credentials) -> None:
        self.credentials = credentials
        try:
            self.logger.info("Attempting to connect to PostgreSQL")
            self.db = postgresql.connect(
                database=credentials.dbname,
                user=credentials.user,
                password=credentials.passwd,
                host=credentials.host,
                port=credentials.port,
            )
            self.db.set_session(autocommit=True)
            self.on_connect.emit(
                f"{credentials.user}@{credentials.host}:{credentials.port}"
            )
        except Exception as error:
            error = str(error).strip()
            self.on_disconnect.emit(error)

    def on_connect_handler(self, meta: str) -> None:
        self.connected = True
        self.logger.info(f"Successfully connected to {meta}")

    def on_disconnect_handler(self, error: str) -> None:
        self.db = None
        self.connected = True
        self.logger.error(error)

    def select(self, query: str | bytes | Composable, vars) -> list[tuple]:
        if not self.db:
            return []
        else:
            with self.db.cursor() as cursor:
                cursor.execute(query, vars)
                return cursor.fetchall()

    # Составной многотабличный запрос с CASE-выражением.
    def task_case(self) -> None:
        if self.db:
            with self.db.cursor() as cursor:
                cursor.execute("SELECT * FROM get_author_activity()")
        else:
            self.logger.warn("Not connected to DB, skipping request")

    # Многотабличный VIEW, с возможностью его обновления (использовать триггеры или правила).
    def task_view(self) -> None:
        if self.db:
            with self.db.cursor() as cursor:
                cursor.execute("SELECT * FROM post_details")
        else:
            self.logger.warn("Not connected to DB, skipping request")

    # Материализованное представление.
    def task_materialized_view(self) -> None:
        if self.db:
            with self.db.cursor() as cursor:
                cursor.execute(
                    """
                       REFRESH MATERIALIZED VIEW author_activity_score;
                       SELECT * FROM author_activity_score;
                    """
                )
        else:
            self.logger.warn("Not connected to DB, skipping request")

    # Запросы, содержащие подзапрос в разделах SELECT, FROM и WHERE (в каждом хотя бы по одному).
    def task_subquery_select(self) -> None:
        if self.db:
            with self.db.cursor() as cursor:
                cursor.execute("SELECT * FROM get_posts_with_author_count()")
        else:
            self.logger.warn("Not connected to DB, skipping request")

    # Запросы, содержащие подзапрос в разделах SELECT, FROM и WHERE (в каждом хотя бы по одному).
    def task_subquery_where(self) -> None:
        if self.db:
            with self.db.cursor() as cursor:
                cursor.execute("SELECT * FROM get_posts_by_prolific_authors(13)")
        else:
            self.logger.warn("Not connected to DB, skipping request")

    # Запросы, содержащие подзапрос в разделах SELECT, FROM и WHERE (в каждом хотя бы по одному).
    def task_subquery_from(self) -> None:
        if self.db:
            with self.db.cursor() as cursor:
                cursor.execute("SELECT * FROM get_posts_with_average_ratings()")
        else:
            self.logger.warn("Not connected to DB, skipping request")

    def task_correlated_1(self) -> None:
        if self.db:
            with self.db.cursor() as cursor:
                cursor.execute("SELECT * FROM get_latest_rating_for_each_post()")
        else:
            self.logger.warn("Not connected to DB, skipping request")

    def task_correlated_2(self) -> None:
        if self.db:
            with self.db.cursor() as cursor:
                cursor.execute("SELECT * FROM get_highest_rated_post_per_author()")
        else:
            self.logger.warn("Not connected to DB, skipping request")

    def task_correlated_3(self) -> None:
        if self.db:
            with self.db.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM get_authors_with_high_rated_posts(4::smallint)"
                )
        else:
            self.logger.warn("Not connected to DB, skipping request")

    # Реализовать отдельную хранимую процедуру, состоящую из нескольких отдельных операций в виде
    # единой транзакции, которая при определенных условиях может быть зафиксирована или откатана.
    def task_transaction(self) -> None:
        if self.db:
            with self.db.cursor() as cursor:
                cursor.execute("CALL sanitize_posts_and_authors(2.0, 4.5)")
        else:
            self.logger.warn("Not connected to DB, skipping request")
