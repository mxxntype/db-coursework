from logging import Logger

from database.credentials import READER
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QFrame,
    QMainWindow,
    QTabWidget,
)

# Font, shared between all other modules.
FONT_FAMILY: str = "IosevkaTerm NF"
FONT_SIZE: int = 24
FONT: QFont = QFont(FONT_FAMILY, FONT_SIZE)

# Some colors.
SUBTEXT = "#99abb8"
SURFACE = "#60798B"
ACCENT = "#259AE9"


def vertical_separator():
    separator = QFrame()
    separator.setFrameShape(QFrame.Shape.VLine)
    separator.setFrameShadow(QFrame.Shadow.Sunken)
    return separator


def horizontal_separator():
    separator = QFrame()
    separator.setFrameShape(QFrame.Shape.HLine)
    separator.setFrameShadow(QFrame.Shadow.Sunken)
    return separator


def trim_str(string: str, length: int) -> str:
    if len(string) > length:
        return f"{string[:length]}..."
    else:
        return string


from database.connection import PgDatabase  # noqa: E402
from gui.tabs.mod import Tabs  # noqa: E402
from log.main import create_named_logger  # noqa: E402


class DatabaseGUI(QMainWindow):
    db: PgDatabase | None = None
    logger: Logger = create_named_logger("GUI")
    font: QFont = FONT
    tabs: Tabs

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Вартанян А.А. Курсовая работа")
        self.setGeometry(900, 1600, 1600, 900)

        # Create the tabs.
        self.tabs = Tabs(self.logger)
        self.tab_widget = QTabWidget()
        self.tab_widget.setFont(self.font)
        self.tab_widget.setStyleSheet("QTabWidget {font-weight: bold}")

        # Load the tabs.
        self.tab_widget.addTab(self.tabs.read, " Публикации ")
        self.tab_widget.addTab(self.tabs.author, " Авторы ")
        self.tab_widget.addTab(self.tabs.author, " Авторы ")
        # self.tab_widget.addTab(self.tabs.maintenance, " Система обеспечения ")
        self.tab_widget.addTab(self.tabs.connection, " Подключение к системе ")

        # Wire up the remaining signals.
        self.tabs.connection.connection.on_connect.connect(self.full_refresh)
        self.tabs.connection.connect_as(credentials=READER)
        # self.tabs.connection.connection.task_transaction()

        # Display the tab widget.
        self.setCentralWidget(self.tab_widget)

    # Perform a full refresh of the UI.
    def full_refresh(self) -> None:
        self.tabs.read.list_posts()
        self.tabs.author.refresh()
