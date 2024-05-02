from database.connection import DatabaseConnection
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class DatabaseGUI(QWidget):
    font_family: str = "IosevkaTerm NF"
    font_size: int = 24

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("mxxntype's DB Coursework")
        self.setGeometry(600, 800, 800, 600)

        layout = QVBoxLayout()

        # Create the text area.
        self.db_connection = DatabaseConnection()
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setFont(QFont(self.font_family, self.font_size))
        layout.addWidget(self.text_area)

        # Create the button.
        self.button = QPushButton("Execute Query")
        self.button.clicked.connect(self.run_sql_query)
        self.button.setFont(QFont(self.font_family, self.font_size))
        layout.addWidget(self.button)

        self.setLayout(layout)
        self.show()

    def run_sql_query(self):
        rows = self.db_connection.select("SELECT * FROM authors")
        for row in rows:
            self.text_area.append(str(row))


# class GUI(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Tab Example")
#         self.resize(300, 200)

#         layout = QVBoxLayout()
#         self.tab_widget = QTabWidget()
#         self.tab_widget.addTab(self.create_tab("Tab 1"), "Tab 1")
#         self.tab_widget.addTab(self.create_tab("Tab 2"), "Tab 2")
#         self.tab_widget.addTab(self.create_tab("Tab 3"), "Tab 3")
#         layout.addWidget(self.tab_widget)

#         self.setLayout(layout)

#     def create_tab(self, title):
#         tab = QWidget()
#         layout = QVBoxLayout()
#         layout.addWidget(QPushButton(title))
#         tab.setLayout(layout)
#         return tab
