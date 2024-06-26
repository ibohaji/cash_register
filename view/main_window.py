from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QApplication, QStackedLayout, QSizePolicy, QGridLayout
from PySide6.QtCore import Qt
from Model.product import Product, ProductRepository
from Model.register import RegisterController
from view.cart_view import CartView
from view.button_grid import ButtonGrid
from view.transaction_history_view import TransactionHistoryView
from view.withdrawal_window import WithdrawalWindow
from view.product_management import ProductManagementView
import sys

class MainWindow(QMainWindow):
    def __init__(self, app: QApplication, product_repo: ProductRepository) -> None:
        super().__init__()
        self.app = app
        self.product_repo = product_repo
        self.controller = RegisterController(product_repo)
        self.setWindowTitle("Cash Register System")
        self.setObjectName("main-window")

        # Initialize side_area before calling initUI
        self.side_area = CartView(self.controller, self)
        
        self.initUI()

    def initUI(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # Navigation bar
        nav_bar = QHBoxLayout()
        nav_bar.setSpacing(10)
        nav_bar.setContentsMargins(10, 10, 10, 10)
        nav_bar.setAlignment(Qt.AlignTop)

        self.category_button = QPushButton("Categories")
        self.category_button.setObjectName("nav-button")
        self.category_button.clicked.connect(self.showCategoryView)
        nav_bar.addWidget(self.category_button)

        self.transaction_history_button = QPushButton("Transaction History")
        self.transaction_history_button.setObjectName("nav-button")
        self.transaction_history_button.clicked.connect(self.showTransactionHistoryView)
        nav_bar.addWidget(self.transaction_history_button)

        self.product_management_button = QPushButton("Add Products")
        self.product_management_button.setObjectName("nav-button")
        self.product_management_button.clicked.connect(self.showProductManagementView)
        nav_bar.addWidget(self.product_management_button)

        main_layout.addLayout(nav_bar)

        # Content layout
        content_layout = QHBoxLayout()
        self.stacked_layout = QStackedLayout()

        # Category view
        self.category_view = QWidget()
        self.initCategoryView()
        self.stacked_layout.addWidget(self.category_view)

        # Product view
        self.product_view = QWidget()
        self.initProductView()
        self.stacked_layout.addWidget(self.product_view)

        # Add product view
        self.product_management_view = ProductManagementView(self.controller)
        self.stacked_layout.addWidget(self.product_management_view)

        # Transaction history view
        self.transaction_history_view = TransactionHistoryView(self.controller, self)
        self.stacked_layout.addWidget(self.transaction_history_view)

        content_layout.addLayout(self.stacked_layout, 4)
        content_layout.addWidget(self.side_area, 1)  # Ensure CartView is always visible

        main_layout.addLayout(content_layout)

        # Load stylesheets
        self.setStyleSheet(open("styles/main_window.css").read())
        self.main_area.setStyleSheet(open("styles/button_grid.css").read())

    def initCategoryView(self):
        layout = QVBoxLayout(self.category_view)
        grid_layout = QGridLayout()
        categories = self.product_repo.storage.categories.keys()
        for idx, category_name in enumerate(categories):
            category_button = QPushButton(category_name)
            category_button.setFixedSize(150, 100)
            category_button.setObjectName("category-button")
            category_button.clicked.connect(lambda checked, category_name=category_name: self.showProductView(category_name))
            grid_layout.addWidget(category_button, idx // 3, idx % 3)
        layout.addLayout(grid_layout)

    def initProductView(self):
        layout = QVBoxLayout(self.product_view)
        content_layout = QHBoxLayout()
        content_layout.setSpacing(10)

        # Main area
        self.main_area = ButtonGrid(self.controller)
        self.main_area.setStyleSheet(open("styles/button_grid.css").read())
        content_layout.addWidget(self.main_area, 4)  # 80% width

        # Side area
        content_layout.addWidget(self.side_area, 1)  # 20% width

        layout.addLayout(content_layout)

    def showCategoryView(self):
        self.stacked_layout.setCurrentWidget(self.category_view)

    def showProductView(self, category_name=None):
        if category_name:
            products = self.product_repo.storage.categories[category_name].products
            self.main_area.generate_buttons(products, self.side_area.add_to_cart)
        self.stacked_layout.setCurrentWidget(self.product_view)

    def showTransactionHistoryView(self):
        self.transaction_history_view.update_transaction_list()
        self.stacked_layout.setCurrentWidget(self.transaction_history_view)

    def showProductManagementView(self):
        self.stacked_layout.setCurrentWidget(self.product_management_view)

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
