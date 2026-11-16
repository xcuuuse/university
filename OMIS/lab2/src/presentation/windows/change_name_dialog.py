from typing import Callable

from PyQt6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QWidget

from src.presentation.widgets.buttons import BaseButton
from src.presentation.widgets.overlay import Overlay


class ChangeNameDialog(Overlay):
    """Форма «Изменение имени пользователя».

    on_confirm(имя) возвращает True при успехе. И «ОК», и «Отмена» ведут
    на просмотр аккаунта (диаграмма состояний): это делает on_finish.
    """

    def __init__(self, parent: QWidget, on_confirm: Callable[[str], bool], on_finish: Callable[[], None]):
        super().__init__(parent)
        self.__on_confirm = on_confirm
        self.__on_finish = on_finish

        title = QLabel("ИЗМЕНЕНИЕ ИМЕНИ ПОЛЬЗОВАТЕЛЯ")
        title.setStyleSheet("font-size: 13px; font-weight: 700;")
        self.__name_edit = QLineEdit()
        self.__name_edit.setPlaceholderText("Введите новое имя")
        self.__name_edit.setStyleSheet(
            "QLineEdit { background: #555; color: white; border-radius: 16px; padding: 8px 14px; }"
        )

        buttons = QHBoxLayout()
        buttons.addWidget(BaseButton("Отмена", 130, 44, handler=self.__cancel))
        buttons.addWidget(BaseButton("ОК", 130, 44, handler=self.__confirm))

        self.card_layout.addWidget(title)
        self.card_layout.addWidget(self.__name_edit)
        self.card_layout.addLayout(buttons)

    def open(self) -> None:
        self.__name_edit.clear()
        super().open()
        self.__name_edit.setFocus()

    def __confirm(self) -> None:
        if self.__on_confirm(self.__name_edit.text()):
            self.close_overlay()
            self.__on_finish()

    def __cancel(self) -> None:
        self.close_overlay()
        self.__on_finish()
