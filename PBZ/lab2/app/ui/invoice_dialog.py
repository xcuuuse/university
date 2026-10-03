from decimal import Decimal, InvalidOperation

from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QDateEdit,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QVBoxLayout,
)

from .. import repository as repo
from .common import fill_table, selected_row, warn

ITEM_HEADERS = ["Product", "Quantity", "Price", "Total"]


def fmt_qty(value):
    """5.000 -> '5', 2.500 -> '2.5'"""
    return format(Decimal(value).normalize(), "f")


def fmt_money(value):
    return f"{Decimal(str(value)):.2f}"


def city_label(city):
    """'Минск, Минская область, Беларусь'; для зарубежных городов без региона."""
    parts = [city.city_name]
    if city.region is not None:
        parts.append(city.region.region_name)
    parts.append(city.country.country_name)
    return ", ".join(parts)


def item_rows(items):
    """Строки таблицы позиций: (товар, количество, цена, сумма)."""
    return [
        (name, fmt_qty(qty), fmt_money(price), fmt_money(qty * price))
        for _, name, qty, price in items
    ]


class InvoiceDialog(QDialog):
    """invoice=None — новая накладная, иначе редактирование."""

    def __init__(self, parent=None, invoice=None):
        super().__init__(parent)
        self.invoice = invoice
        self.setWindowTitle("Invoice" if invoice else "New invoice")
        self.setMinimumSize(680, 560)
        # позиции хранятся в памяти до нажатия OK: [product_id, название, кол-во, цена]
        self.items = []

        self.number_edit = QLineEdit()
        self.date_edit = QDateEdit(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDisplayFormat("dd.MM.yyyy")
        self.date_edit.dateChanged.connect(self.reprice_items)

        self.buyer_box = QComboBox()
        for buyer in repo.get_buyers():
            self.buyer_box.addItem(buyer.buyer_name, buyer.buyer_id)

        self.city_box = QComboBox()
        for city in repo.get_cities():
            self.city_box.addItem(city_label(city), city.city_id)

        form = QFormLayout()
        form.addRow("Number:", self.number_edit)
        form.addRow("Date:", self.date_edit)
        form.addRow("Buyer:", self.buyer_box)
        form.addRow("Destination:", self.city_box)

        # --- добавление позиции ---
        self.product_box = QComboBox()
        for product in repo.get_products():
            self.product_box.addItem(
                f"{product.product_code} – {product.product_name}", product.product_id
            )
        self.qty_edit = QLineEdit()
        self.qty_edit.setPlaceholderText("Quantity")
        self.qty_edit.setMaximumWidth(110)
        add_button = QPushButton("Add item")
        remove_button = QPushButton("Remove item")
        add_button.clicked.connect(self.add_item)
        remove_button.clicked.connect(self.remove_item)

        item_row = QHBoxLayout()
        item_row.addWidget(self.product_box, 1)
        item_row.addWidget(self.qty_edit)
        item_row.addWidget(add_button)
        item_row.addWidget(remove_button)

        self.table = QTableWidget()
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.total_label = QLabel()

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addLayout(item_row)
        layout.addWidget(self.table)
        layout.addWidget(self.total_label)
        layout.addWidget(buttons)

        if invoice:
            self.number_edit.setText(invoice.invoice_number)
            self.date_edit.blockSignals(True)  # без пересчёта сохранённых цен
            self.date_edit.setDate(
                QDate(invoice.doc_date.year, invoice.doc_date.month, invoice.doc_date.day)
            )
            self.date_edit.blockSignals(False)
            self._select(self.buyer_box, invoice.buyer_id)
            self._select(self.city_box, invoice.city_id)
            for item in invoice.items:
                p = item.product
                self.items.append(
                    [p.product_id, f"{p.product_code} – {p.product_name}",
                     Decimal(item.quantity), Decimal(str(item.price))]
                )
        self.refresh_items()

    @staticmethod
    def _select(box, value):
        index = box.findData(value)
        if index >= 0:
            box.setCurrentIndex(index)

    def doc_date(self):
        return self.date_edit.date().toPyDate()

    def refresh_items(self):
        fill_table(self.table, ITEM_HEADERS, item_rows(self.items))
        total = sum((q * p for _, _, q, p in self.items), Decimal("0"))
        self.total_label.setText(f"Total: {fmt_money(total)}")

    def add_item(self):
        product_id = self.product_box.currentData()
        if product_id is None:
            warn(self, "There are no products")
            return
        try:
            quantity = Decimal(self.qty_edit.text().strip().replace(",", "."))
        except InvalidOperation:
            warn(self, "Quantity must be a number")
            return
        if quantity <= 0:
            warn(self, "Quantity must be greater than zero")
            return
        if any(item[0] == product_id for item in self.items):
            warn(self, "This product is already in the invoice")
            return
        # отпускная цена — цена из истории на дату накладной
        price = repo.price_at(product_id, self.doc_date())
        if price is None:
            warn(self, "The product has no price on the invoice date")
            return
        self.items.append(
            [product_id, self.product_box.currentText(), quantity, Decimal(str(price))]
        )
        self.qty_edit.clear()
        self.refresh_items()

    def remove_item(self):
        row = selected_row(self.table)
        if row is None:
            warn(self, "Select an item")
            return
        del self.items[row]
        self.refresh_items()

    def reprice_items(self):
        """При смене даты в НОВОЙ накладной цены берутся заново на новую дату.
        В существующей накладной сохранённые цены не меняются."""
        if self.invoice is not None or not self.items:
            return
        missing = []
        for item in self.items:
            price = repo.price_at(item[0], self.doc_date())
            if price is None:
                missing.append(item[1])
            else:
                item[3] = Decimal(str(price))
        self.refresh_items()
        if missing:
            warn(self, "No price on this date for:\n" + "\n".join(missing))

    def accept(self):
        if not self.number_edit.text().strip():
            warn(self, "Enter the invoice number")
            return
        if self.buyer_box.currentData() is None or self.city_box.currentData() is None:
            warn(self, "Select the buyer and the destination")
            return
        if not self.items:
            warn(self, "The invoice must contain at least one item")
            return
        super().accept()

    def values(self):
        return {
            "number": self.number_edit.text().strip(),
            "doc_date": self.doc_date(),
            "buyer_id": self.buyer_box.currentData(),
            "city_id": self.city_box.currentData(),
            "items": [(pid, qty, price) for pid, _, qty, price in self.items],
        }