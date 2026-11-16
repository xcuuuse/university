from typing import Callable

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QWidget

from src.presentation import styles
from src.presentation.widgets.buttons import BaseButton


class BaseScreen(QWidget):
    """Полноэкранная страница на тёмно-синем фоне со стрелкой «назад» в углу."""

    def __init__(self, on_back: Callable[[], None]):
        super().__init__()
        self.setObjectName("screen")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(f"QWidget#screen {{ {styles.DARK_BACKGROUND} }}")

        self.content = QVBoxLayout(self)
        self.content.setContentsMargins(16, 16, 16, 16)
        self.content.setSpacing(14)
        self.content.addWidget(BaseButton("←", 34, 34, styles.CARD_GREY, on_back))
