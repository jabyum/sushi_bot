from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

def main_menu_ru():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    menu = KeyboardButton("🍽Меню")
    information = KeyboardButton("ℹ️Информация")
    feedback = KeyboardButton("✍️Оставить отзыв")
    settings = KeyboardButton("⚙️Настрйоки")
    cart = KeyboardButton("🛒Корзина")
    uzb = KeyboardButton("🇺🇿O'zbek tili")
    kb.row(menu, information)
    kb.row(feedback, settings)
    kb.row(cart, uzb)
    return kb
def phone_kb_ru():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    phone_number = KeyboardButton("Отправить номер", request_contact=True)
    kb.add(phone_number)
    return kb
def location_kb_ru():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    location = KeyboardButton("Отправить локацию", request_location=True)
    otmena = KeyboardButton("❌Отмена")
    kb.add(location)
    kb.row(otmena)
    return kb
def categories_ru(cats):
    kb = InlineKeyboardMarkup(row_width=2)
    back = InlineKeyboardButton(text="🔙Назад", callback_data="main_menu")
    all_menu = InlineKeyboardButton(text="Всё меню", url="https://telegra.ph/Menyu-12-07-22")
    all_cats = [InlineKeyboardButton(text=i[1], callback_data=i[1]) for i in cats]
    kb.add(all_menu, *all_cats, back)
    return kb
def products_ru(cats):
    kb = InlineKeyboardMarkup(row_width=2)
    back = InlineKeyboardButton(text="🔙Назад", callback_data="back")
    all_products = [InlineKeyboardButton(text=i, callback_data=i) for i in cats]
    kb.add(*all_products, back)
    return kb
def exact_product_ru(current_ammount=1, plus_or_minus=""):
    kb = InlineKeyboardMarkup(row_width=3)
    back = InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")
    accept =  InlineKeyboardButton(text="Добавить в корзигу", callback_data="to_cart")
    minus = InlineKeyboardButton(text="➖", callback_data="minus")
    plus = InlineKeyboardButton(text="➕", callback_data="plus")
    count = InlineKeyboardButton(text=f"{current_ammount}", callback_data="none")
    if plus_or_minus == "plus":
        new_ammount = current_ammount + 1
        count = InlineKeyboardButton(text=f"{new_ammount}", callback_data="none")
    elif plus_or_minus == "minus":
        if current_ammount > 1:
            new_ammount = current_ammount - 1
            count = InlineKeyboardButton(text=f"{new_ammount}", callback_data="none")
    kb.add(minus, count, plus)
    kb.row(accept)
    kb.row(back)
    return kb
def get_cart_kb_ru(cart):
    kb = InlineKeyboardMarkup(row_width=1)
    clear = InlineKeyboardButton(text="Очистить корзину", callback_data="clear_cart")
    back = InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")
    order = InlineKeyboardButton(text="Оформить заказ", callback_data="order")
    products = [InlineKeyboardButton(text=f"❌ {i[0]}", callback_data=f"{int(i[1])}") for i in cart]
    kb.add(clear,back,order)
    kb.add(*products)
    return kb
def admin_panel_kb():
    kb = InlineKeyboardMarkup(row_width=1)
    admins = InlineKeyboardButton(text="Админы", callback_data="admins")
    base = InlineKeyboardButton(text="База данных", callback_data="get_base")
    menu = InlineKeyboardButton(text='Действия с меню', callback_data="change_menu")
    close = InlineKeyboardButton(text="Закрыть", callback_data="close")
    kb.add(admins, base, menu,close)
    return kb
def admins_kb():
    kb = InlineKeyboardMarkup(row_width=1)
    add_admins = InlineKeyboardButton(text="Добавить админа", callback_data="add_admin")
    delete_admin = InlineKeyboardButton(text="Удалить админа", callback_data="delete_admin")
    close = InlineKeyboardButton(text="Закрыть", callback_data="close")
    kb.add(add_admins, delete_admin, close)
    return kb
def base_kb():
    kb = InlineKeyboardMarkup(row_width=1)
    category = InlineKeyboardButton(text="Категории", callback_data="cats_excel")
    products = InlineKeyboardButton(text="Продукты", callback_data="prods_excel")
    users = InlineKeyboardButton(text="Юзеры", callback_data="users_excel")
    admins = InlineKeyboardButton(text="Админы", callback_data="admins_excel")
    close = InlineKeyboardButton(text="Закрыть", callback_data="close")
    kb.add(category, products, users, admins, close)
    return kb
def change_menu():
    pass
def add_cats():
    pass
def add_prods():
    pass
def change_prods():
    pass
def change_cats():
    pass
def delete_prods():
    pass
def delete_cats():
    pass
