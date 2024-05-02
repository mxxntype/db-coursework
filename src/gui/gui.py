from database.connection import DatabaseConnection
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QComboBox,
    QListWidget,
    QPushButton,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class DatabaseGUI(QWidget):
    __font_family: str = "IosevkaTerm NF"
    __font_size: int = 24
    font: QFont = QFont(__font_family, __font_size)
    db: DatabaseConnection = DatabaseConnection()

    def __init__(self) -> None:
        super().__init__()
        self.init_ui()

    def init_ui(self) -> None:
        self.setWindowTitle("mxxntype's DB Coursework")
        self.setGeometry(600, 800, 800, 600)

        layout = QVBoxLayout()
        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.create_authors_tab(), "Authors")
        self.tab_widget.addTab(self.create_compose_tab(), "Compose a post")
        self.tab_widget.setFont(self.font)
        layout.addWidget(self.tab_widget)

        self.setLayout(layout)
        self.show()

    def create_authors_tab(self) -> QWidget:
        self.author_list = QListWidget()
        self.author_list.setFont(self.font)

        authors: list[tuple] = self.db.select("SELECT * FROM authors")
        list(map(lambda author: self.author_list.addItem(str(author)), authors))

        layout = QVBoxLayout()
        layout.addWidget(self.author_list)
        tab = QWidget()
        tab.setLayout(layout)
        return tab

    def create_compose_tab(self) -> QWidget:
        self.compose_text_area = QTextEdit()
        self.compose_text_area.setFont(self.font)
        self.compose_text_area.setPlaceholderText("Let your soul out...")

        authors = self.db.select("SELECT * FROM authors")
        authors = list(map(lambda author: str(author), authors))

        author_choice = QComboBox()
        author_choice.addItems(authors)
        author_choice.setFont(self.font)

        submit_button = QPushButton("Submit post")
        submit_button.setFont(self.font)
        submit_button.clicked.connect(
            lambda: self.db.upload_post(
                text=self.compose_text_area.toPlainText(),
                author_id=eval(author_choice.currentText())[0],
                title="Sample post",
            )
        )

        layout = QVBoxLayout()
        layout.addWidget(self.compose_text_area)
        layout.addWidget(author_choice)
        layout.addWidget(submit_button)
        tab = QWidget()
        tab.setLayout(layout)
        return tab
