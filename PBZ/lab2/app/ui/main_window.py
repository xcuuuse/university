from PyQt6.QtWidgets import QMainWindow, QTabWidget
from .categories_tab import CategoriesTab
from .invoices_tab import InvoicesTab
from .products_tab import ProductsTab
from .reports_tab import ReportsTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sales")
        self.resize(1000, 650)
        self.tabs = QTabWidget()
        self.tabs.addTab(ProductsTab(), "Products")
        self.tabs.addTab(InvoicesTab(), "Invoices")
        self.tabs.addTab(ReportsTab(), "Reports")
        self.tabs.addTab(CategoriesTab(), "Categories")
        self.tabs.currentChanged.connect(self.on_tab_changed)
        self.setCentralWidget(self.tabs)

    def on_tab_changed(self, index):
        refresh = getattr(self.tabs.widget(index), "refresh", None)
        if refresh:
            refresh()