from bs4 import BeautifulSoup
import requests
from typing import List

class Scraping:
    def __init__(self, url) -> None:
        self.url = url
        self.bs = self.get_soup()

    def get_soup(self):
        page = requests.get(self.url).text
        bs = BeautifulSoup(page, 'html.parser')
        return bs

    def get_price_from_soup(self) -> int:
        price_element = self.bs.find(class_="ProductHeader__price-default_current-price")
        price_int = int(price_element.string.replace(" ", ""))
        return price_int
    
    def get_name_from_soup(self) -> str:
        name_element = self.bs.find(class_='ProductHeader__title')
        name = name_element.string.strip()
        return name