from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextEdit
from PySide6.QtCore import Qt
from Model.register import Receipt

class TransactionDetailDialog(QDialog):
    def __init__(self, receipt: Receipt, parent=None):
        super().__init__(parent)
        self.receipt = receipt
        self.setWindowTitle("Transaction Details")
        self.setFixedSize(400, 500)
        self.setStyleSheet(open("styles/transaction_detail_dialog.css").read())
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Header
        header = QLabel("Transaction Details")
        header.setAlignment(Qt.AlignCenter)
        header.setObjectName("header")
        layout.addWidget(header)

        # Transaction details
        details = QTextEdit()
        details.setReadOnly(True)
        details.setText(self.format_receipt_details())
        layout.addWidget(details)

        self.setLayout(layout)

    def format_receipt_details(self):
        details = f"Date: {self.receipt.timestamp.isoformat()}\n"
        details += f"Total: ${self.receipt.total:.2f}\n"
        details += f"Paid: ${self.receipt.paid:.2f}\n"
        details += f"Change: ${self.receipt.change:.2f}\n"
        details += "Products:\n"
        for product, quantity in self.receipt.products:
            details += f"  - {product.name} x{quantity} @ ${product.price:.2f} each\n"
        return details
