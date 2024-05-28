import sys

import qdarkstyle
from gui.main import DatabaseGUI
from PyQt6.QtWidgets import QApplication

# Program entrypoint.
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api="pyqt6"))
    gui = DatabaseGUI()
    gui.show()
    sys.exit(app.exec())
