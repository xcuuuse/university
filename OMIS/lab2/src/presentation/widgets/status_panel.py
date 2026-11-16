from datetime import datetime
from typing import Callable

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout

from src.presentation import styles
from src.presentation.widgets.buttons import BaseButton, OccupyButton, ReleaseButton


class StatusPanel(QFrame):
    def __init__(
            self,
            on_occupy: Callable[[], None],
            on_extend: Callable[[], None],
            on_cancel: Callable[[], None],
            on_release: Callable[[], None]
    ):
        super().__init__()
        self.setObjectName("card")
        self.setStyleSheet(styles.CARD_STYLE + f"QFrame#card {{ border: 1px solid {styles.BUTTON_BLUE}; }}")
        self.setFixedWidth(340)

        self.__title = QLabel()
        self.__subtitle = QLabel()
        self.__details = QLabel()
        for label in (self.__title, self.__subtitle, self.__details):
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.__title.setStyleSheet("font-weight: 700; font-size: 12px;")

        self.__occupy_button = OccupyButton(on_occupy, length=95)
        self.__extend_button = BaseButton("ПРОДЛИТЬ", 95, 36, handler=on_extend)
        self.__cancel_button = BaseButton("СНЯТЬ БРОНЬ", 110, 36, handler=on_cancel)
        self.__release_button = ReleaseButton(on_release, length=300)

        buttons = QHBoxLayout()
        for button in (self.__occupy_button, self.__extend_button,
                       self.__cancel_button, self.__release_button):
            buttons.addWidget(button)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 12)
        layout.addWidget(self.__title)
        layout.addWidget(self.__subtitle)
        layout.addWidget(self.__details)
        layout.addLayout(buttons)

        self.hide()

    def show_booked(self, space_number: int, booking_end: datetime) -> None:
        self.__title.setText(f"ЗАБРОНИРОВАНО: #P{space_number}")
        self.__subtitle.setText(f"ВРЕМЯ ОКОНЧАНИЯ БРОНИ: {styles.format_datetime(booking_end)}")
        self.__details.hide()
        self.__set_buttons(booked=True)
        self.show()

    def show_occupied(self, space_number: int, start: datetime, duration_hours: float, cost: float) -> None:
        self.__title.setText(f"ЗАНЯТО: #P{space_number}")
        self.__subtitle.setText(f"ЗАНЯТО С: {styles.format_datetime(start)}")
        self.__details.setText(
            f"Прошло: {styles.format_duration(duration_hours)}   Стоимость: {cost:.2f} BYN"
        )
        self.__details.show()
        self.__set_buttons(booked=False)
        self.show()

    def __set_buttons(self, booked: bool) -> None:
        for button in (self.__occupy_button, self.__extend_button, self.__cancel_button):
            button.setVisible(booked)
        self.__release_button.setVisible(not booked)
