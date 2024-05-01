from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QTextEdit,
)
from database.connection import DatabaseConnection
import qdarkstyle
import sys


class DatabaseGUI(QWidget):
    font_family: str = "IosevkaTerm NF"
    font_size: int = 24

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.db_connection = DatabaseConnection()
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setFont(QFont(self.font_family, self.font_size))
        layout.addWidget(self.text_area)

        self.button = QPushButton("Execute Query")
        self.button.clicked.connect(self.run_sql_query)
        self.button.setFont(QFont(self.font_family, self.font_size))
        layout.addWidget(self.button)

        self.setLayout(layout)
        self.setGeometry(600, 800, 800, 600)
        self.setWindowTitle("mxxntype's DB Coursework")
        self.show()

    def run_sql_query(self):
        rows = self.db_connection.select("SELECT * FROM authors")
        for row in rows:
            self.text_area.append(str(row))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api="pyqt6"))
    gui = DatabaseGUI()
    sys.exit(app.exec())
