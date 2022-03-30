from bs4 import BeautifulSoup
import requests
from typing import List



class Scrapping:
    def __init__(self, url) -> None:
        self.url = url

    def get_soup(self):
        page = requests.get(self.url).text
        bs = BeautifulSoup(page, 'html.parser')
        return bs

