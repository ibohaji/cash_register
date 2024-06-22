from typing import List,Tuple
from dataclasses import dataclass,field 
from Model.product import Product 


@dataclass 
class Cart:
    basket:List[Tuple[Product,int]] = field(default_factory=list)

    def get_total_items(self) -> int:
        return len(self.basket)
    
    def get_total_price(self) -> float: 
        total = sum([product.price * qty for product,qty in self.basket])
        return total
    
    def add_item(self,product:Product,qty:int) -> None:
        for i,(p,q) in enumerate(self.basket):
            if p.id == product.id:
                self.basket[i] = (p,q+qty)
                break
        else:
            self.basket.append((product,qty))
        

        
 
    def remove_item(self,product:Product,qty) -> None:
        updated_basket =  []
        for p,q in self.basket:
            if p.id == product.id: 
                if q-qty > 0:
                    updated_basket.append((p,q-qty))
            else:
                updated_basket.append((p,q))
        self.basket = updated_basket


    def get_quantity(self,product:Product) -> int:
        for p,q in self.basket:
            if p.id == product.id:
                return q
    
 
