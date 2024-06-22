import json
import os

class CashInventory:
    def __init__(self, filepath='cash_inventory.json'):
        self.filepath = filepath
        self.cash_on_hand = 0.0
        self.load_inventory()

    def load_inventory(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as file:
                data = json.load(file)
                self.cash_on_hand = data.get('cash_on_hand', 0.0)
        else:
            self.save_inventory()

    def save_inventory(self):
        with open(self.filepath, 'w') as file:
            json.dump({'cash_on_hand': self.cash_on_hand}, file)

    def add_cash(self, amount):
        self.cash_on_hand += amount
        self.save_inventory()

    def remove_cash(self, amount):
        if amount <= self.cash_on_hand:
            self.cash_on_hand -= amount
            self.save_inventory()
        else:
            raise ValueError("Insufficient funds")

    def get_cash_on_hand(self):
        return self.cash_on_hand
