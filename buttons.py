from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


def choose_language_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    uz = InlineKeyboardButton(text="🇺🇿O'zbek tili", callback_data="uz_lang")
    ru = InlineKeyboardButton(text="🇷🇺Русский язык", callback_data="ru_lang")
    kb.add(uz, ru)
    return kb
def main_menu_ru():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    menu = KeyboardButton("🍽Меню")
    feedback = KeyboardButton("✍️Оставить отзыв")
    cart = KeyboardButton("🛒Корзина")
    uzb = KeyboardButton("🇺🇿O'zbek tili")
    kb.row(menu, feedback)
    kb.row(cart, uzb)
    return kb
def main_menu_uz():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    menu = KeyboardButton("🍽Меню")
    feedback = KeyboardButton("✍️Фикр қолдириш")
    cart = KeyboardButton("🛒Сават")
    ru = KeyboardButton("🇷🇺Русский язык")
    kb.row(menu, feedback)
    kb.row(cart, ru)
    return kb
def phone_kb_ru():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    phone_number = KeyboardButton("Отправить номер", request_contact=True)
    kb.add(phone_number)
    return kb
def phone_kb_uz():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    phone_number = KeyboardButton("Телефон рақамингизни юбориш", request_contact=True)
    kb.add(phone_number)
    return kb

def location_kb_ru():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    location = KeyboardButton("Отправить локацию", request_location=True)
    otmena = KeyboardButton("❌Отмена")
    kb.add(location)
    kb.row(otmena)
    return kb
def location_kb_uz():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    location = KeyboardButton("Локацияни юбориш", request_location=True)
    otmena = KeyboardButton("❌Бекор қилиш")
    kb.add(location)
    kb.row(otmena)
    return kb

def categories_ru(cats):
    kb = InlineKeyboardMarkup(row_width=2)
    back = InlineKeyboardButton(text="🔙Назад", callback_data="main_menu")
    all_cats = [InlineKeyboardButton(text=i[1], callback_data=i[1]) for i in cats]
    kb.add( *all_cats, back)
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
    accept =  InlineKeyboardButton(text="Добавить в корзину", callback_data="to_cart")
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
def get_cart_kb_ru(cart, status):
    kb = InlineKeyboardMarkup(row_width=1)
    if status == 1:
        clear = InlineKeyboardButton(text="Очистить корзину", callback_data="clear_cart")
        back = InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")
        order = InlineKeyboardButton(text="Оформить заказ", callback_data="order")
        products = [InlineKeyboardButton(text=f"❌ {i[0]}", callback_data=f"{int(i[1])}") for i in cart]
        kb.add(clear,back,order)
        kb.add(*products)
    elif status == 0:
        back = InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")
        kb.add(back)
    return kb
def categories_uz(cats):
    kb = InlineKeyboardMarkup(row_width=2)
    back = InlineKeyboardButton(text="🔙Орқага", callback_data="main_menu_uz")

    all_cats = [InlineKeyboardButton(text=i[1], callback_data=i[1]) for i in cats]
    kb.add(*all_cats, back)
    return kb

def products_uz(cats):
    kb = InlineKeyboardMarkup(row_width=2)
    back = InlineKeyboardButton(text="🔙Орқага", callback_data="back_uz")
    all_products = [InlineKeyboardButton(text=i, callback_data=i) for i in cats]
    kb.add(*all_products, back)
    return kb

def exact_product_uz(current_ammount=1, plus_or_minus=""):
    kb = InlineKeyboardMarkup(row_width=3)
    back = InlineKeyboardButton(text="⬅️ Орқага", callback_data="main_menu_uz")
    accept =  InlineKeyboardButton(text="Саватга қўшиш", callback_data="to_cart_uz")
    minus = InlineKeyboardButton(text="➖", callback_data="minus_uz")
    plus = InlineKeyboardButton(text="➕", callback_data="plus_uz")
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

def get_cart_kb_uz(cart, status):
    kb = InlineKeyboardMarkup(row_width=1)
    if status == 1:
        clear = InlineKeyboardButton(text="Саватни тозалаш", callback_data="clear_cart_uz")
        back = InlineKeyboardButton(text="⬅️ Орқага", callback_data="main_menu_uz")
        order = InlineKeyboardButton(text="Буюртма бериш", callback_data="order_uz")
        products = [InlineKeyboardButton(text=f"❌ {i[0]}", callback_data=f"{int(i[1])}") for i in cart]
        kb.add(clear,back,order)
        kb.add(*products)
    elif status == 0:
        back = InlineKeyboardButton(text="⬅️ Орқага", callback_data="main_menu_uz")
        kb.add(back)
    return kb

def accept_kb_uz():
    kb = InlineKeyboardMarkup(row_width=2)
    yes = InlineKeyboardButton(text="Ҳа, истайман", callback_data="yes_uz")
    no = InlineKeyboardButton(text="Йўқ, истамайман", callback_data="no_uz")
    kb.add(yes, no)
    return kb





############################################
def admin_panel_kb():
    kb = InlineKeyboardMarkup(row_width=1)
    admins = InlineKeyboardButton(text="Админы", callback_data="admins")
    base = InlineKeyboardButton(text="База данных", callback_data="get_base")
    menu = InlineKeyboardButton(text='Действия с продуктами', callback_data="admin_product")
    mailing = InlineKeyboardButton(text="Создать рассылку", callback_data="mailing")
    close = InlineKeyboardButton(text="Закрыть", callback_data="close")
    kb.add(admins, base, menu, mailing, close)
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
def accept_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    yes = InlineKeyboardButton(text="Да, хочу", callback_data="yes")
    no = InlineKeyboardButton(text="Нет, не хочу", callback_data="no")
    kb.add(yes, no)
    return kb
def cancel_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    cancel = KeyboardButton("❌Отменить")
    kb.add(cancel)
    return kb
def cancel_kb_uz():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    cancel = KeyboardButton("❌Бекор қилиш")
    kb.add(cancel)
    return kb

def change_product_kb():
    kb = InlineKeyboardMarkup(row_width=1)
    name = InlineKeyboardButton(text="Изменить название", callback_data="change_name")
    desc = InlineKeyboardButton(text="Изменить описание", callback_data="change_desc")
    cat = InlineKeyboardButton(text="Изменить категорию", callback_data="change_cat")
    photo = InlineKeyboardButton(text="Изменить фото", callback_data="change_photo")
    price = InlineKeyboardButton(text="Изменить цену", callback_data="change_price")
    close = InlineKeyboardButton(text="Закрыть", callback_data="close")
    kb.add(name, desc, cat, photo, price, close)
    return kb
def change_product_name_kb():
    kb = InlineKeyboardMarkup(row_width=1)
    name_ru = InlineKeyboardButton(text="Изменить русское название", callback_data="change_ru_name")
    name_uz = InlineKeyboardButton(text="Изменить узбекское название", callback_data="change_uz_name")
    close = InlineKeyboardButton(text="Закрыть", callback_data="close")
    kb.add(name_ru, name_uz, close)
    return kb
def change_product_desc_kb():
    kb = InlineKeyboardMarkup(row_width=1)
    name_ru = InlineKeyboardButton(text="Изменить русское описание", callback_data="change_ru_desc")
    name_uz = InlineKeyboardButton(text="Изменить узбекское описание", callback_data="change_uz_desc")
    close = InlineKeyboardButton(text="Закрыть", callback_data="close")
    kb.add(name_ru, name_uz, close)
def admin_product_menu_kb():
    kb = InlineKeyboardMarkup(row_width=1)
    add = InlineKeyboardButton(text="Добавить продукт", callback_data="add_product")
    delete = InlineKeyboardButton(text="Удалить продукт", callback_data="delete_product")
    change = InlineKeyboardButton(text="Изменить продукт", callback_data="change_product")
    close = InlineKeyboardButton(text="Закрыть", callback_data="close")
    kb.add(add, delete, change, close)
    return kb
def send_prove_kb():
    kb = InlineKeyboardMarkup(row_width=1)
    prove = InlineKeyboardButton(text="Подтвердить оплату", callback_data="send_prove")
    kb.add(prove)
    return kb
def admin_accept_kb_ru():
    kb = InlineKeyboardMarkup(row_width=1)
    ok = InlineKeyboardButton(text="Заказ принят", callback_data="accept_order")
    no = InlineKeyboardButton(text="Заказ отменен", callback_data="cancel_order")
    send_message = InlineKeyboardButton(text="Написать пользователю", callback_data="send_message")
    kb.add(ok, no, send_message)
    return kb
def admin_accept_kb_uz():
    kb = InlineKeyboardMarkup(row_width=1)
    ok = InlineKeyboardButton(text="Буюртма қабул қилинди", callback_data="accept_order_uz")
    no = InlineKeyboardButton(text="Буюртма бекор қилинди", callback_data="cancel_order_uz")
    send_message = InlineKeyboardButton(text="Фойдаланувчига хабар ёзиш", callback_data="send_message_uz")
    kb.add(ok, no, send_message)
    return kb

def for_mailing():
    kb = InlineKeyboardMarkup(row_width=1)
    but = InlineKeyboardButton(text="Начать заказ / Буюртма бошлаш", callback_data="to_mm")
    kb.add(but)
    return kb
