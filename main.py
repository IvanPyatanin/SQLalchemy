import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker



Base = declarative_base()

class Publisher(Base):
    __tablename__ = "Publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

    def __str__(self):
        return f'{self.id}| {self.name}'

class Book(Base):
    __tablename__ = "Book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=100))
    publisher_id = sq.Column(sq.Integer, sq.ForeignKey("Publisher.id"), nullable=False)

    publisher = relationship(Publisher, backref="Book")

    def __str__(self):
        return f'{self.id}| {self.title}| {self.publisher.name}'

class Shop(Base):
    __tablename__ = "Shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

    def __str__(self):
        return f'{self.id}: {self.name}'

class Stock(Base):
    __tablename__ = "Stock"

    id = sq.Column(sq.Integer, primary_key=True)
    book_id = sq.Column(sq.Integer, sq.ForeignKey("Book.id"), nullable=False)
    shop_id = sq.Column(sq.Integer, sq.ForeignKey("Shop.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    book = relationship(Book, backref="Stock")
    shop = relationship(Shop, backref="Stock")

    def __str__(self):
        return f'{self.id}| {self.book.title}| {self.shop.name}| {self.count}'

class Sale(Base):
    __tablename__ = "Sale"

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Integer, nullable=False)
    data_sale = sq.Column(sq.String,nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    stock_id = sq.Column(sq.Integer, sq.ForeignKey("Stock.id"), nullable=False)

    stock = relationship(Stock, backref="Sale")

    def __str__(self):
        return f'{self.id}| {self.price}| {self.data_sale}| {self.count}| {self.stock.book.title}'

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

DNS = 'postgresql://postgres:158660@localhost:5432/sqlalchemy'
engine = sqlalchemy.create_engine(DNS)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

#Добавление данных

Publisher_1 = Publisher(name='Пушкин')
Publisher_2 = Publisher(name='Глуховский')

Book_1 = Book(title='Капитанская дочка', publisher=Publisher_1)
Book_2 = Book(title='Руслан и Людмила', publisher=Publisher_1)
Book_3 = Book(title='Евгений Онегин', publisher=Publisher_1)
Book_4 = Book(title='метро 2033', publisher=Publisher_2)
Book_5 = Book(title='метро 2034', publisher=Publisher_2)
Book_6 = Book(title='метро 2035', publisher=Publisher_2)

Shop_1 = Shop(name='Буквоед')
Shop_2 = Shop(name='Лабиринт')
Shop_3 = Shop(name='Книжный дом')

Stock_1 = Stock(count=1, book=Book_1, shop=Shop_1)
Stock_2 = Stock(book=Book_2, shop=Shop_1, count=1)
Stock_3 = Stock(book=Book_3, shop=Shop_2, count=1)
Stock_4 = Stock(book=Book_4, shop=Shop_2, count=1)
Stock_5 = Stock(book=Book_5, shop=Shop_3, count=1)
Stock_6 = Stock(book=Book_6, shop=Shop_3, count=1)
Stock_7 = Stock(book=Book_1, shop=Shop_3, count=1)

Sale_1 = Sale(price=100, data_sale='29-01-2022', count=1, stock=Stock_1)
Sale_2 = Sale(price=200, data_sale='12-06-2021', count=1, stock=Stock_2)
Sale_3 = Sale(price=1000, data_sale='09-01-2023', count=1, stock=Stock_3)
Sale_4 = Sale(price=500, data_sale='30-10-2010', count=1, stock=Stock_4)
Sale_5 = Sale(price=750, data_sale='05-10-2000', count=1, stock=Stock_5)
Sale_6 = Sale(price=150, data_sale='29-12-2002', count=1, stock=Stock_6)
Sale_7 = Sale(price=1500, data_sale='29-04-2020', count=1, stock=Stock_7)
Sale_8 = Sale(price=1010, data_sale='29-03-2022', count=1, stock=Stock_1)
Sale_9 = Sale(price=1111, data_sale='01-01-2022', count=1, stock=Stock_2)
Sale_10 = Sale(price=1055, data_sale='07-11-2022', count=1, stock=Stock_3)
Sale_11 = Sale(price=1001, data_sale='16-05-2020', count=1, stock=Stock_4)


session.add_all([Publisher_1, Publisher_2])
session.add_all([Book_1, Book_2, Book_3, Book_4, Book_5, Book_6])
session.add_all([Shop_1, Shop_2, Shop_3])
session.add_all([Stock_1, Stock_2, Stock_3, Stock_4, Stock_5, Stock_6, Stock_7])
session.add_all([Sale_1, Sale_2, Sale_3, Sale_4, Sale_5, Sale_6, Sale_7, Sale_8, Sale_9, Sale_10, Sale_11])
session.commit()


def get_shop(names):
    q = session.query(Book.title, Shop.name, Sale.price, Sale.data_sale).select_from(Shop).\
        join(Stock, Shop.id == Stock.shop_id).\
        join(Book, Book.id == Stock.book_id).\
        join(Publisher, Publisher.id == Book.publisher_id).\
        join(Sale, Stock.id == Sale.stock_id)

    if names.isdigit():
        res = q.filter(Publisher.id == f'{names}').all()
    else:
        res = q.filter(Publisher.name.like(f'{names}')).all()
    for name, shop, sale, data in res:
        print(f"{name: <20} | {shop: <10} | {sale: <5} | {data}")



if __name__ == '__main__':
    names = input('Введите фамилию или id: ')
    get_shop(names)

session.close()