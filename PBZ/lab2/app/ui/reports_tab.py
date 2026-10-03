from datetime import date

from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QDateEdit,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QVBoxLayout,
    QWidget,
)

from .. import repository as repo
from .common import fill_table, warn

TOP_HEADERS = ["Date", "Buyer", "Address", "Total"]
PRICE_HEADERS = ["Manufacturer", "Product", "Date", "Price"]


def make_date_edit(value):
    edit = QDateEdit(value)
    edit.setCalendarPopup(True)
    edit.setDisplayFormat("dd.MM.yyyy")
    return edit


def make_table():
    table = QTableWidget()
    table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
    return table


class ReportsTab(QWidget):
    def __init__(self):
        super().__init__()

        # --- отчёт 1: покупатели с максимальной суммой на дату ---
        self.top_date = make_date_edit(QDate.currentDate())
        top_button = QPushButton("Show")
        top_button.clicked.connect(self.show_top_buyers)
        self.top_table = make_table()
        self.top_info = QLabel()

        top_row = QHBoxLayout()
        top_row.addWidget(QLabel("Date:"))
        top_row.addWidget(self.top_date)
        top_row.addWidget(top_button)
        top_row.addWidget(self.top_info, 1)

        top_box = QGroupBox("Buyers with the maximum purchase on the date")
        top_layout = QVBoxLayout(top_box)
        top_layout.addLayout(top_row)
        top_layout.addWidget(self.top_table)

        self.product_box = QComboBox()
        self.from_date = make_date_edit(QDate(2025, 1, 1))
        self.to_date = make_date_edit(QDate.currentDate())
        price_button = QPushButton("Show")
        price_button.clicked.connect(self.show_price_changes)
        self.price_table = make_table()
        self.price_info = QLabel()
        price_row = QHBoxLayout()
        price_row.addWidget(QLabel("Product:"))
        price_row.addWidget(self.product_box, 1)
        price_row.addWidget(QLabel("From:"))
        price_row.addWidget(self.from_date)
        price_row.addWidget(QLabel("To:"))
        price_row.addWidget(self.to_date)
        price_row.addWidget(price_button)
        price_box = QGroupBox("Price changes of a product")
        price_layout = QVBoxLayout(price_box)
        price_layout.addLayout(price_row)
        price_layout.addWidget(self.price_info)
        price_layout.addWidget(self.price_table)
        layout = QVBoxLayout(self)
        layout.addWidget(top_box)
        layout.addWidget(price_box)
        fill_table(self.top_table, TOP_HEADERS, [])
        fill_table(self.price_table, PRICE_HEADERS, [])
        self.refresh()

    def refresh(self):
        """Обновляет список товаров и подставляет дату последней накладной."""
        current = self.product_box.currentData()
        self.product_box.clear()
        for product in repo.get_products():
            self.product_box.addItem(
                f"{product.product_code} – {product.product_name}", product.product_id
            )
        index = self.product_box.findData(current)
        if index >= 0:
            self.product_box.setCurrentIndex(index)
        invoices = repo.get_invoices()
        if invoices:  # список отсортирован от новых к старым
            d = invoices[0].doc_date
            self.top_date.setDate(QDate(d.year, d.month, d.day))

    def show_top_buyers(self):
        day = self.top_date.date().toPyDate()
        rows = [
            (d.strftime("%d.%m.%Y"), name, address, f"{total:.2f}")
            for d, name, address, total in repo.top_buyers(day)
        ]
        fill_table(self.top_table, TOP_HEADERS, rows)
        self.top_info.setText("" if rows else "No sales on this date")

    def show_price_changes(self):
        product_id = self.product_box.currentData()
        if product_id is None:
            warn(self, "Select a product")
            return
        date_from = self.from_date.date().toPyDate()
        date_to = self.to_date.date().toPyDate()
        if date_from > date_to:
            warn(self, "The start date is later than the end date")
            return
        rows = [
            (maker, product, d.strftime("%d.%m.%Y"), f"{price:.2f}")
            for maker, product, d, price in repo.price_changes(
                product_id, date_from, date_to
            )
        ]
        fill_table(self.price_table, PRICE_HEADERS, rows)
        self.price_info.setText("" if rows else "No price changes in this period")