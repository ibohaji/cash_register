from typing import List
from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QSizePolicy
from PySide6.QtCore import Qt
from Model.product import Product
from Model.register import RegisterController

class ButtonGrid(QWidget):
    def __init__(self, controller: RegisterController):
        super().__init__()
        self.controller = controller
        self.layout = QGridLayout(self)
        self.layout.setHorizontalSpacing(2)  # Horizontal spacing
        self.layout.setVerticalSpacing(4)    # Vertical spacing
        self.setStyleSheet(open("styles/button_grid.css").read())

    def generate_buttons(self, products: List[Product], on_button_click):
        clear_layout(self.layout)

        num_columns = 5  # Set the number of columns
        num_rows = (len(products) + num_columns - 1) // num_columns  # Calculate the number of rows
        for index, product in enumerate(products):
            button = QPushButton(f"{product.name}\n${product.price:.2f}")
            button.setObjectName("product-button")
            button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            button.setFixedSize(150, 100)  # Ensure buttons have fixed size
            button.clicked.connect(lambda checked, product=product: on_button_click(product))
            row = index // num_columns
            col = index % num_columns
            self.layout.addWidget(button, row, col)

def clear_layout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()
