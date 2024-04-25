from database.models import Category, Product, Cart
from database import get_db
from datetime import datetime

def register_category(cat_name, cat_name_uz):
    db = next(get_db())
    try:
        new_cat = Category(cat_name=cat_name, cat_name_uz=cat_name_uz, reg_date=datetime.now())
        db.add(new_cat)
        db.commit()
        return "Категория успешно добавлена"
    except:
        return "Категория уже существует"
def change_cat_ru(cat_name, new_cat_name):
    db = next(get_db())
    try:
        exact_cat = db.query(Category).filter_by(cat_name).first()
        exact_cat.cat_name = new_cat_name
        db.commit()
        return "Успешно изменено"
    except:
        return "Такой категории нет"
def change_cat_uz(cat_name_uz, new_cat_name):
    db = next(get_db())
    try:
        exact_cat = db.query(Category).filter_by(cat_name_uz).first()
        exact_cat.cat_name_uz = new_cat_name
        db.commit()
        return "Успешно изменено"
    except:
        return "Такой категории нет"
def delete_cat(cat_name):
    db = next(get_db())
    try:
        exact_cat = db.query(Category).filter_by(cat_name).first()
        db.delete(exact_cat)
        db.commit()
        return "Категория удалена"
    except:
        return "Категория не найдена"
def register_product(product_name, product_name_uz, product_price, product_description,
                     product_description_uz, product_photo, product_cat):
    db = next(get_db())
    try:
        new_product = Product(product_name=product_name, product_name_uz=product_name_uz, product_price=product_price,
                              product_description=product_description, product_description_uz=product_description_uz,
                              product_photo=product_photo, product_cat=product_cat, reg_date=datetime.now())
        db.add(new_product)
        db.commit()
        return "Продукт успешно добавлен"
    except:
        return "Продукт уже существует"
def change_product_info(product_id, column, new_info):
    db = next(get_db())
    product = db.query(Product).filter_by(product_id=product_id).first()
    try:
        if column.lower() == "product_name":
            product.product_name = new_info
        elif column.lower() == "product_name_uz":
            product.product_name_uz = new_info
        elif column.lower() == "product_price":
            product.product_price = new_info
        elif column.lower() == "product_description":
            product.product_description = new_info
        elif column.lower() == "product_description_uz":
            product.product_description_uz = new_info
        elif column.lower() == "product_photo":
            product.product_photo = new_info
        elif column.lower() == "product_cat":
            product.product_cat = new_info
        db.commit()
        return "Информация успешно изменена"
    except:
        return "Не получилось изменить"
def delete_product(product_name):
    db = next(get_db())
    try:
        product = db.query(Product).filter_by(product_name=product_name).first()
        db.delete(product)
        db.commit()
        return "Продукт успешно удален"
    except:
        return "Продукт не найден"
def get_cats():
    db = next(get_db())
    try:
        cats = db.query(Category).all()
        all_cats = [(cat.cat_id, cat.cat_name) for cat in cats]
        return all_cats
    except:
        return []
def get_cats_uz():
    db = next(get_db())
    try:
        cats = db.query(Category).all()
        all_cats = [(cat.cat_id, cat.cat_name_uz, cat.cat_name) for cat in cats]
        return all_cats
    except:
        return []
def get_all_cats_name():
    db = next(get_db())
    try:
        cats = db.query(Category).all()
        all_cats = [cat.cat_name for cat in cats]
        return all_cats
    except:
        return []
def get_all_cats_name_uz():
    db = next(get_db())
    try:
        cats = db.query(Category).all()
        all_cats = [cat.cat_name_uz for cat in cats]
        return all_cats
    except:
        return []
def get_products_by_cat(cat):
    db = next(get_db())
    try:
        products = db.query(Product).filter_by(product_cat=cat).all()
        all_products = [product.product_name for product in products]
        return all_products
    except:
        return []
def get_products_by_cat_uz(cat):
    db = next(get_db())
    try:
        products = db.query(Product).filter_by(product_cat=cat).all()
        all_products = [product.product_name_uz for product in products]
        return all_products
    except:
        return []
def get_all_products_name():
    db = next(get_db())
    try:
        products = db.query(Product).all()
        all_products = [product.product_name for product in products]
        return all_products
    except:
        return []
def get_all_products_name_uz():
    db = next(get_db())
    try:
        products = db.query(Product).all()
        all_products = [product.product_name_uz for product in products]
        return all_products
    except:
        return []
def get_product(product_name):
    db = next(get_db())
    try:
        product = db.query(Product).filter_by(product_name=product_name).first()
        return [product.product_name, product.product_price,
                product.product_description, product.product_photo]
    except:
        return []
def get_product_uz(product_name_uz):
    db = next(get_db())
    try:
        product = db.query(Product).filter_by(product_name_uz=product_name_uz).first()
        return [product.product_name_uz, product.product_price,
                product.product_description_uz, product.product_photo]
    except:
        return []
def get_user_cart(user_id):
    db = next(get_db())
    try:
        cart = db.query(Cart).filter_by(user_id=user_id).all()
        user_cart = [(exact.product_name, exact.product_count, exact.total_price) for exact in cart]
        return user_cart
    except:
        return []
def get_user_cart_id_name(user_id):
    db = next(get_db())
    try:
        cart = db.query(Cart).filter_by(user_id=user_id).all()
        user_cart = [(exact.product_name, exact.cart_id) for exact in cart]
        return user_cart
    except:
        return []
def add_to_cart(user_id, product_name, product_count, product_price):
    db = next(get_db())
    try:
        total_price = product_count * product_price
        new_cart = Cart(user_id=user_id, product_name=product_name,
                        product_count=product_count, total_price=total_price)
        db.add(new_cart)
        db.commit()
    except:
        pass

def delete_user_cart(user_id):
    db = next(get_db())
    exact_cat = db.query(Cart).filter_by(user_id=user_id).all()
    try:
        for items in exact_cat:
            db.delete(items)
        db.commit()
    except:
        pass
def user_cart_ids(user_id):
    db = next(get_db())
    exact_carts = db.query(Cart).filter_by(user_id=user_id).all()
    try:
        actual_ids = [exact.cart_id for exact in exact_carts]
        return actual_ids
    except:
        pass

def delete_exact_product_from_cart(cart_id):
    db = next(get_db())
    try:
        product = db.query(Cart).filter_by(cart_id=cart_id).first()
        db.delete(product)
        db.commit()
    except:
        pass