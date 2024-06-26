from PySide6.QtWidgets import QWidget,QDialog, QVBoxLayout, QListWidget, QLabel, QPushButton, QHBoxLayout, QListWidgetItem, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt
from Model.product import Product
from Model.register import RegisterController
from view.checkout_window import CheckoutWindow

class CartView(QWidget):
    def __init__(self, controller: RegisterController, parent):
        super().__init__()
        self.controller = controller
        self.parent = parent
        self.setFixedWidth(300)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)

        self.cart_container = QWidget()
        self.cart_container.setObjectName("cart-container")
        self.cart_container.setStyleSheet(open("styles/cart_view.css").read())
        self.cart_container.setFixedHeight(500)
        cart_layout = QVBoxLayout(self.cart_container)
        cart_layout.setSpacing(0)  # Set spacing to 0

        self.cart_list = QListWidget()
        self.cart_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        cart_layout.addWidget(self.cart_list)

        self.total_price_label = QLabel("Total: 0.00")
        self.total_price_label.setAlignment(Qt.AlignLeft)
        cart_layout.addWidget(self.total_price_label)

        self.checkout_button = QPushButton("Checkout")
        self.checkout_button.clicked.connect(self.checkout)
        cart_layout.addWidget(self.checkout_button)

        layout.addWidget(self.cart_container)
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.update_cart_view()
        self.update_total_price()

    def add_to_cart(self, product: Product):
        self.controller.add_item_to_cart(product, 1)
        self.update_cart_view()
        self.update_total_price()

    def update_cart_view(self):
        self.cart_list.clear()
        for product, quantity in self.controller.current_cart().basket:
            total = product.price * quantity
            cart_item_text = f"{quantity}x {product.name} : {total:.2f}"
            item_widget = QWidget()
            item_layout = QHBoxLayout(item_widget)
            item_layout.setContentsMargins(1, 1, 1, 1)
            item_label = QLabel(cart_item_text)
            item_label.setFixedHeight(25)
            delete_button = QPushButton("Delete")
            delete_button.setFixedSize(40, 15)
            delete_button.setStyleSheet("""
                QPushButton {
                    background-color: #ff4c4c;
                    color: #fff;
                    padding: 3px;
                    font-size: 12px;
                    border: none; /* Remove border */
                    border-radius: 2px;
                    cursor: pointer;
                }
                QPushButton:hover {
                    background-color: #ff1a1a;
                }
            """)
            delete_button.clicked.connect(lambda checked, product=product: self.remove_from_cart(product))
            item_layout.addWidget(item_label, alignment=Qt.AlignLeft)
            item_layout.addWidget(delete_button, alignment=Qt.AlignRight)
            item_widget.setLayout(item_layout)
            item = QListWidgetItem(self.cart_list)
            item.setSizeHint(item_widget.sizeHint())
            self.cart_list.setItemWidget(item, item_widget)

    def update_total_price(self):
        total_price = self.controller.get_total()
        self.total_price_label.setStyleSheet("""
            QLabel {
                background-color: #E5F6DF;
                font-size: 25px;
                font-weight: bold;
                padding: 10px;
            }
        """)
        self.total_price_label.setAlignment(Qt.AlignLeft)
        self.total_price_label.setText(f"Total: {total_price:.2f}")

    def remove_from_cart(self, product: Product):
        self.controller.remove_product_from_cart(product, 1)
        self.update_cart_view()
        self.update_total_price()

    def checkout(self):
        checkout_window = CheckoutWindow(self.controller, self.parent)
        if checkout_window.exec_() == QDialog.Accepted:
            self.update_cart_view()  # Reset cart view
            self.update_total_price()  # Reset total price
