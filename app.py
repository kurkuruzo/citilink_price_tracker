from datetime import datetime
from models.product import Product
from requests.exceptions import MissingSchema
from services import general
from services.price import PriceHandler
from services.product import ProductOperations, MultipleProductsManager
from sqlalchemy.exc import IntegrityError
from database import session, Base, engine

Base.metadata.create_all(engine)

# ssd = Product(url='https://www.citilink.ru/product/ssd-nakopitel-crucial-bx500-ct480bx500ssd1-480gb-2-5-sata-iii-1084930')
# print(ssd)
# ssd.get_name_and_price()
# session.add(ssd)
# session.commit()
# print(ssd.id)

def menu():
    while True:
        option = input(
            """Выберите действие:
            1 - Добавить товар для отслеживания
            2 - Показать все товары
            3 - Обновить цены
            q - Выход
            """
        )
        products_list = ProductOperations.get_all_products()

        if option == 'q':
            break
        elif option == '1':
            url = input("Введите url товара для отлсеживания\n")
            try:
                product = Product(url=url, update_date=datetime.now())
                session.add(product)
                session.flush()
            except IntegrityError as e:
                session.rollback()
                print(e.args)
            else:
                product_handler = ProductOperations(product)
                try:
                    product_handler.get_name_and_price()
                except MissingSchema as e:
                    print(f'Неправильный формат URL. {e.args}') 
                    continue
                else:
                    session.commit()


        elif option == '2':
            [print(product, sep="\n") for product in products_list]
        elif option == '3':
            products_list_manager = MultipleProductsManager(products_list)
            products_list_manager.check_for_price_updates()
        else:
            print("Вы ввели неправильный символ")

if __name__ == "__main__":
    menu()