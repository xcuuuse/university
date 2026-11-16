from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QWidget

from src.presentation import styles


class Overlay(QWidget):
    def __init__(
            self,
            parent: QWidget,
            card_width: int = 340,
            alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter,
            close_on_outside_click: bool = False
    ):
        super().__init__(parent)
        self.__close_on_outside_click = close_on_outside_click

        self.card = QFrame(self)
        self.card.setObjectName("card")
        self.card.setStyleSheet(styles.CARD_STYLE)
        self.card.setFixedWidth(card_width)
        self.card_layout = QVBoxLayout(self.card)
        self.card_layout.setContentsMargins(20, 18, 20, 18)
        self.card_layout.setSpacing(12)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.addWidget(self.card, alignment=alignment)

        self.hide()

    def open(self) -> None:
        parent: Optional[QWidget] = self.parentWidget()
        if parent is not None:
            self.setGeometry(parent.rect())
        self.raise_()
        self.show()

    def close_overlay(self) -> None:
        self.hide()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(*styles.OVERLAY_RGBA))
        painter.end()

    def mousePressEvent(self, event) -> None:
        if self.__close_on_outside_click and not self.card.geometry().contains(event.position().toPoint()):
            self.close_overlay()
        event.accept()
