from Model.cash_inventory import CashInventory
from Model.cart import Cart
from Model.product import Product
from Model.product import ProductRepository
from dataclasses import dataclass, field
from typing import List, Tuple
from datetime import datetime
import json 
import os


TRANSACTION_FILE = 'transactions.json'

@dataclass
class Receipt:
    products: List[Tuple[Product, int]] = field(default_factory=list)
    total: float = 0.0
    paid: float = 0.0
    change: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self):
        return {
            "products": [(product.__dict__, quantity) for product, quantity in self.products],
            "total": self.total,
            "paid": self.paid,
            "change": self.change,
            "timestamp": self.timestamp.isoformat()
        }

    @staticmethod
    def from_dict(data):
        products = [(Product(**product_data), quantity) for product_data, quantity in data["products"]]
        timestamp = datetime.fromisoformat(data["timestamp"])
        return Receipt(products=products, total=data["total"], paid=data["paid"], change=data["change"], timestamp=timestamp)

class RegisterController:
    def __init__(self,productRepository:ProductRepository):
        self.cart = Cart()
        self.receipts: List[Receipt] = []
        self.cash_inventory = CashInventory()
        self.load_receipts()  
        self.productRepo = productRepository

    def load_receipts(self):
        if os.path.exists(TRANSACTION_FILE):
            with open(TRANSACTION_FILE, 'r') as file:
                data = json.load(file)
                self.receipts = [Receipt.from_dict(receipt) for receipt in data]

    def save_receipts(self):
        with open(TRANSACTION_FILE, 'w') as file:
            json.dump([receipt.to_dict() for receipt in self.receipts], file, indent=4)

    def current_cart(self) -> Cart:
        return self.cart

    def get_total(self) -> float:
        return self.cart.get_total_price()

    def checkout(self, payment_amount: float) -> Receipt:
        total_price = self.get_total()

        if total_price > payment_amount:
            raise ValueError("Insufficient funds")

        change = payment_amount - total_price
        self.cash_inventory.add_cash(total_price)
        receipt = self.generate_receipt(total_price, payment_amount, change)
        self.receipts.append(receipt)
        self.save_receipts()
        self.reset_cart()
        return receipt

    def add_item_to_cart(self, product: Product, qty: int) -> None:
        self.cart.add_item(product, qty)

    def remove_product_from_cart(self, product: Product, qty: int) -> None:
        self.cart.remove_item(product, qty)

    def generate_receipt(self, total_price: float, paid: float, change: float) -> Receipt:
        return Receipt(products=self.cart.basket, total=total_price, paid=paid, change=change)

    def reset_cart(self):
        self.cart = Cart()

    def withdraw_cash(self, amount: float):
        self.cash_inventory.remove_cash(amount)

    def get_all_receipts_sorted(self) -> List[Receipt]:
        return sorted(self.receipts, key=lambda r: r.timestamp)
