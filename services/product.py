import logging
from database import session
from datetime import datetime
from typing import List
from models.product import Product
from services.general import Scraping
from services.price import PriceHandler

logger = logging.getLogger('app')
class ProductOperations:
    def __init__(self, product: Product) -> None:
        self.product = product
        logger.debug(f'Product handler initialized for product id {self.product.id}')

    @staticmethod
    def get_all_products() -> List:
        products = session.query(Product).all()
        return products

    def update_price_from_site(self):
        new_price = self.get_price_from_site()
        try:
            old_price = self.product.prices[-1].price
        except IndexError:
            old_price = 0
        if old_price == new_price:
            logger.info(f'Цена не изменилась. Старая цена = {old_price}, новая цена = {new_price}\n-------------------------------')
        else:
            logger.info(f'!!!ЦЕНА ИЗМЕНИЛАСЬ!!!. Старая цена = {old_price}, новая цена = {new_price}\n-------------------------------')
            price_handler = PriceHandler(self.product)
            price_handler.append_new_price(new_price)
        
    def get_price_from_site(self):
        price_int = Scraping(self.product.url).get_price_from_soup()
        return price_int

    def get_name_and_price(self):
        scrap = Scraping(self.product.url)
        price_int = scrap.get_price_from_soup()
        self.product.name = scrap.get_name_from_soup()
        return {'name': self.product.name, 'price': price_int}
        
    def get_attributes_from_site(self, **kwargs):
        scrap = Scraping(self.product.url)
        if kwargs['name']:
            scrap.get_name_from_soup()
        if kwargs['price']:
            scrap.get_price_from_soup()
        else:
            raise NotImplementedError
    
class MultipleProductsManager:
    def __init__(self, products_list: List) -> None:
        self.products_list = products_list

    def check_for_price_updates(self):
        for product in self.products_list:
            logger.info(f'Product {product.name}, prices {[p.price for p in product.prices]}')
            product_handler = ProductOperations(product=product)
            product_handler.update_price_from_site()
