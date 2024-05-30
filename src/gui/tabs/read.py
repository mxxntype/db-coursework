from logging import Logger

from database.connection import PgDatabase
from gui.main import FONT
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget


class ReadTab(QWidget):
    logger: Logger
    connection: PgDatabase

    table: QTableWidget

    def __init__(self, connection: PgDatabase, logger: Logger) -> None:
        super().__init__()
        self.connection = connection
        self.logger = logger

    def refresh(self) -> None:
        posts = self.connection.select("SELECT * FROM posts LIMIT 100") or []
        self.table = QTableWidget()
        self.table.setColumnCount(len(posts[0]))
        self.table.setRowCount(len(posts))
        self.table.setFont(FONT)

        for row, __row in enumerate(posts):
            for col, item in enumerate(__row):
                self.table.setItem(row, col, QTableWidgetItem(str(item)))

        tab_layout = QVBoxLayout()
        tab_layout.addWidget(self.table)
        self.setLayout(tab_layout)
