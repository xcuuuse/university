from typing import Any, Callable

from PyQt6.QtWidgets import QMessageBox, QWidget

from src.application.exceptions import ApplicationError


def safe_call(parent: QWidget, func: Callable[..., Any], *args) -> tuple[bool, Any]:
    try:
        return True, func(*args)
    except ApplicationError as error:
        QMessageBox.warning(parent, "Ошибка", str(error))
        return False, None
