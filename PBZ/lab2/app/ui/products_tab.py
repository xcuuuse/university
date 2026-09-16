from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSplitter,
    QTableWidget,
    QVBoxLayout,
    QWidget,
)

from .. import repository as repo
from .common import ask, fill_table, selected_row, warn
from .price_dialog import PriceDialog
from .product_dialog import ProductDialog

PRODUCT_HEADERS = ["Код", "Название", "Ед.", "Категория", "Производитель"]
PRICE_HEADERS = ["Дата", "Цена"]


class ProductsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.product_ids = []
        self.price_ids = []

        # --- панель фильтров ---
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Поиск по названию")
        self.search_edit.textChanged.connect(self.refresh_products)

        self.category_box = QComboBox()
        self.category_box.currentIndexChanged.connect(self.refresh_products)

        filters = QHBoxLayout()
        filters.addWidget(QLabel("Найти:"))
        filters.addWidget(self.search_edit, 1)
        filters.addWidget(QLabel("Категория:"))
        filters.addWidget(self.category_box)

        # --- таблица товаров ---
        self.product_table = QTableWidget()
        self.product_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.product_table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.product_table.itemSelectionChanged.connect(self.refresh_prices)
        self.product_table.doubleClicked.connect(self.edit_product)

        add_button = QPushButton("Добавить")
        edit_button = QPushButton("Изменить")
        delete_button = QPushButton("Удалить")
        add_button.clicked.connect(self.add_product)
        edit_button.clicked.connect(self.edit_product)
        delete_button.clicked.connect(self.delete_product)

        product_buttons = QHBoxLayout()
        product_buttons.addWidget(add_button)
        product_buttons.addWidget(edit_button)
        product_buttons.addWidget(delete_button)
        product_buttons.addStretch()

        product_box = QWidget()
        product_layout = QVBoxLayout(product_box)
        product_layout.setContentsMargins(0, 0, 0, 0)
        product_layout.addLayout(filters)
        product_layout.addWidget(self.product_table)
        product_layout.addLayout(product_buttons)

        # --- история цен ---
        self.price_table = QTableWidget()
        self.price_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        add_price_button = QPushButton("Добавить цену")
        delete_price_button = QPushButton("Удалить цену")
        add_price_button.clicked.connect(self.add_price)
        delete_price_button.clicked.connect(self.delete_price)

        price_buttons = QHBoxLayout()
        price_buttons.addWidget(add_price_button)
        price_buttons.addWidget(delete_price_button)
        price_buttons.addStretch()

        price_box = QGroupBox("История цен выбранного товара")
        price_layout = QVBoxLayout(price_box)
        price_layout.addWidget(self.price_table)
        price_layout.addLayout(price_buttons)

        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.addWidget(product_box)
        splitter.addWidget(price_box)
        splitter.setSizes([400, 200])

        layout = QVBoxLayout(self)
        layout.addWidget(splitter)

        self.reload_categories()
        self.refresh_products()

    # --- загрузка данных ---

    def reload_categories(self):
        self.category_box.blockSignals(True)
        self.category_box.clear()
        self.category_box.addItem("— все —", None)
        for category in repo.get_categories():
            self.category_box.addItem(category.category_name, category.category_id)
        self.category_box.blockSignals(False)

    def refresh_products(self):
        products = repo.get_products(
            name=self.search_edit.text().strip() or None,
            category_id=self.category_box.currentData(),
        )
        self.product_ids = [p.product_id for p in products]
        rows = [
            (
                p.product_code,
                p.product_name,
                p.product_unit,
                p.category.category_name,
                p.manufacturer.manufacturer_name,
            )
            for p in products
        ]
        fill_table(self.product_table, PRODUCT_HEADERS, rows)
        self.refresh_prices()

    def refresh_prices(self):
        product_id = self.current_product_id()
        if product_id is None:
            self.price_ids = []
            fill_table(self.price_table, PRICE_HEADERS, [])
            return
        prices = repo.get_prices(product_id)
        self.price_ids = [p.price_history_id for p in prices]
        rows = [(p.start_date.strftime("%d.%m.%Y"), p.price) for p in prices]
        fill_table(self.price_table, PRICE_HEADERS, rows)

    def current_product_id(self):
        row = selected_row(self.product_table)
        return self.product_ids[row] if row is not None else None

    # --- действия над товарами ---

    def add_product(self):
        dialog = ProductDialog(self)
        if dialog.exec():
            try:
                repo.add_product(**dialog.values())
            except Exception as error:
                warn(self, f"Не удалось добавить товар:\n{error}")
                return
            self.refresh_products()

    def edit_product(self):
        product_id = self.current_product_id()
        if product_id is None:
            warn(self, "Выберите товар")
            return
        product = repo.get_product(product_id)
        dialog = ProductDialog(self, product)
        if dialog.exec():
            try:
                repo.update_product(product_id, **dialog.values())
            except Exception as error:
                warn(self, f"Не удалось сохранить товар:\n{error}")
                return
            self.refresh_products()

    def delete_product(self):
        product_id = self.current_product_id()
        if product_id is None:
            warn(self, "Выберите товар")
            return
        product = repo.get_product(product_id)
        if not ask(self, f"Удалить товар «{product.product_name}»?"):
            return
        try:
            repo.delete_product(product_id)
        except ValueError as error:
            warn(self, str(error))
            return
        self.refresh_products()

    # --- действия над ценами ---

    def add_price(self):
        product_id = self.current_product_id()
        if product_id is None:
            warn(self, "Выберите товар")
            return
        product = repo.get_product(product_id)
        dialog = PriceDialog(self, product.product_name)
        if dialog.exec():
            try:
                repo.add_price(product_id, **dialog.values())
            except Exception as error:
                warn(self, f"Не удалось добавить цену:\n{error}")
                return
            self.refresh_prices()

    def delete_price(self):
        row = selected_row(self.price_table)
        if row is None:
            warn(self, "Выберите цену")
            return
        if not ask(self, "Удалить запись о цене?"):
            return
        repo.delete_price(self.price_ids[row])
        self.refresh_prices()