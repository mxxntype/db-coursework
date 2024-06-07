from logging import Logger
from database.connection import PgDatabase
from database.credentials import ADMIN, AUTHOR, READER, Credentials
from gui.main import ACCENT, FONT
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class ConnectionTab(QWidget):
    # Internals.
    credentials: Credentials = READER
    logger: Logger
    connection: PgDatabase = PgDatabase()

    # Signals.
    on_credential_change = pyqtSignal(Credentials)

    # GUI components.
    connection_status: QLabel
    connection_message: QTextEdit

    def __init__(self, logger: Logger) -> None:
        super().__init__()
        self.logger = logger

        # Respond to changes in the internal connection.
        self.connection.on_connect.connect(self.on_connect_ok)
        self.connection.on_disconnect.connect(self.on_connect_fail)

        # Respond to changes on the form.
        self.on_credential_change.connect(
            lambda new_credentials: self.update_credentials(new_credentials)
        )

        # Create forms for input.
        (user_layout, self.user_line_edit) = labeled_line_edit("Имя пользователя")
        (pass_layout, self.pass_line_edit) = labeled_line_edit("Пароль")
        (host_layout, self.host_line_edit) = labeled_line_edit("IP-адрес")
        (port_layout, self.port_line_edit) = labeled_line_edit("Порт")

        # Put the default READER credentials into the forms.
        self.user_line_edit.setText(self.credentials.user)
        self.pass_line_edit.setText(self.credentials.passwd)
        self.host_line_edit.setText(self.credentials.host)
        self.port_line_edit.setText(str(self.credentials.port))

        # Make sure any changes in the forms are reflected in the actual credentials.
        for le in (
            self.user_line_edit,
            self.pass_line_edit,
            self.host_line_edit,
            self.port_line_edit,
        ):
            le.textChanged.connect(
                lambda: self.on_credential_change.emit(self.form_credentials())
            )

        # Create a button for attempting an arbitrary connection.
        attempt_connection_button = QPushButton("Подключиться с указанными данными")
        attempt_connection_button.setFont(FONT)
        attempt_connection_button.clicked.connect(
            lambda: self.connect_as(self.form_credentials())
        )

        # Create shortcut buttons.
        shortcut_hint = QLabel("Или войдите как")
        shortcut_hint.setFont(FONT)
        shortcut_reader = QPushButton("Читатель")
        shortcut_reader.clicked.connect(lambda: self.connect_as(READER))
        shortcut_reader.setFont(FONT)
        shortcut_author = QPushButton("Редактор")
        shortcut_author.clicked.connect(lambda: self.connect_as(AUTHOR))
        shortcut_author.setFont(FONT)
        shortcut_admin = QPushButton("Администратор")
        shortcut_admin.clicked.connect(lambda: self.connect_as(ADMIN))
        shortcut_admin.setFont(FONT)
        shortcut_buttons = QHBoxLayout()
        shortcut_buttons.addWidget(shortcut_hint)
        shortcut_buttons.addWidget(shortcut_reader)
        shortcut_buttons.addWidget(shortcut_author)
        shortcut_buttons.addWidget(shortcut_admin)

        # Create a status label and a field for error messages.
        self.connection_status = QLabel("Статус: нет подключения")
        self.connection_status.setFont(FONT)
        self.connection_message = QTextEdit()
        self.connection_message.setFont(FONT)
        self.connection_message.setReadOnly(True)
        self.connection_message.setPlaceholderText(
            "В случае ошибки, она будет отображена здесь"
        )

        # Compose everything.
        tab_layout = QVBoxLayout()
        for layout in [user_layout, pass_layout]:
            tab_layout.addLayout(layout)
        tab_layout.addWidget(attempt_connection_button)
        tab_layout.addLayout(shortcut_buttons)
        tab_layout.addWidget(self.connection_status)
        tab_layout.addWidget(self.connection_message)
        bottom_layout = QHBoxLayout()
        bottom_layout.addLayout(host_layout)
        bottom_layout.addLayout(port_layout)
        tab_layout.addLayout(bottom_layout)

        self.setLayout(tab_layout)

    def on_connect_ok(self, meta: str) -> None:
        self.connection_status.setText(f"Статус: подключено ({meta})")
        self.connection_status.setStyleSheet(
            f"background-color: {ACCENT}; color: #000000"
        )
        self.connection_message.clear()

    def on_connect_fail(self, error: str) -> None:
        self.connection_status.setText("Статус: нет подключения")
        self.connection_status.setStyleSheet(
            "background-color: IndianRed; color: #000000"
        )
        self.connection_message.setText(error)

    def update_credentials(self, credentials: Credentials) -> None:
        # HACK: Each QLineEdit has its `textChanged` bound to updating
        # the internal credentials, so we do not have to touch those.
        self.user_line_edit.setText(credentials.user)
        self.pass_line_edit.setText(credentials.passwd)
        self.host_line_edit.setText(credentials.host)
        self.port_line_edit.setText(str(credentials.port))

    def connect_as(self, credentials: Credentials) -> None:
        self.update_credentials(credentials)
        self.connection.login(credentials)

    def form_credentials(self) -> Credentials:
        return Credentials(
            user=self.user_line_edit.text(),
            passwd=self.pass_line_edit.text(),
            host=self.host_line_edit.text(),
            port=int(self.port_line_edit.text()),
        )


def labeled_line_edit(label: str) -> tuple[QHBoxLayout, QLineEdit]:
    input_label = QLabel(f"{label}:")
    input_label.setFont(FONT)
    line_edit = QLineEdit()
    line_edit.setFont(FONT)
    line_edit.setPlaceholderText(label.lower())
    layout = QHBoxLayout()
    layout.addWidget(input_label)
    layout.addWidget(line_edit)
    return (layout, line_edit)
