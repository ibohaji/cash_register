from typing import List
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QApplication, QSpacerItem, QSizePolicy, QStackedLayout
from PySide6.QtCore import Qt
from Model.product import Product
from Model.register import RegisterController
from view.cart_view import CartView
from view.button_grid import ButtonGrid
from view.transaction_history_view import TransactionHistoryView
from view.withdrawal_window import WithdrawalWindow
import sys 

class MainWindow(QMainWindow):
    def __init__(self, app: QApplication, products: List[Product]) -> None:
        super().__init__()
        self.app = app
        self.products = products
        self.controller = RegisterController()
        self.setWindowTitle("Cash Register System")
        self.setStyleSheet(open("styles/main_window.css").read())
        self.initUI()

    def initUI(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        self.stacked_layout = QStackedLayout()
        main_layout.addLayout(self.stacked_layout)

        # Product view
        self.product_view = QWidget()
        self.initProductView()
        self.stacked_layout.addWidget(self.product_view)

        # Transaction history view
        self.transaction_history_view = TransactionHistoryView(self.controller, self)
        self.stacked_layout.addWidget(self.transaction_history_view)

        # Navigation buttons
        nav_layout = QHBoxLayout()
        main_layout.addLayout(nav_layout)

        self.product_button = QPushButton("Products")
        self.product_button.clicked.connect(self.showProductView)
        nav_layout.addWidget(self.product_button)

        self.transaction_history_button = QPushButton("Transaction History")
        self.transaction_history_button.clicked.connect(self.showTransactionHistoryView)
        nav_layout.addWidget(self.transaction_history_button)

    def initProductView(self):
        product_layout = QVBoxLayout(self.product_view)
        content_layout = QHBoxLayout()
        content_layout.setSpacing(10)
        product_layout.addLayout(content_layout)

        # Main area
        self.main_area = ButtonGrid(self.controller)
        content_layout.addWidget(self.main_area, 4)  # 80% width

        # Side area
        self.side_area = CartView(self.controller, self)
        content_layout.addWidget(self.side_area, 1)  # 20% width

        # Generate buttons for stock items
        self.main_area.generate_buttons(self.products, self.side_area.add_to_cart)

        # Footer layout
        footer_layout = QHBoxLayout()
        footer_layout.setSpacing(10)
        footer_layout.setContentsMargins(0, 0, 0, 0)
        product_layout.addLayout(footer_layout)

        # Withdrawal button
        self.withdrawal_button = QPushButton("Withdraw Cash")
        self.withdrawal_button.clicked.connect(self.open_withdrawal_window)
        self.withdrawal_button.setFixedWidth(150)
        footer_layout.addWidget(self.withdrawal_button, alignment=Qt.AlignLeft)

        # Spacer to push the cash inventory label to the right
        footer_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Cash inventory label
        self.cash_inventory_label = QLabel(f"Cash on Hand: ${self.controller.cash_inventory.get_cash_on_hand():.2f}")
        self.cash_inventory_label.setObjectName("cash-inventory")
        footer_layout.addWidget(self.cash_inventory_label, alignment=Qt.AlignRight)

    def showProductView(self):
        self.stacked_layout.setCurrentWidget(self.product_view)

    def showTransactionHistoryView(self):
        self.transaction_history_view.update_transaction_list()
        self.stacked_layout.setCurrentWidget(self.transaction_history_view)

    def update_cash_inventory(self):
        self.cash_inventory_label.setText(f"Cash on Hand: ${self.controller.cash_inventory.get_cash_on_hand():.2f}")

    def open_withdrawal_window(self):
        withdrawal_window = WithdrawalWindow(self.controller, self)
        withdrawal_window.exec_()

    def run(self):
        self.show()
        sys.exit(self.app.exec())

    def reinitUI(self):
        self.initUI()
        self.update()
