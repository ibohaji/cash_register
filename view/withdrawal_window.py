from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy, QMessageBox
from PySide6.QtCore import Qt
from Model.register import RegisterController

class WithdrawalWindow(QDialog):
    def __init__(self, controller: RegisterController, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent
        self.setWindowTitle("Withdraw Cash")
        self.setFixedSize(400, 300)
        self.setStyleSheet(open("styles/withdrawal_window.css").read())
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Header
        header = QLabel("Withdraw Cash")
        header.setAlignment(Qt.AlignCenter)
        header.setObjectName("header")
        layout.addWidget(header)

        # Withdrawal input
        withdrawal_layout = QVBoxLayout()
        withdrawal_label = QLabel("Withdrawal Amount:")
        self.withdrawal_input = QLineEdit()
        self.withdrawal_input.setPlaceholderText("Enter amount to withdraw")
        withdrawal_layout.addWidget(withdrawal_label)
        withdrawal_layout.addWidget(self.withdrawal_input)
        layout.addLayout(withdrawal_layout)

        # Confirm button
        self.confirm_button = QPushButton("Confirm Withdrawal")
        self.confirm_button.clicked.connect(self.confirm_withdrawal)
        layout.addWidget(self.confirm_button)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(layout)

    def confirm_withdrawal(self):
        try:
            withdrawal_amount = float(self.withdrawal_input.text())
            self.controller.withdraw_cash(withdrawal_amount)
            self.parent.update_cash_inventory()  # Update the cash inventory label
            self.accept()
        except ValueError as e:
            QMessageBox.critical(self, "Withdrawal Error", str(e))
