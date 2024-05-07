from logging import Logger

from gui.tabs.connection import ConnectionTab


class Tabs:
    connection: ConnectionTab

    def __init__(self, logger: Logger) -> None:
        self.connection = ConnectionTab(logger)
