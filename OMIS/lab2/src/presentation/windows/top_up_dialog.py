from typing import Callable

from PyQt6.QtWidgets import QDoubleSpinBox, QHBoxLayout, QLabel, QWidget

from src.presentation.widgets.buttons import BaseButton
from src.presentation.widgets.overlay import Overlay


class TopUpDialog(Overlay):
    """Форма пополнения кошелька (на макете её нет, придумана самостоятельно)."""

    def __init__(self, parent: QWidget, on_confirm: Callable[[float], bool]):
        super().__init__(parent)
        self.__on_confirm = on_confirm

        title = QLabel("ПОПОЛНЕНИЕ КОШЕЛЬКА")
        title.setStyleSheet("font-size: 13px; font-weight: 700;")
        self.__amount = QDoubleSpinBox()
        self.__amount.setRange(0.0, 10000.0)
        self.__amount.setDecimals(2)
        self.__amount.setSuffix(" BYN")

        buttons = QHBoxLayout()
        buttons.addWidget(BaseButton("Отмена", 130, 44, handler=self.close_overlay))
        buttons.addWidget(BaseButton("ОК", 130, 44, handler=self.__confirm))

        self.card_layout.addWidget(title)
        self.card_layout.addWidget(QLabel("Сумма пополнения:"))
        self.card_layout.addWidget(self.__amount)
        self.card_layout.addLayout(buttons)

    def open(self) -> None:
        self.__amount.setValue(10.0)
        super().open()

    def __confirm(self) -> None:
        if self.__on_confirm(self.__amount.value()):
            self.close_overlay()
