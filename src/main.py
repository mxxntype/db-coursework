import logging
import sys

import qdarkstyle
from gui.gui import DatabaseGUI
from PyQt6.QtWidgets import (
    QApplication,
)

# Program entrypoint.
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api="pyqt6"))
    gui = DatabaseGUI()  # noqa: F841
    sys.exit(app.exec())
