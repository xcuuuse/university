from typing import Callable

from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtGui import QColor, QFont, QPainter
from PyQt6.QtWidgets import QLabel, QWidget

from src.domain.entities.user import User
from src.presentation import styles
from src.presentation.widgets.buttons import BaseButton
from src.presentation.windows.base_screen import BaseScreen


class Avatar(QWidget):
    """Круглая аватарка с первой буквой имени (фото профиля в модели нет)."""

    def __init__(self):
        super().__init__()
        self.setFixedSize(110, 110)
        self.__letter = "?"

    def set_name(self, name: str) -> None:
        self.__letter = name[:1].upper() or "?"
        self.update()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(styles.CARD_GREY))
        painter.drawEllipse(QRectF(self.rect()))
        painter.setPen(QColor(styles.DARK_BLUE))
        painter.setFont(QFont("Sans", 40, QFont.Weight.Bold))
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.__letter)
        painter.end()


class AccountScreen(BaseScreen):
    """«Просмотр и изменение данных аккаунта» (сценарий 10)."""

    def __init__(self, on_back: Callable[[], None], on_edit_profile: Callable[[], None]):
        super().__init__(on_back)
        self.__avatar = Avatar()
        self.__name = QLabel()
        self.__name.setStyleSheet(f"color: {styles.TEXT_LIGHT}; font-size: 26px; font-weight: 700;")
        self.__user_id = QLabel()
        self.__user_id.setStyleSheet(f"color: {styles.TEXT_LIGHT}; font-size: 11px;")

        center = Qt.AlignmentFlag.AlignHCenter
        self.content.addSpacing(30)
        self.content.addWidget(self.__avatar, alignment=center)
        self.content.addWidget(self.__name, alignment=center)
        self.content.addWidget(self.__user_id, alignment=center)
        self.content.addSpacing(10)
        self.content.addWidget(
            BaseButton("Изменить настройки профиля", 240, 44, styles.CARD_GREY, on_edit_profile),
            alignment=center
        )
        self.content.addStretch()

    def show_user(self, user: User) -> None:
        self.__avatar.set_name(user.name)
        self.__name.setText(user.name)
        self.__user_id.setText(f"id: #{user.id}")
