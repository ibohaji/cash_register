import uuid 
from typing import Optional,List,Tuple,Dict 
from dataclasses import field,dataclass
from Model.database import MongoDB


@dataclass
class Product:
    id:str 
    name:str 
    price:float 

@dataclass 
class Category: 
    name:str 
    products: List[Product] = field(default_factory = list)

@dataclass 
class Catalogue: 
    categories: Dict[str,Category] = field(default_factory=dict)


class ProductRepository:
    def __init__(self) -> None:
        self.storage = Catalogue()
        return 
    """ 
    def __init__(self)  -> None:
        self.db = MongoDB() 
        try:

            self.collection = self.db.get_collection()
        except Exception as err:
            print("there is an errrrrrrrrrrrror")
        self.menu_items = self.load_meanu()
""" 


    def create_product(self,product:Product,qty:int,category:str): 
        if category not in self.storage.categories:
            self.storage.categories[category] = Category(name=category)
        self.storage.categories[category].products.append(product)
        return product


    def load_meanu(self):
        return list(self.collection.find({}))
    
    def get_product(self,product_id:str):
        product_data = self.menu_items.find_one({"id": product_id})
        if product_data:
            product_data.pop("_id")  
            return Product(**product_data)
        return None 
    
    def list_products(self)-> list[Product]:
        products = self.collection.find()
        return [Product(**{k:v for k,v  in product_data.items() if k!="_id"}) for product_data in products]    
   
    def delete_all_products(self):
        result = self.collection.delete_many({})
        print(f"Deleted {result.deleted_count} products.")



