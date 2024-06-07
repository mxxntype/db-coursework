from collections.abc import Iterable
from logging import Logger

from database.connection import PgDatabase
from gui.main import (
    ACCENT,
    FONT,
    FONT_FAMILY,
    FONT_SIZE,
    SUBTEXT,
    SURFACE,
    trim_str,
    vertical_separator,
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSpinBox,
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
    status_message: QLabel

    title_filter: QLineEdit
    text_filter: QLineEdit
    author_filter: QLineEdit

    POST_LIMIT: int = 30

    def __init__(self, connection: PgDatabase, logger: Logger) -> None:
        super().__init__()
        self.connection = connection
        self.logger = logger

        self.post_focused.connect(lambda post_id: self.focus_post(post_id))
        self.post_unfocused.connect(lambda: self.list_posts())

        self.filter_hint = QLabel(" Фильтры ")
        self.filter_hint.setFont(FONT)
        self.filter_hint.setStyleSheet(f"background-color: {ACCENT}; color: black")
        self.title_hint = QLabel("Название:")
        self.title_hint.setFont(FONT)
        self.title_hint.setStyleSheet(f"color: {SUBTEXT}")
        self.title_filter = QLineEdit()
        self.title_filter.setFont(FONT)
        self.title_filter.textChanged.connect(self.list_posts)
        self.text_hint = QLabel("Содержание:")
        self.text_hint.setFont(FONT)
        self.text_hint.setStyleSheet(f"color: {SUBTEXT}")
        self.text_filter = QLineEdit()
        self.text_filter.setFont(FONT)
        self.text_filter.textChanged.connect(self.list_posts)
        self.author_hint = QLabel("Автор:")
        self.author_hint.setFont(FONT)
        self.author_hint.setStyleSheet(f"color: {SUBTEXT}")
        self.author_filter = QLineEdit()
        self.author_filter.setFont(FONT)
        self.author_filter.textChanged.connect(self.list_posts)
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(self.filter_hint)
        filter_layout.addWidget(self.title_hint)
        filter_layout.addWidget(self.title_filter)
        filter_layout.addWidget(self.text_hint)
        filter_layout.addWidget(self.text_filter)
        filter_layout.addWidget(self.author_hint)
        filter_layout.addWidget(self.author_filter)

        self.status_message = QLabel("")
        self.status_message.setFont(FONT)

        self.scroll_area = QScrollArea()
        self.scroll_area.setFont(FONT)
        self.scroll_area.setWidgetResizable(True)

        self.layout = QVBoxLayout()
        self.layout.addLayout(filter_layout)
        self.setLayout(self.layout)

    def list_posts(self) -> None:
        self.logger.info("Loading posts into the READ tab")
        # HACK: Fix segfault after swiching users.
        self.status_message = QLabel("")
        self.status_message.setFont(FONT)
        self.filter_hint.setHidden(False)
        self.title_filter.setHidden(False)
        self.title_hint.setHidden(False)
        self.text_filter.setHidden(False)
        self.text_hint.setHidden(False)
        self.author_filter.setHidden(False)
        self.author_hint.setHidden(False)

        posts: list[tuple] = self.connection.select(
            """
                SELECT
                    p.id,
                    p.title,
                    p.text,
                    (a.surname || ' ' || a.name || ' ' || a.middle_name) as author_name,
                    created_at
                FROM posts p
                LEFT JOIN authors a ON p.author_id = a.id
                WHERE
                    LOWER(p.title) LIKE '%%' || %s || '%%' AND
                    LOWER(p.text) LIKE '%%' || %s || '%%' AND
                    LOWER(a.surname || ' ' || a.name || ' ' || a.middle_name) LIKE '%%' || %s || '%%'
                ORDER BY id ASC
                LIMIT %s
            """,
            [
                self.title_filter.text().lower(),
                self.text_filter.text().lower(),
                self.author_filter.text().lower(),
                self.POST_LIMIT,
            ],
        )

        post_list = QVBoxLayout()
        for post in posts:
            post_list.addLayout(
                self.render_post(
                    post_id=post[0],
                    title_str=post[1],
                    text_str=post[2],
                    author_str=post[3],
                    timestamp_str=post[4],
                )
            )

        note = QLabel("Измените критерии поиска для просмотра других публикаций.")
        note.setFont(FONT)
        note.setStyleSheet(f"color: {ACCENT}")
        post_list.addWidget(note)
        post_list.addWidget(QLabel())
        post_list.setStretch(len(posts) + 1, 1)

        __widget = QWidget()
        __widget.setLayout(post_list)

        self.scroll_area.setWidget(__widget)
        self.layout.addWidget(self.scroll_area)

    def render_post(
        self,
        post_id: int,
        title_str: str,
        text_str: str,
        author_str: str,
        timestamp_str: str,
    ) -> QVBoxLayout:
        # The post's title, author and timestamp.
        title = QLabel(f"<b>{trim_str(title_str, 60)}</b>")
        title.setFont(QFont(FONT_FAMILY, FONT_SIZE + 4))
        author_hint = QLabel("Автор:")
        author_hint.setFont(FONT)
        author_hint.setStyleSheet(f"color: {SURFACE}")
        author = QLabel(author_str)
        author.setFont(FONT)
        timestamp_hint = QLabel("Дата публикации:")
        timestamp_hint.setFont(FONT)
        timestamp_hint.setStyleSheet(f"color: {SURFACE}")
        timestamp = QLabel(f"<b>{str(timestamp_str).split(' ')[0]}</b>")
        timestamp.setFont(FONT)

        # A snippet of the post's text, as well as an `Read` button.
        text = QTextEdit()
        text.setFont(FONT)
        text.setFixedHeight(FONT_SIZE * 4)
        text.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        text.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        text.setReadOnly(True)
        text.setText(text_str)
        text.setStyleSheet(f"color: {SUBTEXT}")
        focus_button = QPushButton(" Читать... ")
        focus_button.setFont(FONT)
        focus_button.setFixedHeight(FONT_SIZE * 4)
        focus_button.clicked.connect(lambda: self.post_focused.emit(post_id))
        focus_button.setStyleSheet(
            """
                QPushButton {
                    background-color: SlateBlue;
                    color: black;
                }
                QPushButton:hover {
                    background-color: #8d81d9;
                }
            """
        )

        # Compose everything into a single layout.
        metadata = QHBoxLayout()
        metadata.addWidget(title)
        metadata.addWidget(QLabel(""))  # Spacer.
        metadata.addWidget(author_hint)
        metadata.addWidget(author)
        metadata.addWidget(vertical_separator())
        metadata.addWidget(timestamp_hint)
        metadata.addWidget(timestamp)
        metadata.setStretch(1, 1)
        contents = QHBoxLayout()
        contents.addWidget(text)
        contents.addWidget(focus_button)
        container = QVBoxLayout()
        container.addLayout(metadata)
        container.addLayout(contents)
        container.addWidget(QLabel(""))  # A spacer.
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
            row: tuple = cursor.fetchall()[0]

            # Editing field.
            title_edit = QLineEdit()
            title_edit.setFont(QFont(FONT_FAMILY, FONT_SIZE + 2))
            title_edit.setStyleSheet("font-weight: bold")
            title_edit.setText(row[2])
            text_edit = QTextEdit()
            text_edit.setFont(FONT)
            text_edit.setText(row[1])
            title_edit.setReadOnly(True)
            text_edit.setReadOnly(True)

            # Buttons for saving changes (if allowed) and going back.
            button_layout = QHBoxLayout()
            if self.connection.credentials.user in ["editor", "admin"]:
                title_edit.setReadOnly(False)
                text_edit.setReadOnly(False)
                author_combobox = QComboBox()
                author_combobox.setFont(FONT)
                author_filter = QLineEdit()
                author_filter.setFont(FONT)
                author_filter.setPlaceholderText("Фильтр")
                author_filter.textChanged.connect(lambda: author_combobox.clear())
                author_filter.textChanged.connect(
                    lambda: author_combobox.addItems(
                        self.load_authors(author_filter.text()) or []
                    )
                )
                author_filter.textChanged.emit("")
                update_button = QPushButton(" Сохранить изменения ")
                update_button.setFont(FONT)
                update_button.clicked.connect(
                    lambda: self.update_post(
                        post_id=int(row[0]),
                        new_title=title_edit.text(),
                        new_text=text_edit.toPlainText(),
                        new_author=author_combobox.currentText(),
                    )
                )
                button_layout.addWidget(author_filter)
                button_layout.addWidget(author_combobox)
                button_layout.addWidget(update_button)
            else:
                self.set_warn(
                    "Для того, чтобы редактировать публикации, авторизуйтесь как автор или администратор."
                )

            # A button for going back to the post list.
            unfocus_button = QPushButton(" Вернуться к списку публикаций ")
            unfocus_button.setFont(FONT)
            unfocus_button.clicked.connect(lambda: self.post_unfocused.emit())
            button_layout.addWidget(unfocus_button)

            rate_label = QLabel("Оцените публикацию:")
            rate_label.setFont(FONT)
            rate_edit = QSpinBox()
            rate_edit.setFont(FONT)
            rate_edit.setRange(1, 5)
            rate_label.setStyleSheet(f"color: {SUBTEXT}")
            rate_button = QPushButton(" Оценить публикацию ")
            rate_button.setFont(FONT)
            if self.connection.db:
                with self.connection.db.cursor() as cursor:
                    rate_button.clicked.connect(
                        lambda: cursor.execute(
                            "SELECT rate_post(%s, %s::smallint)",
                            [post_id, rate_edit.text()],
                        )
                    )
            rate_layout = QHBoxLayout()
            rate_layout.addWidget(rate_label)
            rate_layout.addWidget(rate_edit)
            rate_layout.addWidget(rate_button)

            # Compose everything.
            layout = QVBoxLayout()
            layout.addWidget(title_edit)
            layout.addWidget(text_edit)
            layout.addLayout(rate_layout)
            layout.addLayout(button_layout)
            layout.addWidget(self.status_message)
            __widget.setLayout(layout)

        self.filter_hint.setHidden(True)
        self.title_filter.setHidden(True)
        self.title_hint.setHidden(True)
        self.text_filter.setHidden(True)
        self.text_hint.setHidden(True)
        self.author_filter.setHidden(True)
        self.author_hint.setHidden(True)
        self.scroll_area.setWidget(__widget)

    def update_post(
        self,
        post_id: int,
        new_title: str,
        new_text: str,
        new_author: str,
    ) -> None:
        self.logger.info(f"Updating post #{post_id}")
        db = self.connection.db
        if db:
            try:
                cursor = db.cursor()
                cursor.execute(
                    """
                        UPDATE posts
                        SET
                            title = %s,
                            text = %s,
                            author_id = (
                                SELECT MIN(id) FROM authors
                                WHERE
                                    (surname || ' ' || name || ' ' || middle_name || ', ' || phone) LIKE '%%' || %s || '%%'
                                GROUP BY id
                            )
                        WHERE id = %s
                    """,
                    [new_title, new_text, new_author, post_id],
                )
                db.commit()
                self.set_info("Изменения сохранены.")
            except Exception as error:
                self.logger.error(f"Can't edit a post as the current user: {error}")
                self.set_error(
                    "Недостаточно разрешений для редактирования публикации! Войдите как автор или администратор."
                )

    def load_authors(self, filter: str) -> Iterable[str] | None:
        rows: list[tuple] = self.connection.select(
            """
                SELECT * FROM authors
                WHERE
                    (surname || ' ' || name || ' ' || middle_name || ', ' || phone) LIKE '%%' || %s || '%%'
            """,
            [filter],
        )
        return list(map(lambda row: f"{row[2]} {row[1]} {row[3]}, {row[4]}", rows))

    def set_info(self, info: str):
        self.status_message.setText(info)
        self.status_message.setStyleSheet("color: LightGreen")
        QTimer.singleShot(3000, self.clear_error)

    def set_warn(self, warn: str):
        self.status_message.setText(warn)
        self.status_message.setStyleSheet(f"color: {ACCENT}")

    def set_error(self, error: str):
        self.status_message.setText(error)
        self.status_message.setStyleSheet("background-color: IndianRed; color: black")
        QTimer.singleShot(3000, self.clear_error)

    def clear_error(self):
        self.status_message.clear()
        self.status_message.setStyleSheet("")
