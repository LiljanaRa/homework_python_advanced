from sqlalchemy import (
    create_engine,
    BigInteger,
    String,
    Numeric,
    Boolean,
    ForeignKey)
from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
    Mapped,
    mapped_column,
    relationship
)
from decimal import Decimal


engine = create_engine(
    url="sqlite:///:memory:",
    echo=True,
    echo_pool=True
)

session_fabric = sessionmaker(bind=engine)
session = session_fabric()

Base = declarative_base()

class Product(Base):
    __tablename__ = 'product'
    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True
    )
    name: Mapped[str] = mapped_column(
        String(100)
    )
    price: Mapped[Decimal] = mapped_column(
        Numeric(10,2)
    )
    in_stock: Mapped[bool] = mapped_column(
        Boolean, default=True
    )
    category_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey('category.id')
    )

    category: Mapped['Category'] = relationship(
        'Category',
        back_populates='products'
    )

class Category(Base):
    __tablename__ = 'category'
    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True
    )
    name: Mapped[str] = mapped_column(
        String(100)
    )
    description: Mapped[str] = mapped_column(
        String(255)
    )

    products: Mapped['Product'] = relationship(
        'Product',
        back_populates='category'
    )

Base.metadata.create_all(bind=engine)