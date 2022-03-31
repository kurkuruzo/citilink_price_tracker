from database import Base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship

class Price(Base):

    __tablename__ = 'price'
    id = Column(Integer, primary_key=True)
    price = Column(Integer)
    date = Column(DateTime)
    product_id = Column(Integer, ForeignKey('product.id'))
    product = relationship("Product", back_populates="prices")
