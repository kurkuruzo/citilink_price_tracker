import logging
from database import session
from typing import List
from models.product import Product
from services.general import Scraping
from services.price import PriceHandler

logger = logging.getLogger('app')
class ProductOperations:
    """Class to operate with Product instances
    """
    def __init__(self, product: Product) -> None:
        self.product = product
        logger.debug(f'Product handler initialized for product id {self.product.id}')

    @staticmethod
    def get_all_products() -> List[Product]:
        """Gets a list of all products in database and returns as a list

        Returns:
            List[Product]: List of Product instances
        """
        products = session.query(Product).all()
        return products

    def update_price_from_site(self) -> None:
        """Updates the price for the product, basing on the current price on site
        """
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
        """Gets a price from site

        Returns:
            int: Integer representation of the price from site
        """
        price_int = Scraping(self.product.url).get_price_from_soup()
        return price_int

    def get_name_and_price(self) -> dict:
        """Gets a name and price for the product from site. Mainly used for creation of a new Product

        Returns:
            dict: Dictionary, containing name and price
        """
        scrap = Scraping(self.product.url)
        price_int = scrap.get_price_from_soup()
        self.product.name = scrap.get_name_from_soup()
        return {'name': self.product.name, 'price': price_int}
        
    # def get_attributes_from_site(self, **kwargs) -> None:
    #     scrap = Scraping(self.product.url)
    #     if kwargs['name']:
    #         name = scrap.get_name_from_soup()
    #     if kwargs['price']:
    #         price = scrap.get_price_from_soup()
    #     else:
    #         raise NotImplementedError
    
class MultipleProductsManager:
    """Class to manage multiple products at once
    """
    def __init__(self, products_list: List) -> None:
        self.products_list = products_list

    def check_for_price_updates(self):
        """Checks for price updates on site for the list of products
        """
        for product in self.products_list:
            logger.info(f'Product {product.name}, prices {[p.price for p in product.prices]}')
            product_handler = ProductOperations(product=product)
            product_handler.update_price_from_site()
