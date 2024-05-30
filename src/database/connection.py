from logging import Logger

import psycopg2 as postgresql
from PyQt6.QtCore import QObject, pyqtSignal

from database.credentials import Credentials
from log.main import create_named_logger


class PgDatabase(QObject):
    # Internals.
    logger: Logger = create_named_logger("DATABASE")
    db: postgresql.extensions.connection | None = None

    # Signals and state.
    on_connect = pyqtSignal(str)
    on_disconnect = pyqtSignal(str)
    connected: bool = False

    def __init__(self) -> None:
        super().__init__()
        self.on_connect.connect(self.on_connect_handler)
        self.on_disconnect.connect(self.on_disconnect_handler)

    def login(self, credentials: Credentials) -> None:
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
        self.logger.debug("Running sanity checks")
        self.sanity_checks()

    def on_disconnect_handler(self, error: str) -> None:
        self.db = None
        self.connected = True
        self.logger.error(error)

    def sanity_checks(self):
        def to_list(dto_objects: list) -> list:
            return list(map(lambda object: object[0], dto_objects))

        tables = self.select(
            "SELECT tablename FROM pg_tables WHERE schemaname = 'public'"
        )
        self.logger.debug(f"Tables in the database: {to_list(tables or [])}")

        users = self.select(
            "SELECT rolname FROM pg_roles WHERE rolname NOT LIKE 'pg_%'"
        )
        self.logger.debug(f"Users in the database: {to_list(users or [])}")

    # Run a SQL query, returning all rows.
    def select(self, query: str) -> list[tuple] | None:
        if self.db:
            cursor = self.db.cursor()
            cursor.execute(query)
            self.db.commit()
            return cursor.fetchall()
