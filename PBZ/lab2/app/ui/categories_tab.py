from PyQt6.QtWidgets import (
    QAbstractItemView,
    QPushButton,
    QTableWidget,
    QVBoxLayout,
    QWidget,
)
from app import repository as repo
from app.ui.common import fill_table

HEADERS = ["Code", "Category"]


class CategoriesTab(QWidget):
    def __init__(self):
        super().__init__()
        self.table = QTableWidget()
        self.table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        refresh_button = QPushButton("Update")
        refresh_button.clicked.connect(self.refresh)
        layout = QVBoxLayout(self)
        layout.addWidget(self.table)
        layout.addWidget(refresh_button)
        self.refresh()

    def refresh(self):
        categories = repo.get_categories()
        rows = [(category.category_id, category.category_name) for category in categories]
        fill_table(self.table, HEADERS, rows)