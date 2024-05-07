from logging import Logger

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

# Font, shared between all other modules.
FONT_FAMILY: str = "IosevkaTerm NF"
FONT_SIZE: int = 24
FONT: QFont = QFont(FONT_FAMILY, FONT_SIZE)

from database.connection import DatabaseConnection  # noqa: E402
from gui.tabs.mod import Tabs  # noqa: E402
from log import create_named_logger  # noqa: E402


class DatabaseGUI(QMainWindow):
    # Internals.
    db: DatabaseConnection | None = None
    logger: Logger = create_named_logger("GUI")

    # GUI components.
    __font_family: str = "IosevkaTerm NF"
    __font_size: int = 24
    font: QFont = FONT

    tabs: Tabs

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("mxxntype's DB Coursework")
        self.setGeometry(600, 800, 800, 600)

        # Create the tabs.
        self.tabs = Tabs(self.logger)
        self.tab_widget = QTabWidget()
        self.tab_widget.setFont(self.font)
        self.tab_widget.addTab(self.tabs.connection, "DB Connection")

        self.setCentralWidget(self.tab_widget)

    # INFO: A form for authorization (selection of privileges).
    #
    # An ordinary `user` can only read posts and put down ratings; to write your own post,
    # you must log in as one of the authors. You can also view all the authors and their
    # average rating in the tab. The average rating is the arithmetic mean of the ratings
    # of all posts and attachments by this author.
    def create_login_tab(self) -> QWidget:
        self.author_list = QListWidget()
        self.author_list.setFont(self.font)

        if self.db is not None:
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
        self.post_list = QListWidget()
        self.post_list.setFont(self.font)

        if self.db is not None:
            posts: list[tuple] = self.db.select("SELECT * FROM posts")
            list(map(lambda post: self.post_list.addItem(str(post)), posts))

        layout = QVBoxLayout()
        layout.addWidget(self.post_list)
        tab = QWidget()
        tab.setLayout(layout)
        return tab

    # INFO: A form for writing your own post.
    #
    # Available only if the user is logged in as the author. Otherwise, it should be disabled,
    # and inform the user that the post cannot be published from a regular `user` account.
    def create_compose_tab(self) -> QWidget:
        title_font = QFont(self.__font_family, self.__font_size * 2)
        self.compose_title_label = QLabel("Title:")
        self.compose_title_label.setFont(title_font)

        self.compose_title_line = QLineEdit()
        self.compose_title_line.setFont(title_font)
        self.compose_title_line.setPlaceholderText("The title of your post")
        self.compose_title_line.setMaxLength(128)
        self.compose_title_line.textChanged.connect(
            lambda: self.compose_title_chars.setText(
                f"{len(self.compose_title_line.text())}/{self.compose_title_line.maxLength()}"
            )
        )

        self.compose_title_chars = QLabel(f"0/{self.compose_title_line.maxLength()}")
        self.compose_title_chars.setFont(title_font)

        title_layout = QHBoxLayout()
        title_layout.addWidget(self.compose_title_label)
        title_layout.addWidget(self.compose_title_line)
        title_layout.addWidget(self.compose_title_chars)

        self.compose_text_area = QTextEdit()
        self.compose_text_area.setFont(self.font)
        self.compose_text_area.setPlaceholderText(
            "The text of your post. Let your soul out..."
        )

        # if self.db is not None:
        #     authors = self.db.select("SELECT * FROM authors")
        #     authors = list(map(lambda author: str(author), authors))

        #     author_choice = QComboBox()
        #     author_choice.addItems(authors)
        #     author_choice.setFont(self.font)

        #     submit_button = QPushButton("Submit post")
        #     submit_button.setFont(self.font)
        #     submit_button.clicked.connect(
        #         lambda: self.db.upload_post(
        #             text=self.compose_text_area.toPlainText(),
        #             author_id=eval(author_choice.currentText())[0],
        #             title=self.compose_title_line.text(),
        #         )
        #     )

        # tab_layout = QVBoxLayout()
        # tab_layout.addLayout(title_layout)
        # tab_layout.addWidget(self.compose_text_area)
        # tab_layout.addWidget(author_choice)
        # tab_layout.addWidget(submit_button)
        tab = QWidget()
        # tab.setLayout(tab_layout)
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
