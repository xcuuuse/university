from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem


def fill_table(table, headers, rows):
    """Заполняет QTableWidget. rows — список кортежей, только для чтения."""
    table.clearContents()
    table.setColumnCount(len(headers))
    table.setHorizontalHeaderLabels(headers)
    table.setRowCount(len(rows))
    for i, row in enumerate(rows):
        for j, value in enumerate(row):
            item = QTableWidgetItem("" if value is None else str(value))
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            table.setItem(i, j, item)
    table.resizeColumnsToContents()


def selected_row(table):
    """Индекс выделенной строки или None."""
    rows = table.selectionModel().selectedRows()
    return rows[0].row() if rows else None


def warn(parent, text):
    QMessageBox.warning(parent, "Внимание", text)


def ask(parent, text):
    answer = QMessageBox.question(
        parent,
        "Подтверждение",
        text,
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
    )
    return answer == QMessageBox.StandardButton.Yes