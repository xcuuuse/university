from typing import Callable

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget

from src.presentation import styles
from src.presentation.widgets.buttons import BaseButton
from src.presentation.widgets.overlay import Overlay


class SideMenu(Overlay):
    def __init__(
            self,
            parent: QWidget,
            on_account: Callable[[], None],
            on_wallet: Callable[[], None],
            on_settings: Callable[[], None]
    ):
        super().__init__(
            parent,
            card_width=220,
            alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop,
            close_on_outside_click=True
        )
        close_button = BaseButton("←", 32, 32, styles.BUTTON_BLUE, self.close_overlay)
        self.card_layout.addWidget(close_button)
        for text, handler in (("Аккаунт", on_account), ("Кошелёк", on_wallet), ("Настройки", on_settings)):
            self.card_layout.addWidget(BaseButton(text, 180, 44, handler=self.__then_close(handler)))

    def __then_close(self, handler: Callable[[], None]) -> Callable[[], None]:
        def wrapper() -> None:
            self.close_overlay()
            handler()
        return wrapper
