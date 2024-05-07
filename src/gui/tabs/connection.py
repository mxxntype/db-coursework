import os
from logging import Logger

from database.connection import DatabaseConnection
from gui.main import FONT
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
    # Connection credentials.
    db_name: str = os.environ.get("DB_NAME") or "coursework"
    db_user: str = os.environ.get("DB_USER") or "admin"
    db_pass: str = os.environ.get("DB_PASSWORD") or "admin"
    db_host: str = "localhost"
    db_port: int = 5432

    # Internals.
    logger: Logger
    connection = DatabaseConnection | None
    status: str = "Not connected"

    # GUI components.
    connection_status: QLabel
    connection_message: QTextEdit

    def __init__(self, logger: Logger) -> None:
        super().__init__()
        self.logger = logger

        (user_layout, user_line_edit) = self.labeled_line_edit("Username")
        (pass_layout, pass_line_edit) = self.labeled_line_edit("Password")
        (host_layout, host_line_edit) = self.labeled_line_edit("Hostname")
        (port_layout, port_line_edit) = self.labeled_line_edit("Port")
        user_line_edit.setText(self.db_user)
        pass_line_edit.setText(self.db_pass)
        host_line_edit.setText(self.db_host)
        port_line_edit.setText(str(self.db_port))
        user_line_edit.textChanged.connect(
            lambda: setattr(self, "db_user", user_line_edit.text())
        )
        pass_line_edit.textChanged.connect(
            lambda: setattr(self, "db_pass", pass_line_edit.text())
        )
        host_line_edit.textChanged.connect(
            lambda: setattr(self, "db_host", host_line_edit.text())
        )
        port_line_edit.textChanged.connect(
            lambda: setattr(self, "db_port", port_line_edit.text())
        )

        attempt_connection_button = QPushButton("Connect")
        attempt_connection_button.setFont(FONT)
        attempt_connection_button.clicked.connect(self.connect)

        self.connection_status = QLabel("Status: Not connected")
        self.connection_status.setFont(FONT)

        self.connection_message = QTextEdit()
        self.connection_message.setFont(FONT)
        self.connection_message.setReadOnly(True)
        self.connection_message.setPlaceholderText(
            "If an error occurs, you will see it here"
        )

        tab_layout = QVBoxLayout()
        for layout in [user_layout, pass_layout, host_layout, port_layout]:
            tab_layout.addLayout(layout)
        tab_layout.addWidget(attempt_connection_button)
        tab_layout.addWidget(self.connection_status)
        tab_layout.addWidget(self.connection_message)

        self.setLayout(tab_layout)

    def connect(self) -> None:
        connection: DatabaseConnection | None
        try:
            self.logger.info("Attempting to connect to backend")
            connection = DatabaseConnection(
                db_name=self.db_name,
                db_user=self.db_user,
                db_pass=self.db_pass,
                db_host=self.db_host,
                db_port=self.db_port,
            )
        except Exception as error:
            self.logger.error(f"Could not instantiate a connection: {error}")
            self.connection_status.setText("Status: Not connected")
            self.connection_message.setText(str(error))
        else:
            self.connection = connection
            self.connection_status.setText("Status: Connected")

    def labeled_line_edit(self, label: str) -> tuple[QHBoxLayout, QLineEdit]:
        input_label = QLabel(f"{label}:")
        input_label.setFont(FONT)
        line_edit = QLineEdit()
        line_edit.setFont(FONT)
        line_edit.setPlaceholderText(label)
        layout = QHBoxLayout()
        layout.addWidget(input_label)
        layout.addWidget(line_edit)
        return (layout, line_edit)


class ConnectionStatus:
    status: str = "Not connected"
