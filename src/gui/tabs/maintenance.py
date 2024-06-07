from logging import Logger

from database.connection import PgDatabase
from gui.main import FONT
from gui.status import StatusBar
from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class MaintenanceTab(QWidget):
    logger: Logger
    connection: PgDatabase
    layout: QVBoxLayout
    statusbar: StatusBar
    layout: QVBoxLayout

    area_w: QWidget
    button_layout: QVBoxLayout

    def __init__(self, connection: PgDatabase, logger: Logger) -> None:
        super().__init__()
        self.connection = connection
        self.logger = logger
        self.connection.on_connect.connect(self.refresh)
        self.statusbar = StatusBar()

        # Add all the buttons.
        self.button_layout = QVBoxLayout()
        self.button_layout.addWidget(
            self.create_maintenance_button(
                "#3(a). Выполнить составной многотабличный запрос с CASE-выражением",
                self.connection.task_case,
            )
        )
        self.button_layout.addWidget(
            self.create_maintenance_button(
                "#3(b). Загрузить данные из многотабличного VIEW",
                self.connection.task_view,
            )
        )
        self.button_layout.addWidget(
            self.create_maintenance_button(
                "#3(c). Загрузить данные из материализованного представления",
                self.connection.task_materialized_view,
            )
        )
        self.button_layout.addWidget(
            self.create_maintenance_button(
                "#3(d). Выполнить запрос с подзапросом в SELECT",
                self.connection.task_subquery_select,
            )
        )
        self.button_layout.addWidget(
            self.create_maintenance_button(
                "#3(d). Выполнить запрос с подзапросом в WHERE",
                self.connection.task_subquery_where,
            )
        )
        self.button_layout.addWidget(
            self.create_maintenance_button(
                "#3(d). Выполнить запрос с подзапросом в FROM",
                self.connection.task_subquery_from,
            )
        )
        self.button_layout.addWidget(
            self.create_maintenance_button(
                "#3(d). Выполнить кореллированый подзапрос №1",
                self.connection.task_correlated_1,
            )
        )
        self.button_layout.addWidget(
            self.create_maintenance_button(
                "#3(d). Выполнить кореллированый подзапрос №2",
                self.connection.task_correlated_2,
            )
        )
        self.button_layout.addWidget(
            self.create_maintenance_button(
                "#3(d). Выполнить кореллированый подзапрос №3",
                self.connection.task_correlated_3,
            )
        )
        self.button_layout.addWidget(
            self.create_maintenance_button(
                "#8. Удалить некачественные публикации и выделить успешные, очистить старые номера телефонов",
                self.connection.task_transaction,
            )
        )

        self.area_w = QWidget()
        self.area_w.setLayout(self.button_layout)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.area_w)
        self.layout.addWidget(QLabel(""))  # Padding.
        self.layout.addWidget(self.statusbar)
        self.layout.setStretch(self.layout.count() - 2, 1)
        self.setLayout(self.layout)

    def refresh(self) -> None:
        match self.connection.credentials.user:
            case "admin":
                self.area_w.setHidden(False)
                self.statusbar.set_idle()

            case _:
                self.area_w.setHidden(True)
                self.statusbar.set_warn(
                    message="Данная вкладка доступна только администратору.",
                    transient=False,
                )

    def create_maintenance_button(
        self,
        label: str,
        callback,
    ) -> QPushButton:
        def wrapper(self: MaintenanceTab, callback):
            self.statusbar.set_info("Запрос выполняется...")
            callback()
            self.statusbar.set_ok("Запрос выполнен успешно!")

        button = QPushButton(label.ljust(100))
        button.setFont(FONT)
        button.clicked.connect(lambda: wrapper(self, callback))
        return button
