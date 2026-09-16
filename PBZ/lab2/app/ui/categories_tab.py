from PyQt6.QtWidgets import (
    QAbstractItemView,
    QPushButton,
    QTableWidget,
    QVBoxLayout,
    QWidget,
)

from .. import repository as repo
from .common import fill_table

HEADERS = ["Код", "Название категории"]


class CategoriesTab(QWidget):
    def __init__(self):
        super().__init__()

        self.table = QTableWidget()
        self.table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        refresh_button = QPushButton("Обновить")
        refresh_button.clicked.connect(self.refresh)

        layout = QVBoxLayout(self)
        layout.addWidget(self.table)
        layout.addWidget(refresh_button)

        self.refresh()

    def refresh(self):
        categories = repo.get_categories()
        rows = [(c.category_id, c.category_name) for c in categories]
        fill_table(self.table, HEADERS, rows)