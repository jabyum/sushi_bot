from sqlalchemy import (Column, Integer,
                        String, ForeignKey, Float, DateTime, Boolean)
from sqlalchemy.orm import relationship, backref
from database import Base
class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(Integer, unique=True)
    user_name = Column(String)
    phone_number = Column(String, unique=True)
    language = Column(String, default="ru")
    reg_date = Column(DateTime)
class Category(Base):
    __tablename__ = "category"
    cat_id = Column(Integer, primary_key=True, autoincrement=True)
    cat_name = Column(String, unique=True)
    cat_name_uz = Column(String, unique=True)
    reg_date = Column(DateTime)
class Product(Base):
    __tablename__ = "product"
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String, unique=True)
    product_name_uz = Column(String, unique=True)
    product_price = Column(Integer)
    product_description = Column(String, nullable=True)
    product_description_uz = Column(String, nullable=True)
    product_photo = Column(Integer, nullable=True)
    product_cat = Column(String)
    reg_date = Column(DateTime)

class Cart(Base):
    __tablename__ = "cart"
    cart_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    product_name = Column(String)
    product_count = Column(Integer)
    total_price = Column(Integer)
    reg_date = Column(DateTime)
    user_fk = relationship(User, lazy="subquery")

class Admin(Base):
    __tablename__ = "admin"
    admin_id = Column(Integer, primary_key=True, autoincrement=True)
    admin_tg_id = Column(Integer, unique=True)
    admin_name = Column(String)
    admin_reg_date = Column(DateTime)



