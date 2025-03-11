from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Publisher, Book, Stock, Sale, Shop  # Импортируем модели
from sqlalchemy import or_

# Подключение к базе данных PostgreSQL
DATABASE_URI = "postgresql+psycopg2://test123:test1234@host:5432/bookstore"
engine = create_engine(DATABASE_URI)

# Создаем сессию
Session = sessionmaker(bind=engine)
session = Session()

# Запрашиваем имя или идентификатор издателя
publisher_input = input("Введите имя или идентификатор издателя: ")

# Определяем, является ли ввод числом (ID) или строкой (имя)
try:
    publisher_id = int(publisher_input)
    publisher_filter = Publisher.id == publisher_id
except ValueError:
    publisher_filter = Publisher.name.ilike(f"%{publisher_input}%")

# Запрос для выборки данных
results = (
    session.query(Book.title, Shop.name, Sale.price, Sale.date_sale)
    .join(Publisher, Publisher.id == Book.id_publisher)
    .join(Stock, Stock.id_book == Book.id)
    .join(Shop, Shop.id == Stock.id_shop)
    .join(Sale, Sale.id_stock == Stock.id)
    .filter(publisher_filter)
    .all()
)

# Вывод результатов
if results:
    for title, shop_name, price, date_sale in results:
        print(f"{title} | {shop_name} | {price} | {date_sale.strftime('%d-%m-%Y')}")
else:
    print("Данные о продажах для указанного издателя не найдены.")

# Закрываем сессию
session.close()
