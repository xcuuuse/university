from datetime import date
from decimal import Decimal, InvalidOperation
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import (
    QDateEdit,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QVBoxLayout,
)


class PriceDialog(QDialog):
    def __init__(self, parent=None, product_name=""):
        super().__init__(parent)
        self.setWindowTitle(f"New price - {product_name}")
        self.setMinimumWidth(320)
        self.price_edit = QLineEdit()
        self.date_edit = QDateEdit(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDisplayFormat("dd.MM.yyyy")

        form = QFormLayout()
        form.addRow("Price:", self.price_edit)
        form.addRow("From (date):", self.date_edit)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(buttons)

    def accept(self):
        try:
            price = Decimal(self.price_edit.text().replace(",", "."))
        except (InvalidOperation, ValueError):
            QMessageBox.warning(self, "Warning", "Price must be a number")
            return
        if price <= 0:
            QMessageBox.warning(self, "Warning", "Price must be > 0")
            return
        super().accept()

    def values(self):
        qdate = self.date_edit.date()
        return {
            "price": Decimal(self.price_edit.text().replace(",", ".")),
            "start_date": date(qdate.year(), qdate.month(), qdate.day()),
        }