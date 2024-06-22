from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem
from PySide6.QtCore import Qt, QSize
from Model.register import RegisterController
from view.transaction_detail_dialog import TransactionDetailDialog

class TransactionHistoryView(QWidget):
    def __init__(self, controller: RegisterController, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setStyleSheet(open("styles/transaction_history_view.css").read())
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Header
        header = QLabel("Transaction History")
        header.setAlignment(Qt.AlignCenter)
        header.setObjectName("header")
        layout.addWidget(header)

        # Transaction List
        self.transaction_list = QListWidget()
        self.transaction_list.itemClicked.connect(self.show_transaction_details)
        layout.addWidget(self.transaction_list)

        self.setLayout(layout)

    def update_transaction_list(self):
        self.transaction_list.clear()
        receipts = self.controller.get_all_receipts_sorted()
        for receipt in receipts:
            item_text = f"Date: {receipt.timestamp.isoformat()}\nTotal: ${receipt.total:.2f}"
            list_item = QListWidgetItem(item_text)
            list_item.setData(Qt.UserRole, receipt)
            list_item.setSizeHint(QSize(580, 50))
            self.transaction_list.addItem(list_item)

    def show_transaction_details(self, item):
        receipt = item.data(Qt.UserRole)
        dialog = TransactionDetailDialog(receipt, self)
        dialog.exec_()
