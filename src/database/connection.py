from logging import Logger

import psycopg2 as postgresql
from PyQt6.QtCore import QObject, pyqtSignal
from psycopg2.sql import Composable

from database.credentials import Credentials
from log.main import create_named_logger


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
            cursor = self.db.cursor()
            cursor.execute(query, vars)
            self.db.commit()
            return cursor.fetchall()

    def task_transaction(self) -> None:
        if self.db:
            cursor = self.db.cursor()
            cursor.execute("CALL sanitize_posts_and_authors(2.0, 4.5)")
            self.db.commit()
