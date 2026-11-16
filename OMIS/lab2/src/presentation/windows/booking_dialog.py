from datetime import datetime, timedelta
from typing import Callable

from PyQt6.QtCore import QDateTime
from PyQt6.QtWidgets import QDateTimeEdit, QGridLayout, QHBoxLayout, QLabel, QWidget

from src.presentation.widgets.buttons import BaseButton
from src.presentation.widgets.overlay import Overlay

DATETIME_FORMAT = "dd.MM.yyyy HH:mm"


class BookingDialog(Overlay):
    """Форма «Бронь парковочного места» (сценарий 3).

    on_confirm(номер, начало, конец) возвращает True, если бронь создана: тогда форма закрывается.
    """

    def __init__(self, parent: QWidget, on_confirm: Callable[[int, datetime, datetime], bool]):
        super().__init__(parent)
        self.__on_confirm = on_confirm
        self.__space_number = 0

        self.__title = QLabel()
        self.__title.setStyleSheet("font-size: 14px; font-weight: 700;")

        self.__start_edit = QDateTimeEdit()
        self.__end_edit = QDateTimeEdit()
        for edit in (self.__start_edit, self.__end_edit):
            edit.setDisplayFormat(DATETIME_FORMAT)
            edit.setCalendarPopup(True)

        form = QGridLayout()
        form.addWidget(QLabel("Время начала:"), 0, 0)
        form.addWidget(self.__start_edit, 0, 1)
        form.addWidget(QLabel("Время окончания:"), 1, 0)
        form.addWidget(self.__end_edit, 1, 1)

        buttons = QHBoxLayout()
        buttons.addWidget(BaseButton("Отмена", 130, 44, handler=self.close_overlay))
        buttons.addWidget(BaseButton("ОК", 130, 44, handler=self.__confirm))

        self.card_layout.addWidget(self.__title)
        self.card_layout.addLayout(form)
        self.card_layout.addLayout(buttons)

    def open_for(self, space_number: int) -> None:
        self.__space_number = space_number
        self.__title.setText(f"БРОНЬ ПАРКОВОЧНОГО МЕСТА #P{space_number}")
        now = datetime.now().replace(second=0, microsecond=0)
        self.__start_edit.setDateTime(QDateTime(now))
        self.__end_edit.setDateTime(QDateTime(now + timedelta(hours=1)))
        self.open()

    def __confirm(self) -> None:
        start = self.__start_edit.dateTime().toPyDateTime()
        end = self.__end_edit.dateTime().toPyDateTime()
        if self.__on_confirm(self.__space_number, start, end):
            self.close_overlay()
