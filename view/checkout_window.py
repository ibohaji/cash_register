from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy, QMessageBox
from PySide6.QtCore import Qt
from Model.register import RegisterController

class CheckoutWindow(QDialog):
    def __init__(self, controller: RegisterController, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent
        self.setWindowTitle("Checkout")
        self.setFixedSize(600, 500)
        self.setStyleSheet(open("styles/checkout_window.css").read())
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        self.total_price = self.controller.get_total()

        # Header
        header = QLabel("Checkout")
        header.setAlignment(Qt.AlignCenter)
        header.setObjectName("header")
        layout.addWidget(header)

        # Amount due label
        self.amount_due_label = QLabel(f"Amount Due: ${self.total_price:.2f}")
        self.amount_due_label.setObjectName("amount-due")
        layout.addWidget(self.amount_due_label)

        # Payment input
        payment_layout = QVBoxLayout()
        payment_label = QLabel("Payment Amount:")
        self.payment_input = QLineEdit()
        self.payment_input.setPlaceholderText("Enter payment amount")
        payment_layout.addWidget(payment_label)
        payment_layout.addWidget(self.payment_input)
        layout.addLayout(payment_layout)

        # Change due label
        self.change_due_label = QLabel("Change Due: $0.00")
        self.change_due_label.setObjectName("change-due")
        layout.addWidget(self.change_due_label)

        self.payment_input.textChanged.connect(self.update_change_due)

        # Confirm button
        self.confirm_button = QPushButton("Confirm Payment")
        self.confirm_button.clicked.connect(self.confirm_payment)
        layout.addWidget(self.confirm_button)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(layout)

    def update_change_due(self):
        try:
            payment_amount = float(self.payment_input.text())
            change_due = payment_amount - self.total_price
            self.change_due_label.setText(f"Change Due: ${change_due:.2f}")
        except ValueError:
            self.change_due_label.setText("Change Due: $0.00")

    def confirm_payment(self):
        try:
            payment_amount = float(self.payment_input.text())
            receipt = self.controller.checkout(payment_amount)
            self.payment_input.setReadOnly(True)  # Make the payment input immutable
            self.show_receipt(receipt)
            self.parent.update_cash_inventory()  # Update the cash inventory label
        except ValueError as e:
            QMessageBox.critical(self, "Payment Error", str(e))

    def show_receipt(self, receipt):
        layout = self.layout()
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        receipt_text = f"Total: ${receipt.total:.2f}\nPaid: ${receipt.paid:.2f}\nChange: ${receipt.change:.2f}"
        for product, qty in receipt.products:
            receipt_text += f"\n{product.name} x{qty} @ ${product.price:.2f} each"

        receipt_label = QLabel(receipt_text)
        receipt_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-family: 'Courier New', monospace;
            }
        """)
        layout.addWidget(receipt_label)

        finish_button = QPushButton("Finish")
        finish_button.clicked.connect(self.finish_transaction)
        layout.addWidget(finish_button)

    def finish_transaction(self):
        self.parent.side_area.update_cart_view()  # Reset cart view
        self.parent.side_area.update_total_price()  # Reset total price
        self.parent.controller.reset_cart()  # Reset cart in the controller
        self.accept()
