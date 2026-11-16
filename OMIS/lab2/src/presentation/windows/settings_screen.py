from typing import Callable

from PyQt6.QtWidgets import QCheckBox, QFrame, QHBoxLayout, QLabel

from src.presentation import styles
from src.presentation.windows.base_screen import BaseScreen

# Настроек нет в модели классов, поэтому они живут только в интерфейсе
SETTINGS = [
    ("Отправлять уведомление до окончания брони?", True),
    ("Автоматически продлевать бронь?", False),
    ("Автоматически продлевать занятое место?", False),
    ("Списывать деньги с карты в случае их отсутствия на кошельке?", True),
]


class SettingsScreen(BaseScreen):
    """«Настройки системы» (сценарий 12)."""

    def __init__(self, on_back: Callable[[], None]):
        super().__init__(on_back)
        self.__checkboxes: list[QCheckBox] = []

        for text, checked in SETTINGS:
            item = QFrame()
            item.setObjectName("card")
            item.setStyleSheet(styles.CARD_STYLE)
            label = QLabel(text)
            label.setWordWrap(True)
            label.setStyleSheet("font-size: 12px; font-weight: 600;")
            checkbox = QCheckBox()
            checkbox.setChecked(checked)
            checkbox.setStyleSheet("QCheckBox::indicator { width: 26px; height: 26px; }")
            self.__checkboxes.append(checkbox)

            row = QHBoxLayout(item)
            row.setContentsMargins(16, 12, 16, 12)
            row.addWidget(label, stretch=1)
            row.addWidget(checkbox)
            self.content.addWidget(item)

        self.content.addStretch()

    def values(self) -> list[bool]:
        return [checkbox.isChecked() for checkbox in self.__checkboxes]
