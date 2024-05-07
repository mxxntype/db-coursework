import sys

import qdarkstyle
from PyQt6.QtWidgets import QApplication

from gui.main import DatabaseGUI

# Program entrypoint.
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api="pyqt6"))
    gui = DatabaseGUI()
    gui.show()
    sys.exit(app.exec())
