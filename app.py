import argparse
from datetime import datetime
from json.tool import main
from typing import List
from models.product import Product
from requests.exceptions import MissingSchema
from services import general
from services.price import PriceHandler
from services.product import ProductOperations, MultipleProductsManager
from sqlalchemy.exc import IntegrityError
from database import session, Base, engine

Base.metadata.create_all(engine)

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [URL]...",
        description="Проверка изменения цены на товары в магазине citilink.ru"
    )
    parser.add_argument(
        "-m", "--menu",
        action='store_true'
    )
    parser.add_argument('urls', nargs='*')
    return parser


def add_product(urls: List):
    for url in urls:
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
                price = product_handler.get_name_and_price()['price']
            except MissingSchema as e:
                print(f'Неправильный формат URL. {e.args}') 
                return
            else:
                price_handler = PriceHandler(product=product)
                price_handler.append_new_price(price)
                session.commit()

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
            add_product(urls=[url])
        elif option == '2':
            [print(product, sep="\n") for product in products_list]
        elif option == '3':
            products_list_manager = MultipleProductsManager(products_list)
            products_list_manager.check_for_price_updates()
            session.commit()
        else:
            print("Вы ввели неправильный символ")


def main():
    parser = init_argparse()
    args = parser.parse_args()
    print(args)
    # if args.menu:
    #     menu()
    if args.urls:
        add_product(args.urls)
    else:
        menu()

if __name__ == "__main__":
    main()