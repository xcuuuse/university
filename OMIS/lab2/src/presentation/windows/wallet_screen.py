from typing import Callable

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QLabel, QMessageBox, QVBoxLayout

from src.presentation import styles
from src.presentation.widgets.buttons import BaseButton
from src.presentation.windows.base_screen import BaseScreen

LINKED_CARD = "**** **** **** 1234"


class WalletScreen(BaseScreen):
    """«Просмотр и пополнение кошелька» (сценарий 11)."""

    def __init__(self, on_back: Callable[[], None], on_top_up: Callable[[], None]):
        super().__init__(on_back)

        card = QFrame()
        card.setObjectName("card")
        card.setStyleSheet(styles.CARD_STYLE)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 16, 20, 16)

        title = QLabel("Кошелёк 1")
        title.setStyleSheet("font-size: 28px; font-weight: 700;")
        self.__balance = QLabel()
        self.__balance.setStyleSheet("font-size: 20px; font-weight: 600;")
        card_text = QLabel(f"Привязанная карта:\n{LINKED_CARD}")
        card_text.setStyleSheet("font-size: 16px; font-weight: 600;")

        card_layout.addWidget(title)
        card_layout.addWidget(self.__balance)
        card_layout.addWidget(card_text)
        card_layout.addWidget(BaseButton("Пополнить", 340, 44, handler=on_top_up))

        self.content.addWidget(card)
        self.content.addSpacing(10)
        self.content.addWidget(
            BaseButton("+", 56, 56, styles.CARD_GREY, self.__add_wallet),
            alignment=Qt.AlignmentFlag.AlignHCenter
        )
        self.content.addStretch()

    def show_balance(self, balance: float) -> None:
        self.__balance.setText(f"Баланс: {balance:.2f} BYN")

    def __add_wallet(self) -> None:
        QMessageBox.information(
            self, "Кошелёк",
            "Добавление кошелька не реализовано: по модели у пользователя ровно один кошелёк."
        )
