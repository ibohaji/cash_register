import sys
from PySide6.QtWidgets import QApplication
from Model.product import Product, ProductRepository
from view.main_window import MainWindow
from Model.register import RegisterController

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Example stock items
    stock_items = [
        Product(id="1", name="Pepsi", price=10.00),
        Product(id="2", name="Coca Cola", price=20.00),
        Product(id="3", name="Velo", price=30.00),
        Product(id="4", name="Kitkat", price=40.00),
        Product(id="5", name="Snickers", price=50.00),
        Product(id="6", name="Lays", price=60.00),
        Product(id="7", name="Marlboro", price=70.00),
        Product(id="8", name="Juice", price=80.00),
        Product(id="9", name="Chocolate", price=90.00),
        Product(id="10", name="Candy", price=100.00),
        Product(id="11", name="Gum", price=110.00),
        Product(id="12", name="Milk", price=120.00),
        Product(id="13", name="Bread", price=130.00),
        Product(id="14", name="Butter", price=140.00),
        Product(id="15", name="Cheese", price=150.00),
    ]

    product_repo = ProductRepository()

    # Add example stock items to product repository under different categories
    for product in stock_items:
        category_name = "Beverages" if product.name in ["Pepsi", "Coca Cola", "Velo", "Juice"] else "Snacks"
        product_repo.create_product(product, qty=10, category=category_name)


    window = MainWindow(app, product_repo)
    window.run()
