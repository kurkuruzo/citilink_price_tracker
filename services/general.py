from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import requests


class PriceNotFoundError(Exception):
    pass


class Scraping:
    """Class for the scraping methods
    """

    def __init__(self, url: str) -> None:
        """

        Args:
            url (str): URL to scrap
        """
        self.url = url
        self.bs = self.get_soup()

    def get_soup(self) -> BeautifulSoup:
        """Gets a page from site and returns a BeautifulSoup object for it

        Returns:
            BeautifulSoup: BeautifulSoup object for the page
        """
        page = requests.get(self.url).text
        bs = BeautifulSoup(page, 'html.parser')
        return bs

    def get_price_from_soup(self) -> int:
        """Parces a price from the page

        Returns:
            int: Price of the product on the page
        """
        price_element = self.bs.find(
            class_="ProductHeader__price-default_current-price")
        if not price_element:
            raise PriceNotFoundError('Цена не найдена')
        price_int = int(price_element.string.replace(" ", ""))
        return price_int

    def get_name_from_soup(self) -> str:
        """Parces a name of a product from the page

        Returns:
            str: Name of the product on the page
        """
        name_element = self.bs.find(class_='ProductHeader__title')
        name = name_element.string.strip()
        return name


class Printer(ABC):
    @abstractmethod
    def print():
        pass


class ConsolePrinter(Printer):
    def __init__(self, object) -> None:
        super().__init__()
        self.object = object

    def print(self):
        print(self.object)
