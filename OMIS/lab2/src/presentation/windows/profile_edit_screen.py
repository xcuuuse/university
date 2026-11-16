from typing import Callable

from PyQt6.QtWidgets import QMessageBox

from src.presentation import styles
from src.presentation.widgets.buttons import BaseButton
from src.presentation.windows.base_screen import BaseScreen


class ProfileEditScreen(BaseScreen):

    def __init__(self, on_back: Callable[[], None], on_change_name: Callable[[], None]):
        super().__init__(on_back)
        self.content.addSpacing(10)
        self.content.addWidget(
            BaseButton("Загрузить новое фото профиля", 388, 44, styles.CARD_GREY, self.__upload_photo)
        )
        self.content.addWidget(
            BaseButton("Изменить имя пользователя", 388, 44, styles.CARD_GREY, on_change_name)
        )
        self.content.addStretch()

    def __upload_photo(self) -> None:
        QMessageBox.information(
            self, "Фото профиля",
            "Загрузка фото не реализована: фото профиля отсутствует в объектной модели."
        )
