from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QVBoxLayout,
)

from .. import repository as repo


class ProductDialog(QDialog):
    """product=None — добавление, иначе редактирование."""

    def __init__(self, parent=None, product=None):
        super().__init__(parent)
        self.product = product
        self.setWindowTitle("Товар" if product else "Новый товар")
        self.setMinimumWidth(400)

        self.code_edit = QLineEdit()
        self.name_edit = QLineEdit()
        self.unit_edit = QLineEdit("шт")

        self.category_box = QComboBox()
        for category in repo.get_categories():
            self.category_box.addItem(category.category_name, category.category_id)

        self.manufacturer_box = QComboBox()
        for maker in repo.get_manufacturers():
            self.manufacturer_box.addItem(
                maker.manufacturer_name, maker.manufacturer_id
            )

        form = QFormLayout()
        form.addRow("Код:", self.code_edit)
        form.addRow("Название:", self.name_edit)
        form.addRow("Единица измерения:", self.unit_edit)
        form.addRow("Категория:", self.category_box)
        form.addRow("Производитель:", self.manufacturer_box)

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
            QMessageBox.warning(self, "Внимание", "Укажите код товара")
            return
        if not self.name_edit.text().strip():
            QMessageBox.warning(self, "Внимание", "Укажите название товара")
            return
        if self.category_box.currentData() is None:
            QMessageBox.warning(self, "Внимание", "Нет ни одной категории")
            return
        if self.manufacturer_box.currentData() is None:
            QMessageBox.warning(self, "Внимание", "Нет ни одного производителя")
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