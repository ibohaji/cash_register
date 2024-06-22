from typing import List
from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton,QSizePolicy
from PySide6.QtCore import Qt
from Model.product import Product
from Model.register import RegisterController

class ButtonGrid(QWidget):
    def __init__(self, controller: RegisterController):
        super().__init__()
        self.controller = controller
        self.layout = QGridLayout(self)
        self.layout.setHorizontalSpacing(10)  # Horizontal spacing
        self.layout.setVerticalSpacing(10)    # Vertical spacing

    def generate_buttons(self, products: List[Product], on_button_click):
        clear_layout(self.layout)

        num_columns = 3  # Set the number of columns
        num_rows = (len(products) + num_columns - 1) // num_columns  # Calculate the number of rows
        for index, product in enumerate(products):
            button = QPushButton(f"{product.name}\n${product.price:.2f}")
            style_button(button)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Ensure buttons expand
            button.clicked.connect(lambda checked, product=product: on_button_click(product))
            row = index // num_columns
            col = index % num_columns
            self.layout.addWidget(button, row, col)

def style_button(button):
    button.setStyleSheet("""
        QPushButton {
            background-color: #d3d3d3;
            color: #333;
            padding: 10px;
            text-align: center;
            font-size: 14px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        QPushButton:hover {
            background-color: #c0c0c0;
        }
    """)

def clear_layout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()
