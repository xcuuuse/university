from PyQt6.QtCore import QDate, Qt
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QDateEdit,
    QGroupBox,
    QHBoxLayout,
    QPushButton,
    QSplitter,
    QTableWidget,
    QVBoxLayout,
    QWidget,
)
from .. import repository as repo
from .common import ask, fill_table, selected_row, warn
from .invoice_dialog import (
    ITEM_HEADERS,
    InvoiceDialog,
    city_label,
    fmt_money,
    item_rows,
)

INVOICE_HEADERS = ["Number", "Date", "Buyer", "Destination", "Total"]


class InvoicesTab(QWidget):
    def __init__(self):
        super().__init__()
        self.invoice_ids = []
        self.period_check = QCheckBox("Period:")
        self.from_edit = QDateEdit(QDate(2025, 1, 1))
        self.to_edit = QDateEdit(QDate.currentDate())
        for edit in (self.from_edit, self.to_edit):
            edit.setCalendarPopup(True)
            edit.setDisplayFormat("dd.MM.yyyy")
            edit.setEnabled(False)
            edit.dateChanged.connect(self.refresh_invoices)
        self.period_check.toggled.connect(self.from_edit.setEnabled)
        self.period_check.toggled.connect(self.to_edit.setEnabled)
        self.period_check.toggled.connect(self.refresh_invoices)
        filters = QHBoxLayout()
        filters.addWidget(self.period_check)
        filters.addWidget(self.from_edit)
        filters.addWidget(self.to_edit)
        filters.addStretch()
        self.invoice_table = QTableWidget()
        self.invoice_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.invoice_table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.invoice_table.itemSelectionChanged.connect(self.refresh_items)
        self.invoice_table.doubleClicked.connect(self.edit_invoice)
        add_button = QPushButton("Add")
        edit_button = QPushButton("Change")
        delete_button = QPushButton("Delete")
        add_button.clicked.connect(self.add_invoice)
        edit_button.clicked.connect(self.edit_invoice)
        delete_button.clicked.connect(self.delete_invoice)
        buttons = QHBoxLayout()
        buttons.addWidget(add_button)
        buttons.addWidget(edit_button)
        buttons.addWidget(delete_button)
        buttons.addStretch()
        top = QWidget()
        top_layout = QVBoxLayout(top)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.addLayout(filters)
        top_layout.addWidget(self.invoice_table)
        top_layout.addLayout(buttons)
        self.items_table = QTableWidget()
        items_box = QGroupBox("Invoice items")
        items_layout = QVBoxLayout(items_box)
        items_layout.addWidget(self.items_table)
        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.addWidget(top)
        splitter.addWidget(items_box)
        splitter.setSizes([420, 200])
        layout = QVBoxLayout(self)
        layout.addWidget(splitter)
        self.refresh_invoices()

    def refresh(self):
        self.refresh_invoices()

    def refresh_invoices(self):
        date_from = date_to = None
        if self.period_check.isChecked():
            date_from = self.from_edit.date().toPyDate()
            date_to = self.to_edit.date().toPyDate()
        invoices = repo.get_invoices(date_from, date_to)
        self.invoice_ids = [inv.invoice_id for inv in invoices]
        rows = [
            (
                inv.invoice_number,
                inv.doc_date.strftime("%d.%m.%Y"),
                inv.buyer.buyer_name,
                city_label(inv.city),
                fmt_money(inv.total),
            )
            for inv in invoices
        ]
        fill_table(self.invoice_table, INVOICE_HEADERS, rows)
        self.refresh_items()

    def refresh_items(self):
        invoice_id = self.current_invoice_id()
        if invoice_id is None:
            fill_table(self.items_table, ITEM_HEADERS, [])
            return
        invoice = repo.get_invoice(invoice_id)
        rows = item_rows(
            [
                (i.product_id, f"{i.product.product_code} – {i.product.product_name}",
                 i.quantity, i.price)
                for i in invoice.items
            ]
        )
        fill_table(self.items_table, ITEM_HEADERS, rows)

    def current_invoice_id(self):
        row = selected_row(self.invoice_table)
        return self.invoice_ids[row] if row is not None else None

    def add_invoice(self):
        dialog = InvoiceDialog(self)
        if dialog.exec():
            try:
                repo.add_invoice(**dialog.values())
            except Exception as error:
                warn(self, f"Could not save the invoice:\n{error}")
                return
            self.refresh_invoices()

    def edit_invoice(self):
        invoice_id = self.current_invoice_id()
        if invoice_id is None:
            warn(self, "Select an invoice")
            return
        dialog = InvoiceDialog(self, repo.get_invoice(invoice_id))
        if dialog.exec():
            try:
                repo.update_invoice(invoice_id, **dialog.values())
            except Exception as error:
                warn(self, f"Could not save the invoice:\n{error}")
                return
            self.refresh_invoices()

    def delete_invoice(self):
        invoice_id = self.current_invoice_id()
        if invoice_id is None:
            warn(self, "Select an invoice")
            return
        invoice = repo.get_invoice(invoice_id)
        if not ask(self, f"Delete invoice {invoice.invoice_number}?"):
            return
        repo.delete_invoice(invoice_id)
        self.refresh_invoices()