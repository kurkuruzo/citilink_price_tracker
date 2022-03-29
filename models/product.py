from datetime import date, datetime
from fileinput import filename
from typing import List
from bs4 import BeautifulSoup
from database import Base
from database import session
from datetime import datetime
import requests
import os
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship
from models.price import Price


class Product(Base):
    # def __init__(self, url: str,  name: str = None, price: int = None, date: datetime = None) -> None:
    #     self.url = url
    #     self.name = name
    #     self.price = price
    #     self.date = date

    __tablename__ = 'products'
    id = Column(Integer(), primary_key=True)
    url = Column(String(length=1000))
    name = Column(String(length=512))
    price = relationship("Price")
    update_date = Column(DateTime)

    def _get_soup(self):
        page = requests.get(self.url).text
        bs = BeautifulSoup(page, 'html.parser')
        return bs

    def __str__(self) -> str:
        return f'<Product {self.name if self.name else "Имя не определено"}: цена {self.price if self.price else "Цена не определена"}, сохранена {self.date.isoformat() if self.date else "Дата не сохранена"}>'
                
    def get_name_and_price(self):
        bs = self._get_soup()
        price_element = bs.find(class_="ProductHeader__price-default_current-price")
        self.price = int(price_element.string.replace(" ", ""))
        name_element = bs.find(class_='ProductHeader__title')
        self.name = name_element.string.strip()
        self.date = datetime.now()
        return {'name': self.name, 'price': self.price}

class ProductOperations:
    @staticmethod
    def get_all_products() -> List:
        products = session.query(Product).all()
        return products


    @classmethod
    def update_price(cls):
        for product in cls.get_all_products():
            new_price = Product.get_name_and_price(product)['price']
            

class FileOperations:
    def save_to_file(filename, obj):
        with open(filename, 'w') as f:
            f.write(obj.__dict__)