from logging import Logger

from gui.tabs.authors import AuthorTab
from gui.tabs.connection import ConnectionTab
from gui.tabs.read import ReadTab


class Tabs:
    connection: ConnectionTab
    read: ReadTab
    author: AuthorTab

    def __init__(self, logger: Logger) -> None:
        self.connection = ConnectionTab(logger)
        self.read = ReadTab(self.connection.connection, logger)
        self.author = AuthorTab(self.connection.connection, logger)
