from datetime import datetime
import logging
from database import session
from models.price import Price
from models.product import Product

logger = logging.getLogger('app')


class PriceHandler:
    """Class to operate with Price instances
    """

    def __init__(self, product: Product) -> None:
        self.product = product
        logger.debug(
            f'Price handler initialized for product id {self.product.id}')

    def append_new_price(self, new_price: int) -> Price:
        """Function adds new price to the database with relation to the product id

        Args:
            new_price (int): New price that should be recorded

        Returns:
            Price: Price object
        """
        new_price_obj = Price(
            price=new_price, product_id=self.product.id, date=datetime.now())
        session.add(new_price_obj)
        session.flush()
        return new_price_obj
