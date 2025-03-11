from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Создаем базовый класс для моделей
Base = declarative_base()


# Модель для таблицы Publisher
class Publisher(Base):
    __tablename__ = "publisher"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # Связь с таблицей Book
    books = relationship("Book", back_populates="publisher")


# Модель для таблицы Book
class Book(Base):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    id_publisher = Column(Integer, ForeignKey("publisher.id"), nullable=False)

    # Связь с таблицей Publisher
    publisher = relationship("Publisher", back_populates="books")
    # Связь с таблицей Stock
    stocks = relationship("Stock", back_populates="book")


# Модель для таблицы Stock
class Stock(Base):
    __tablename__ = "stock"
    id = Column(Integer, primary_key=True)
    id_book = Column(Integer, ForeignKey("book.id"), nullable=False)
    id_shop = Column(Integer, ForeignKey("shop.id"), nullable=False)
    count = Column(Integer, nullable=False)

    # Связь с таблицей Book
    book = relationship("Book", back_populates="stocks")
    # Связь с таблицей Shop
    shop = relationship("Shop", back_populates="stocks")
    # Связь с таблицей Sale
    sales = relationship("Sale", back_populates="stock")


# Модель для таблицы Sale
class Sale(Base):
    __tablename__ = "sale"
    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    date_sale = Column(Date, nullable=False)
    id_stock = Column(Integer, ForeignKey("stock.id"), nullable=False)
    count = Column(Integer, nullable=False)

    # Связь с таблицей Stock
    stock = relationship("Stock", back_populates="sales")


# Модель для таблицы Shop
class Shop(Base):
    __tablename__ = "shop"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # Связь с таблицей Stock
    stocks = relationship("Stock", back_populates="shop")


# Создаем подключение к базе данных (SQLite в данном примере)
engine = create_engine("sqlite:///bookstore.db")

# Создаем таблицы в базе данных
Base.metadata.create_all(engine)

# Создаем сессию для работы с базой данных
Session = sessionmaker(bind=engine)
session = Session()
