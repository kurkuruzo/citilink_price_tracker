from datetime import datetime
import logging
from database import session
from models.price import Price
from models.product import Product

logger = logging.getLogger('app')
class PriceHandler:
    def __init__(self, product: Product) -> None:
        self.product = product
        logger.info(f'Price handler initialized for product id {self.product.id}')

    # def update_price(self, new_price: int):
    #     existing_price = self.product.prices[-1]
    #     if new_price != existing_price:
    #         self.append_new_price(self.product)
        
    #     return self.product.prices
        
    def append_new_price(self, new_price: int) -> Price:
        new_price_obj = Price(price=new_price, product_id=self.product.id, date=datetime.now())
        session.add(new_price_obj)
        session.flush()
        return new_price_obj