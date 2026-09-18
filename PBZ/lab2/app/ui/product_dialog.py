from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QVBoxLayout,
)
from app import repository as repo

class ProductDialog(QDialog):
    def __init__(self, parent=None, product=None):
        super().__init__(parent)
        self.product = product
        self.setWindowTitle("Product" if product else "New product")
        self.setMinimumWidth(400)
        self.code_edit = QLineEdit()
        self.name_edit = QLineEdit()
        self.unit_edit = QLineEdit("pieces")
        self.category_box = QComboBox()
        for category in repo.get_categories():
            self.category_box.addItem(category.category_name, category.category_id)

        self.manufacturer_box = QComboBox()
        for maker in repo.get_manufacturers():
            self.manufacturer_box.addItem(
                maker.manufacturer_name, maker.manufacturer_id
            )

        form = QFormLayout()
        form.addRow("Code:", self.code_edit)
        form.addRow("Name:", self.name_edit)
        form.addRow("Unit of measurement:", self.unit_edit)
        form.addRow("Category:", self.category_box)
        form.addRow("Manufacturer:", self.manufacturer_box)
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(buttons)
        if product:
            self.code_edit.setText(product.product_code)
            self.name_edit.setText(product.product_name)
            self.unit_edit.setText(product.product_unit)
            self._select(self.category_box, product.category_id)
            self._select(self.manufacturer_box, product.manufacturer_id)

    @staticmethod
    def _select(box, value):
        index = box.findData(value)
        if index >= 0:
            box.setCurrentIndex(index)

    def accept(self):
        if not self.code_edit.text().strip():
            QMessageBox.warning(self, "Warning", "Enter the product code")
            return
        if not self.name_edit.text().strip():
            QMessageBox.warning(self, "Warning", "Enter the product name")
            return
        if self.category_box.currentData() is None:
            QMessageBox.warning(self, "Warning", "No categories")
            return
        if self.manufacturer_box.currentData() is None:
            QMessageBox.warning(self, "Warning", "No manufacturers")
            return
        super().accept()

    def values(self):
        return {
            "code": self.code_edit.text().strip(),
            "name": self.name_edit.text().strip(),
            "unit": self.unit_edit.text().strip() or "шт",
            "category_id": self.category_box.currentData(),
            "manufacturer_id": self.manufacturer_box.currentData(),
        }