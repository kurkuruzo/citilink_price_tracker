from models.product import Product, ProductOperations
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
            q - Выход
            """
        )
        if option == 'q':
            break
        elif option == '1':
            url = input("Введите url товара для отлсеживания")
            product = Product(url=url)
            product.get_name_and_price()
            session.add(product)
            try:
                session.commit()
            except Exception as e:
                session.rollback()
                print(f'Произошла ошибка: {e.args}')
        elif option == '2':
            [print(product, sep="\n") for product in ProductOperations.get_all_products()]
        else:
            print("Вы ввели неправильный символ")

if __name__ == "__main__":
    menu()