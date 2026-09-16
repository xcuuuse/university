from PyQt6.QtWidgets import QMainWindow, QTabWidget

from .categories_tab import CategoriesTab
from .products_tab import ProductsTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Отдел маркетинга — учёт продаж")
        self.resize(1000, 650)
        tabs = QTabWidget()
        tabs.addTab(ProductsTab(), "Товары")
        tabs.addTab(CategoriesTab(), "Категории")
        self.setCentralWidget(tabs)