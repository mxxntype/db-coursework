import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit
from PyQt6.QtCore import Qt
from database_connection import DatabaseConnection


class DatabaseGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.db_connection = DatabaseConnection(
            database="coursework",
            user="user",
            password="password",
            host="localhost",
            port=5432,
        )

        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        layout.addWidget(self.text_area)

        self.button = QPushButton("Execute Query")
        self.button.clicked.connect(self.execute_query)
        layout.addWidget(self.button)

        self.setLayout(layout)
        self.setWindowTitle("Database Query GUI")
        self.setGeometry(300, 300, 400, 300)
        self.show()

    def execute_query(self):
        query = "SELECT * FROM authors"
        rows = self.db_connection.run_query(query)
        for row in rows:
            self.text_area.append(str(row))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = DatabaseGUI()
    sys.exit(app.exec())
