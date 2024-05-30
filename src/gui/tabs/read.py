from logging import Logger

from PyQt6.QtCore import pyqtSignal

from database.connection import PgDatabase
from gui.main import (
    FONT,
    FONT_FAMILY,
    FONT_SIZE,
    SUBTEXT,
    SURFACE,
    trim_str,
    vertical_separator,
)
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class ReadTab(QWidget):
    logger: Logger
    connection: PgDatabase
    scroll_area: QScrollArea

    post_focused = pyqtSignal(int)
    post_unfocused = pyqtSignal()

    layout: QVBoxLayout
    scroll_area: QScrollArea

    POST_LIMIT: int = 100

    def __init__(self, connection: PgDatabase, logger: Logger) -> None:
        super().__init__()
        self.connection = connection
        self.logger = logger

        self.post_focused.connect(lambda post_id: self.focus_post(post_id))
        self.post_unfocused.connect(lambda: self.list_posts())

        self.scroll_area = QScrollArea()
        self.scroll_area.setFont(FONT)
        self.scroll_area.setWidgetResizable(True)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def list_posts(self) -> None:
        self.logger.info("Loading posts into the READ tab")

        post_list = QVBoxLayout()
        for post_id in range(1, self.POST_LIMIT + 1):
            post_list.addLayout(self.render_post(post_id))

        __widget = QWidget()
        __widget.setLayout(post_list)

        self.scroll_area.setWidget(__widget)
        self.layout.addWidget(self.scroll_area)

    def render_post(self, post_id: int) -> QVBoxLayout:
        container = QVBoxLayout()

        db = self.connection.db
        if db:
            cursor = db.cursor()
            cursor.execute(
                """
                   SELECT
                       p.id,
                       p.text,
                       p.title,
                       (a.surname || ' ' || a.name || ' ' || a.middle_name) as author_name,
                       p.created_at
                   FROM
                       posts p
                   LEFT JOIN
                       authors a ON p.author_id = a.id
                   WHERE
                       p.id = %s
                """,
                [post_id],
            )
            db.commit()
            row: tuple = cursor.fetchall()[0]

            # The post's title, author and timestamp.
            title = QLabel(f"<b>{trim_str(row[2], 80)}</b>")
            title.setFont(QFont(FONT_FAMILY, FONT_SIZE + 4))
            author_hint = QLabel("Автор:")
            author_hint.setFont(FONT)
            author_hint.setStyleSheet(f"color: {SURFACE}")
            author = QLabel(f"{row[3]}")
            author.setFont(FONT)
            timestamp_hint = QLabel("Дата публикации:")
            timestamp_hint.setFont(FONT)
            timestamp_hint.setStyleSheet(f"color: {SURFACE}")
            timestamp = QLabel(f"<b>{str(row[4]).split(' ')[0]}</b>")
            timestamp.setFont(FONT)
            metadata = QHBoxLayout()
            metadata.addWidget(title)
            metadata.addWidget(QLabel(""))  # Spacer.
            metadata.addWidget(author_hint)
            metadata.addWidget(author)
            metadata.addWidget(vertical_separator())
            metadata.addWidget(timestamp_hint)
            metadata.addWidget(timestamp)
            metadata.setStretch(1, 1)

            # A snippet of the post's text, as well as an `Read` button.
            text = QLineEdit()
            text.setFont(FONT)
            text.setReadOnly(True)
            text.setText(f"{row[1]}")
            text.setStyleSheet(f"color: {SUBTEXT}")
            read_button = QPushButton(" Читать... ")
            read_button.setFont(FONT)
            read_button.clicked.connect(lambda: self.post_focused.emit(int(row[0])))
            contents = QHBoxLayout()
            contents.addWidget(text)
            contents.addWidget(read_button)

            # Compose everything into a single layout.
            container.addLayout(metadata)
            container.addLayout(contents)
            container.addWidget(QLabel(""))  # A spacer.

        return container

    def focus_post(self, post_id: int) -> None:
        self.logger.info(f"Opening post #{post_id} for reading or editing")
        __widget = QWidget()

        db = self.connection.db
        if db:
            cursor = db.cursor()
            cursor.execute(
                """
                   SELECT
                       p.id,
                       p.text,
                       p.title
                   FROM
                       posts p
                   WHERE
                       p.id = %s
                """,
                [post_id],
            )
            db.commit()
            row: tuple = cursor.fetchall()[0]

            # Editing field.
            title_edit = QLineEdit()
            title_edit.setFont(QFont(FONT_FAMILY, FONT_SIZE + 2))
            title_edit.setText(row[2])
            text_edit = QTextEdit()
            text_edit.setFont(QFont(FONT_FAMILY, FONT_SIZE + 2))
            text_edit.setText(row[1])

            # A button for saving changes.
            update_button = QPushButton("Сохранить изменения")
            update_button.setFont(FONT)
            update_button.clicked.connect(
                lambda: self.update_post(
                    post_id=int(row[0]),
                    new_title=title_edit.text(),
                    new_text=text_edit.toPlainText(),
                )
            )

            # A button for going back to the post list.
            unfocus_button = QPushButton("Вернуться к списку публикаций")
            unfocus_button.setFont(FONT)
            unfocus_button.clicked.connect(lambda: self.post_unfocused.emit())

            # Compose everything.
            button_layout = QHBoxLayout()
            button_layout.addWidget(update_button)
            button_layout.addWidget(unfocus_button)
            layout = QVBoxLayout()
            layout.addWidget(title_edit)
            layout.addWidget(text_edit)
            layout.addLayout(button_layout)
            __widget.setLayout(layout)

        self.scroll_area.setWidget(__widget)

    def update_post(self, post_id: int, new_title: str, new_text: str) -> None:
        self.logger.info(f"Updating post #{post_id}")
        db = self.connection.db
        if db:
            cursor = db.cursor()
            cursor.execute(
                """
                    UPDATE post_updates
                    SET title = %s, text = %s
                    WHERE id = %s
                """,
                [new_title, new_text, post_id],
            )
            db.commit()
