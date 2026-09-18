from PyQt6.QtWidgets import QMainWindow, QTabWidget
from app.ui.categories_tab import CategoriesTab
from app.ui.products_tab import ProductsTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sales")
        self.resize(1000, 650)
        tabs = QTabWidget()
        tabs.addTab(ProductsTab(), "Products")
        tabs.addTab(CategoriesTab(), "Categories")
        self.setCentralWidget(tabs)