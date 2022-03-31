from database import Base
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship

class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer(), primary_key=True)
    url = Column(String(length=1000), unique=True)
    name = Column(String(length=512))
    prices = relationship("Price", back_populates="product")
    update_date = Column(DateTime)

    def __str__(self) -> str:
        return f'<Product {self.name if self.name else "Имя не определено"}: цены {[pr.price for pr in self.prices] if self.prices else "Цены не определены"}, сохранена {self.update_date.isoformat() if self.update_date else "Дата не сохранена"}>'


class FileOperations:
    def __init__(self, filename) -> None:
        self.filename = filename

    def save_to_file(self, obj):
        with open(self.filename, 'w') as f:
            f.write(obj.__dict__)