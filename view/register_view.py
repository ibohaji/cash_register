# register_view.py
from Model.register import RegisterController
from Model.product import Product

class RegisterView:
    def __init__(self):
        self.controller = RegisterController()

    def display_cart(self):
        cart = self.controller.current_cart()
        for product, qty in cart.basket:
            print(f"Product ID: {product.id}, Name: {product.name}, Price: {product.price}, Quantity: {qty}")
        print(f"Total Price: {cart.get_total_price()}")

    def display_receipt(self, receipt):
        print("Receipt:")
        for product, qty in receipt.products:
            print(f"Product ID: {product.id}, Name: {product.name}, Price: {product.price}, Quantity: {qty}")
        print(f"Total: {receipt.total}, Paid: {receipt.paid}, Change: {receipt.change}")

    def display_message(self, message):
        print(message)

    def add_product_to_cart(self, product_id, qty):
        try:
            self.controller.add_item_to_cart(product_id, qty)
            self.display_message("Product added to cart.")
        except ValueError as e:
            self.display_message(str(e))

    def remove_product_from_cart(self, product_id, qty):
        try:
            self.controller.remove_product_from_cart(product_id, qty)
            self.display_message("Product removed from cart.")
        except ValueError as e:
            self.display_message(str(e))

    def checkout(self, payment_amount):
        try:
            receipt = self.controller.checkout(payment_amount)
            self.display_receipt(receipt)
        except ValueError as e:
            self.display_message(str(e))
