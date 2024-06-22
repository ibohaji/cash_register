from unittest import mock 
import pytest 
from Model import register,product

class TestRegister:

    @pytest.fixture 
    def sample_product(self):
        return product.Product(id="1234",name="velo",price=56.0) 

    @pytest.fixture
    def reg(self):
        return register.RegisterController() 

    def test_add_to_cart(self,reg,sample_product):
        reg.add_item_to_cart(sample_product,3) 
        current_cart = reg.current_cart()
        assert (sample_product,3) == current_cart.basket[0]

    def test_delete_product(self,reg,sample_product)  -> None: 
        reg.add_item_to_cart(sample_product,1) 
        reg.remove_product_from_cart(sample_product,1)
        current_cart = reg.current_cart()
        assert len(current_cart.basket) == 0 

    def test_get_total_price(self,reg,sample_product) -> None:
        reg.add_item_to_cart(sample_product,3) 
        assert reg.get_total() == 168.0

    def test_get_total_items(self,reg,sample_product) -> None:
        reg.add_item_to_cart(sample_product,3) 
        assert reg.current_cart().get_total_items() == 1
        
    def test_checkout(self,reg,sample_product) -> None:
        reg.add_item_to_cart(sample_product,3) 
        recipt = reg.checkout(200.0)
        assert recipt.total == 168.0
        assert recipt.paid == 200.0
        assert recipt.change == 32.0
    
    def test_checkout_insufficient_funds(self,reg,sample_product) -> None:
        reg.add_item_to_cart(sample_product,3) 
        with pytest.raises(ValueError):
            reg.checkout(100.0)

