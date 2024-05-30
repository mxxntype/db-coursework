from logging import Logger

from database.connection import PgDatabase
from gui.main import FONT, SUBTEXT, vertical_separator
from gui.status import StatusBar
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


class AuthorTab(QWidget):
    logger: Logger
    connection: PgDatabase
    layout: QVBoxLayout
    scroll_area: QScrollArea
    status_bar: StatusBar

    AUTHOR_LIMIT: int = 50

    def __init__(self, connection: PgDatabase, logger: Logger) -> None:
        super().__init__()
        self.connection = connection
        self.logger = logger
        self.scroll_area = QScrollArea()
        self.scroll_area.setFont(FONT)
        self.scroll_area.setWidgetResizable(True)
        self.layout = QVBoxLayout()
        self.status_bar = StatusBar()
        self.setLayout(self.layout)

    def refresh(self) -> None:
        self.logger.info("Loading authors into the AUTHORS tab")
        authors: list[tuple] = self.connection.select(
            """
                SELECT
                    a.id,
                    a.name,
                    a.surname,
                    a.middle_name,
                    a.phone,
                    act.total_posts,
                    act.total_attachments,
                    act.activity_level
                FROM authors a
                LEFT JOIN get_author_activity() act ON id = act.author_id
                ORDER BY id DESC
                LIMIT %s
            """,
            [self.AUTHOR_LIMIT],
        )

        author_list = QVBoxLayout()
        for row in authors:
            author_list.addLayout(
                self.render_author(
                    id=row[0],
                    name=row[1],
                    surname=row[2],
                    middle_name=row[3],
                    phone=row[4],
                    post_count=row[5],
                    attachment_count=row[6],
                    activity_level=row[7],
                )
            )

        __widget = QWidget()
        __widget.setLayout(author_list)

        self.scroll_area.setWidget(__widget)
        self.layout.addWidget(self.scroll_area)
        self.layout.addWidget(self.status_bar)

    # Create a layout with all the widgets needed to display (and edit) information about an author.
    def render_author(
        self,
        id: int,
        name: str,
        surname: str,
        middle_name: str,
        phone: str,
        post_count: int | None = None,
        attachment_count: int | None = None,
        activity_level: str | None = None,
    ) -> QVBoxLayout:
        container = QVBoxLayout()
        has_update_permissions: bool = self.connection.credentials.user == "admin"

        # A shorthand for creating ready-to-go QLineEdits with labels.
        def mkLineEdit(
            initial_text: str, read_only: bool, label: str
        ) -> tuple[QLineEdit, QLabel]:
            line_edit = QLineEdit()
            line_edit.setFont(FONT)
            line_edit.setReadOnly(read_only)
            line_edit.setText(initial_text)
            _label = QLabel(label)
            _label.setFont(FONT)
            _label.setStyleSheet(f"color: {SUBTEXT}")
            return (line_edit, _label)

        # Create the needed editing fields with their labels.
        (name_le, name_label) = mkLineEdit(name, not has_update_permissions, "Имя:")
        (surname_le, surname_label) = mkLineEdit(
            surname, not has_update_permissions, "Фамилия:"
        )
        (middle_name_le, middle_name_label) = mkLineEdit(
            middle_name, not has_update_permissions, "Отчество:"
        )
        (phone_le, phone_label) = mkLineEdit(
            phone, not has_update_permissions, "Телефон:"
        )

        # Compose them into a horizontal layout.
        identity_layour = QHBoxLayout()
        for w in (
            surname_label,
            surname_le,
            name_label,
            name_le,
            middle_name_label,
            middle_name_le,
            phone_label,
            phone_le,
        ):
            identity_layour.addWidget(w)
        container.addLayout(identity_layour)

        # A shorthand for creating a statistics measure.
        def mkStat(layout: QHBoxLayout, value: str, hint: str) -> None:
            value_label = QLabel(value)
            value_label.setFont(FONT)
            hint_label = QLabel(f"{hint}:")
            hint_label.setFont(FONT)
            hint_label.setStyleSheet(f"color: {SUBTEXT}")
            layout.addWidget(hint_label)
            layout.addWidget(value_label)

        activity_layout = QHBoxLayout()
        container.addLayout(activity_layout)

        if activity_level:
            mkStat(activity_layout, activity_level, "Уровень активности")
            activity_layout.addWidget(vertical_separator())
        if post_count is not None:
            mkStat(activity_layout, str(post_count), "Количество публикаций")
            activity_layout.addWidget(vertical_separator())
        if attachment_count is not None:
            mkStat(activity_layout, str(attachment_count), "Количество вложений")
            activity_layout.setStretch(7, 1)

        # Add a `save` button if we can actually update anything.
        if has_update_permissions:
            save_button = QPushButton("Сохранить данные автора")
            save_button.setFont(FONT)
            save_button.clicked.connect(
                lambda: self.update_author(
                    id=id,
                    new_name=name_le.text(),
                    new_surname=surname_le.text(),
                    new_middle_name=middle_name_le.text(),
                    new_phone=phone_le.text(),
                )
            )
            container.addWidget(save_button)
        container.addWidget(QLabel(""))  # Spacer.
        container.addWidget(QLabel(""))  # Spacer.

        return container

    # Update an author's data in the database.
    def update_author(
        self,
        id: int,
        new_name: str,
        new_surname: str,
        new_middle_name: str,
        new_phone: str,
    ) -> None:
        db = self.connection.db
        if db:
            try:
                cursor = db.cursor()
                cursor.execute(
                    """
                       UPDATE authors
                       SET name = %s, surname = %s, middle_name = %s, phone = %s
                       WHERE id = %s
                   """,
                    [new_name, new_surname, new_middle_name, new_phone, id],
                )
                db.commit()
                self.status_bar.set_ok("Данные автора обновлены.")
            except Exception as error:
                self.logger.error(error)
                self.status_bar.set_error(
                    f"Не удалось обновить данные автора! [{error}]"
                )
