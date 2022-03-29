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

class Price(Base):

    __tablename__ = 'prices'
    id = Column(Integer, primary_key=True)
    price = Column(Integer)
    date = Column(DateTime)
    product_id = Column(Integer, ForeignKey('products.id'))
    # product = relationship("Product", back_populates="prices")