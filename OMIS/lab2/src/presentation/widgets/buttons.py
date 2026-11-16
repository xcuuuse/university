from typing import Callable, Optional

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton, QWidget

from src.presentation import styles

Handler = Optional[Callable[[], None]]


class BaseButton(QPushButton):
    def __init__(
            self,
            text: str,
            length: int = 150,
            width: int = 40,
            color: str = styles.BUTTON_BLUE,
            handler: Handler = None,
            parent: Optional[QWidget] = None
    ):
        super().__init__(text, parent)
        self.__length = length
        self.__width = width
        self.__color = color
        self._handler = handler
        self.setFixedSize(length, width)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.__apply_style()
        self.clicked.connect(self.press)

    @property
    def length(self) -> int:
        return self.__length

    @property
    def button_width(self) -> int:
        return self.__width

    @property
    def color(self) -> str:
        return self.__color

    def set_handler(self, handler: Handler) -> None:
        self._handler = handler

    def press(self) -> None:
        if self._handler is not None:
            self._handler()

    def __apply_style(self) -> None:
        radius = min(self.__width, self.__length) // 2
        font_size = 18 if len(self.text()) == 1 else 11
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.__color};
                color: {styles.TEXT_DARK};
                border: none;
                border-radius: {radius}px;
                font-size: {font_size}px;
                font-weight: 600;
            }}
            QPushButton:hover {{ border: 2px solid {styles.DARK_BLUE}; }}
            QPushButton:disabled {{
                background-color: {styles.BUTTON_DISABLED};
                color: #6B6F86;
            }}
        """)


class BookingButton(BaseButton):
    def __init__(self, handler: Handler = None, length: int = 120, width: int = 36,
                 parent: Optional[QWidget] = None):
        super().__init__("ЗАБРОНИРОВАТЬ", length, width, handler=handler, parent=parent)

    def create_booking(self) -> None:
        if self._handler is not None:
            self._handler()

    def press(self) -> None:
        self.create_booking()


class OccupyButton(BaseButton):
    def __init__(self, handler: Handler = None, length: int = 120, width: int = 36,
                 parent: Optional[QWidget] = None):
        super().__init__("ЗАНЯТЬ", length, width, handler=handler, parent=parent)

    def start_session(self) -> None:
        if self._handler is not None:
            self._handler()

    def press(self) -> None:
        self.start_session()


class ReleaseButton(BaseButton):
    def __init__(self, handler: Handler = None, length: int = 300, width: int = 40,
                 parent: Optional[QWidget] = None):
        super().__init__("ОСВОБОДИТЬ", length, width, handler=handler, parent=parent)

    def end_session(self) -> None:
        if self._handler is not None:
            self._handler()

    def press(self) -> None:
        self.end_session()
