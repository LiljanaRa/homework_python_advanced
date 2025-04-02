from sqlalchemy import (
    create_engine,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Numeric,
    Identity,
    func, Boolean
)
from sqlalchemy.orm import sessionmaker, relationship, Mapped, mapped_column, declarative_base
from sqlalchemy.exc import IntegrityError, DataError

from datetime import datetime


Base = declarative_base()
engine = create_engine('sqlite:///:memory:')


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(always=True),
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(25))
    age: Mapped[int] = mapped_column(Integer)

    orders: Mapped['Order'] = relationship("Order", back_populates="user")


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(always=True),
        primary_key=True,
        autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    amount: Mapped[float] = mapped_column(Numeric(6, 2))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    user: Mapped['User'] = relationship("User", back_populates="orders")


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(always=True),
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(75))
    description: Mapped[str] = mapped_column(String(255))

    products: Mapped[list['Product']] = relationship("Product", back_populates="category" )


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(always=True),
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(75))
    price: Mapped[float] = mapped_column(Numeric(10, 2))
    in_stock: Mapped[bool] = mapped_column(Boolean, default=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))

    category: Mapped['Category'] = relationship("Category", back_populates="products")

Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()

# Задача 1: Наполнение данными

def create_new_category(session: Session, data: dict[str, str|int]) -> Category:
    try:
        category = Category(**data)
        session.add(category)
        session.commit()
        session.refresh(category)
        session.close()

        return category
    except (IntegrityError, DataError) as err:
        session.rollback()
        raise err

def create_new_product(session: Session, data: dict[str, str|int]) -> Product:
    try:
        product = Product(**data)
        session.add(product)
        session.commit()
        session.refresh(product)
        session.close()

        return product
    except (IntegrityError, DataError) as err:
        session.rollback()
        raise err


category_1_data = {
    "id": 1,
    "name": "Electronics",
    "description": "Gadgets and Devices."
    }
category_1 = create_new_category(session=session, data=category_1_data)

category_2_data = {
    "id": 2,
    "name": "Books",
    "description": "Print and electronic books."
    }
category_2 = create_new_category(session=session, data=category_2_data)

category_3_data = {
    "id": 3,
    "name": "Clothes",
    "description": "Clothes for men and women."
    }
category_3 = create_new_category(session=session, data=category_3_data)


product_1_data = {
    "id": 1,
    "price": 299.99,
    "name": "Smartphone",
    "in_stock": True,
    "category_id": 1
    }
product_1 = create_new_product(session=session, data=product_1_data)

product_2_data = {
    "id": 2,
    "price": 499.99,
    "name": "Laptop",
    "in_stock": True,
    "category_id": 1
    }
product_2 = create_new_product(session=session, data=product_2_data)

product_3_data = {
    "id": 3,
    "price": 15.99,
    "name": "Science fiction novel",
    "in_stock": True,
    "category_id": 2
    }
product_3 = create_new_product(session=session, data=product_3_data)

product_4_data = {
    "id": 4,
    "price": 40.50,
    "name": "Jeans",
    "in_stock": True,
    "category_id": 3
    }
product_4 = create_new_product(session=session, data=product_4_data)

product_5_data = {
    "id": 5,
    "price": 20.00,
    "name": "T-shirt",
    "in_stock": True,
    "category_id": 3
    }
product_5 = create_new_product(session=session, data=product_5_data)


# Задача 2: Чтение данных
# Извлеките все записи из таблицы categories.
# Для каждой категории извлеките и выведите все связанные с ней продукты, включая их названия и цены.


all_categories = session.query(Category).all()

for cat in all_categories:
    print(cat.id, cat.name, cat.description)


products_to_categories = session.query(
    Product.id,
    Product.name,
    Product.price,
    Product.category_id,
    Category.name.label("category_name")
).join(Category).filter(Product.category_id == 1).all()

for prod in products_to_categories:
    print(prod.category_id, prod.category_name, prod.id,
          prod.name, prod.price)


products_to_categories = session.query(
    Product.id,
    Product.name,
    Product.price,
    Product.category_id,
    Category.name.label("category_name")
).join(Category).filter(Product.category_id == 2).all()

for prod in products_to_categories:
    print(prod.category_id, prod.category_name, prod.id,
          prod.name, prod.price)

products_to_categories = session.query(
    Product.id,
    Product.name,
    Product.price,
    Product.category_id,
    Category.name.label("category_name")
).join(Category).filter(Product.category_id == 3).all()

for prod in products_to_categories:
    print(prod.category_id, prod.category_name, prod.id,
          prod.name, prod.price)

# Задача 3: Обновление данных
# Найдите в таблице products первый продукт с названием "Смартфон".
# Замените цену этого продукта на 349.99.

first_smartphone = session.query(
    Product
).filter(Product.name == "Smartphone").first()

if first_smartphone:
    first_smartphone.price = 349.99
    session.commit()
    print(first_smartphone.name, first_smartphone.price)

# Задача 4: Агрегация и группировка
# Используя агрегирующие функции и группировку, подсчитайте общее
# количество продуктов в каждой категории.

count_products_to_categories = session.query(
    Product.category_id,
    Category.name.label("category_name"),
    func.count(Product.id).label("count")
    ).join(Category
    ).group_by(Product.category_id
    ).all()


for count_cat in count_products_to_categories:
    print(count_cat.category_id, count_cat.category_name, count_cat.count)

# Задача 5: Группировка с фильтрацией
# Отфильтруйте и выведите только те категории, в которых более одного продукта.

count_products_to_categories_gt_1 = session.query(
    Product.category_id,
    Category.name.label("category_name"),
    func.count(Product.id).label("count")
    ).join(Category
    ).group_by(Product.category_id
    ).having(func.count(Product.id) > 1
    ).all()

for count_cat in count_products_to_categories_gt_1:
    print(count_cat.category_id, count_cat.category_name, count_cat.count)