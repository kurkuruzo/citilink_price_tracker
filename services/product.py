import logging
from database import session
from datetime import datetime
from typing import List
from models.product import Product
from services.general import Scrapping
from services.price import PriceHandler

logger = logging.getLogger('app')
class ProductOperations:
    def __init__(self, product: Product) -> None:
        self.product = product
        print(f'Product handler initialized for product id {self.product.id}')

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
            print(f'Цена не изменилась. Старая цена = {old_price}, новая цена = {new_price}')
        else:
            print(f'!!!ЦЕНА ИЗМЕНИЛАСЬ!!!. Старая цена = {old_price}, новая цена = {new_price}')
            price_handler = PriceHandler(self.product)
            price_handler.append_new_price(new_price)
        

    def get_price_from_soup(self, bs):
        price_element = bs.find(class_="ProductHeader__price-default_current-price")
        price_int = int(price_element.string.replace(" ", ""))
        return price_int
    
    def get_name_from_soup(self, bs):
        name_element = bs.find(class_='ProductHeader__title')
        self.product.name = name_element.string.strip()
        self.product.update_date = datetime.now()

    def get_price_from_site(self):
        bs = self._scraping_init()
        price_int = self.get_price_from_soup(bs)
        return price_int

    def get_name_and_price(self):
        bs = self._scraping_init()
        price_int = self.get_price_from_soup(bs)
        self.get_name_from_soup(bs)
        return {'name': self.product.name, 'price': price_int}
        
    def _scraping_init(self):
        scrapping = Scrapping(self.product.url)
        return scrapping.get_soup()

class MultipleProductsManager:
    def __init__(self, products_list: List) -> None:
        self.products_list = products_list

    def check_for_price_updates(self):
        for product in self.products_list:
            print(f'Product {product.name}, prices {[p.price for p in product.prices]}')
            product_handler = ProductOperations(product=product)
            product_handler.update_price_from_site()
