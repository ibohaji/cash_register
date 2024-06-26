from PySide6.QtWidgets import QWidget

class ProductManagementView(QWidget):
    def __init__(self,controller):
        super().__init__()
        self.controller = controller 


