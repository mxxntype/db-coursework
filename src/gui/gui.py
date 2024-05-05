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
        self.tab_widget.addTab(self.create_login_tab(), " Login as author ")
        self.tab_widget.addTab(self.create_read_tab(), " Read posts ")
        self.tab_widget.addTab(self.create_compose_tab(), " Compose a post ")
        self.tab_widget.addTab(self.create_media_tab(), " Browse media ")
        self.tab_widget.setFont(self.font)
        layout.addWidget(self.tab_widget)

        self.setLayout(layout)
        self.show()

    # INFO: A form for authorization (selection of privileges).
    #
    # An ordinary `user` can only read posts and put down ratings; to write your own post,
    # you must log in as one of the authors. You can also view all the authors and their
    # average rating in the tab. The average rating is the arithmetic mean of the ratings
    # of all posts and attachments by this author.
    def create_login_tab(self) -> QWidget:
        self.author_list = QListWidget()
        self.author_list.setFont(self.font)

        authors: list[tuple] = self.db.select("SELECT * FROM authors")
        list(map(lambda author: self.author_list.addItem(str(author)), authors))

        layout = QVBoxLayout()
        layout.addWidget(self.author_list)
        tab = QWidget()
        tab.setLayout(layout)
        return tab

    # INFO: This tab offers the ability to read all the posts stored in the `posts` table.
    #
    # Initially, a list of all posts is displayed, with the author and rating next to each one.
    # When you click on any of the posts, it should open to the entire tab, showing a possible
    # attachment and text.
    #
    # It is possible to go to all the author's posts and put a rating for the post.
    def create_read_tab(self) -> QWidget:
        layout = QVBoxLayout()
        tab = QWidget()
        tab.setLayout(layout)
        return tab

    # INFO: A form for writing your own post.
    #
    # Available only if the user is logged in as the author. Otherwise, it should be disabled,
    # and inform the user that the post cannot be published from a regular `user` account.
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

    # INFO: A tab for viewing all the media available in the `attachments` table.
    #
    # Provides the ability to go to the post containing the selected
    # attachment and a way to view all media belonging to any of the authors.
    def create_media_tab(self) -> QWidget:
        layout = QVBoxLayout()
        tab = QWidget()
        tab.setLayout(layout)
        return tab
