from gui.main import FONT, SURFACE
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QLabel,
    QLineEdit,
    QHBoxLayout,
    QWidget,
)


class StatusBar(QWidget):
    status: QLabel
    message: QLineEdit

    RESET_DELAY_MS: int = 3000

    def __init__(self) -> None:
        super().__init__()

        self.status = QLabel("")
        self.status.setFont(FONT)
        self.message = QLineEdit()
        self.message.setReadOnly(True)
        self.message.setFont(FONT)

        self.set_idle()
        layout = QHBoxLayout()
        layout.addWidget(self.status)
        layout.addWidget(self.message)
        self.setLayout(layout)

    def set_idle(self) -> None:
        self.status.setText("  IDLE ")
        self.status.setStyleSheet(f"background-color: {SURFACE}; color: black")
        self.message.setText("")

    def set_ok(self, message: str) -> None:
        self.status.setStyleSheet("background-color: LightGreen; color: black")
        self.status.setText("   OK  ")
        self.message.setText(message)
        QTimer.singleShot(self.RESET_DELAY_MS, lambda: self.set_idle())

    def set_warn(self, message: str) -> None:
        self.status.setText("  WARN ")
        self.status.setStyleSheet("background-color: LightSalmon; color: black")
        self.message.setText(message)
        QTimer.singleShot(self.RESET_DELAY_MS, lambda: self.set_idle())

    def set_error(self, message: str) -> None:
        self.status.setText(" ERROR ")
        self.status.setStyleSheet("background-color: IndianRed; color: black")
        self.message.setText(message)
        QTimer.singleShot(self.RESET_DELAY_MS, lambda: self.set_idle())
