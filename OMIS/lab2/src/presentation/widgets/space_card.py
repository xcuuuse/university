from typing import Callable

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout

from src.domain.entities.parking_space import ParkingSpace
from src.presentation import styles
from src.presentation.widgets.buttons import BookingButton, OccupyButton


class SpaceCard(QFrame):
    def __init__(
            self,
            space: ParkingSpace,
            can_occupy: bool,
            can_book: bool,
            selected: bool,
            on_occupy: Callable[[int], None],
            on_book: Callable[[int], None],
            on_select: Callable[[int], None]
    ):
        super().__init__()
        self.__number = space.number
        self.__on_select = on_select

        self.setObjectName("card")
        self.setFixedSize(300, 150)
        border = f"border: 3px solid {styles.DARK_BLUE};" if selected else ""
        self.setStyleSheet(styles.CARD_STYLE + f"QFrame#card {{ {border} }}")
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        info = QVBoxLayout()
        info.setSpacing(2)
        title = QLabel(f"Парковочное место\n#P{space.number}")
        title.setStyleSheet("font-size: 12px; font-weight: 600;")
        status = QLabel(styles.STATUS_TEXT.get(space.status, space.status))
        status.setStyleSheet(f"font-weight: 700; color: {styles.STATUS_COLORS.get(space.status)};")
        price = QLabel(f"Стоимость: {styles.format_price(space.price_per_hour)}")
        coords = QLabel(f"Координаты: {space.location.pos_x:.4f},\n{space.location.pos_y:.4f}")
        coords.setStyleSheet("font-size: 10px;")
        for widget in (title, status, price, coords):
            info.addWidget(widget)
        info.addStretch()

        occupy_button = OccupyButton(lambda: on_occupy(self.__number), length=120)
        occupy_button.setEnabled(can_occupy)
        book_button = BookingButton(lambda: on_book(self.__number), length=120)
        book_button.setEnabled(can_book)

        buttons = QVBoxLayout()
        buttons.addStretch()
        buttons.addWidget(occupy_button)
        buttons.addWidget(book_button)
        buttons.addStretch()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 10, 10, 10)
        layout.addLayout(info, stretch=1)
        layout.addLayout(buttons)

    def mousePressEvent(self, event) -> None:
        self.__on_select(self.__number)
        super().mousePressEvent(event)
