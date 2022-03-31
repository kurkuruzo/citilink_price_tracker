import argparse
from datetime import datetime
from json.tool import main
import logging
from typing import List
from models.product import Product
from requests.exceptions import MissingSchema
from services import general
from services.price import PriceHandler
from services.product import ProductOperations, MultipleProductsManager
from sqlalchemy.exc import IntegrityError
from database import session, Base, engine

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%d-%m %H:%M',
                    filename='app.log',
                    filemode='w')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
console_format = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
console.setFormatter(console_format)
logger = logging.getLogger('app')
logger.addHandler(console)

logger.info('Программа запущена')
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
    parser.add_argument(
        "-u", "--update",
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
            logger.info(e.args)
        else:
            product_handler = ProductOperations(product)
            try:
                price = product_handler.get_name_and_price()['price']
            except MissingSchema as e:
                logger.info(f'Неправильный формат URL. {e.args}') 
                return
            else:
                price_handler = PriceHandler(product=product)
                price_handler.append_new_price(price)
                session.commit()


def update_products():
    products_list = ProductOperations.get_all_products()
    products_list_manager = MultipleProductsManager(products_list)
    products_list_manager.check_for_price_updates()
    session.commit()


def print_all_products():
    products_list = ProductOperations.get_all_products()
    [print(product, sep="\n") for product in products_list]


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
        if option == 'q':
            break
        elif option == '1':
            url = input("Введите url товара для отлсеживания\n")
            add_product(urls=[url])
        elif option == '2':
            print_all_products()
        elif option == '3':
            update_products()
        else:
            print("Вы ввели неправильный символ")
    logger.info('Завершение работы...')


def main():
    parser = init_argparse()
    args = parser.parse_args()
    # if args.menu:
    #     menu()
    if args.update:
        update_products()
        return
    if args.urls:
        add_product(args.urls)
        return
    else:
        menu()

if __name__ == "__main__":
    main()