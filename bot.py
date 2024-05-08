from telebot import TeleBot
from interactions.locator import geolocators
from interactions.converting import convert_to_excel
import os
from database import productservice as pr
from database import userservice as us
from telebot.types import ReplyKeyboardRemove
import buttons as bt
from database import Base, engine
import time
import threading

bot = TeleBot("7030688867:AAHTp74pQhErZWElrRKFmcucOOgsC4tx1hg")
Base.metadata.create_all(bind=engine)
carts = {}
admins_group = -4111231307
# us.register_admin(305896408, "Programmer")
# us.register_admin(305896408, "Programmer")
# pr.register_category("🍱Сеты", "🍱Setlar")
# pr.register_category("🍣Суши", "🍣Sushi")
# pr.register_category("🍤Роллы", "🍤Rollar")
# pr.register_category("🥬Салаты", "🥬Салатлар")
# pr.register_category("🥡ВОК", "🥡WOK")
# pr.register_category("🍜Супы", "🍜Шорбалар")
# pr.register_category("🥟Горячие закуски", "🥟 Иситиқ истифода")
# pr.register_category("🍞Хлеб", "🍞Нон")
# pr.register_category("🍰Десерты", "🍰Десертлар")
# pr.register_category("🍹Напитки", "🍹Ичимликлар")
# pr.register_category("🍹Напитки", "🍹Ичимликлар")
# pr.register_category("❇️Дополнительно", "❇️Қўшимча")
@bot.message_handler(commands=["start", "admin"])
def start(message):
    user_id = message.from_user.id
    check_admin = us.check_admin(user_id)
    # check_admin = True
    checker = us.check_user_db(user_id=user_id)
    if message.text == "/start":
        if checker == True:
            language = us.check_language_db(user_id)
            if language == "ru":

                bot.send_message(user_id, "Выберите действие", reply_markup=bt.main_menu_ru())
            elif language == "uz":

                bot.send_message(user_id, "Ҳаракатни танланг", reply_markup=bt.main_menu_uz())
        elif checker == False:
                bot.send_message(user_id, "Добро пожаловать! Выберите язык \n\n"
                                          "Хуш келибсиз! Тилни танланг", reply_markup=bt.choose_language_kb())

    elif message.text == "/admin":
        if check_admin == True:
            bot.send_message(user_id, "Панель админа", reply_markup=bt.admin_panel_kb())
        else:
            pass
def get_name(message):
    user_id = message.from_user.id
    name = message.text
    bot.send_message(user_id, "Отправьте свой номер через кнопку", reply_markup=bt.phone_kb_ru())
    bot.register_next_step_handler(message, get_phone, name)
def get_phone(message, name):
    user_id = message.from_user.id
    if message.contact:
        phone_number = message.contact.phone_number
        bot.send_message(user_id, "Вы успешно прошли регистрацию!", reply_markup=ReplyKeyboardRemove())
        us.register_user(user_id=user_id, user_name=name, phone_number=phone_number, language="ru")
        bot.send_message(user_id, "Выберите действие", reply_markup=bt.main_menu_ru())



def get_name_uz(message):
    user_id = message.from_user.id
    name = message.text
    bot.send_message(user_id, "Телефон рақамингизни тугмача орқали юборинг", reply_markup=bt.phone_kb_uz())
    bot.register_next_step_handler(message, get_phone_uz, name)


def get_phone_uz(message, name):
    user_id = message.from_user.id
    if message.contact:
        phone_number = message.contact.phone_number
        bot.send_message(user_id, "Рўйхатдан ўтдингиз!", reply_markup=ReplyKeyboardRemove())
        us.register_user(user_id=user_id, user_name=name, phone_number=phone_number, language="uz")
        bot.send_message(user_id, "Ҳаракатни танланг", reply_markup=bt.main_menu_uz())



@bot.callback_query_handler(lambda call: call.data in ["back", "user_cart", "plus", "minus",
                                                       "none", "to_cart", "clear_cart", "main_menu",
                                                       "order", "close", 'cats_excel', "prods_excel",
                                                       "admins_excel", "get_base", "users_excel",
                                                       "yes", "no", "ru_lang", "admin_product", "admins",
                                                       "add_admin", "delete_admin", "add_product",
                                                       "delete_product", "change_product", "change_name",
                                                       "change_desc", "change_cat", "change_photo",
                                                       "change_price", "change_ru_name", "change_uz_name",
                                                       "change_ru_desc", "change_uz_desc", "send_prove",
                                                       'accept_order', "cancel_order", "send_message", 'mailing',
                                                       "to_mm"])
def for_call(call):
    user_id = call.message.chat.id
    if call.data == "back":
        bot.delete_message(user_id, call.message.message_id)
        cats = pr.get_cats()
        bot.send_message(user_id, "Выберите действие", reply_markup=bt.categories_ru(cats))
    elif call.data == "mailing":
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "Введите текст рассылки или отправьте фотографию с описанием, либо отмените рассылку через кнопку в меню",
                         reply_markup=bt.cancel_kb())
        bot.register_next_step_handler(call.message, mailing_to_all)
    elif call.data == "ru_lang":
        bot.send_message(user_id, "Введите своё имя")
        bot.register_next_step_handler(call.message, get_name)
    elif call.data == "close":
        bot.delete_message(user_id, call.message.message_id)
    elif call.data == "user_cart":
        bot.delete_message(user_id, call.message.message_id)
        user_cart = pr.get_user_cart(user_id)
        full_text = f"Ваша корзина \n\n"
        total_amount = 0
        for i in user_cart:
            full_text += f"{i[0]} x{i[1]} = {i[2]:,.0f}\n"
            total_amount += i[2]
        full_text += f"\n\nИтоговая сумма {total_amount:,.0f} сум"
        cart = pr.get_user_cart_id_name(user_id)
        pr_name = []
        for i in cart:
            pr_name.append(i[0])
        bot.send_message(user_id, full_text, reply_markup=bt.get_cart_kb_ru(cart))
    elif call.data == "plus":
        current_ammount = carts[user_id]["pr_count"]
        carts[user_id]["pr_count"] += 1
        bot.edit_message_reply_markup(chat_id=user_id, message_id=call.message.id,
                                      reply_markup=bt.exact_product_ru(current_ammount, "plus"))
    elif call.data == "minus":
        current_ammount = carts[user_id]["pr_count"]
        if current_ammount > 1:
            carts[user_id]["pr_count"] -= 1
            bot.edit_message_reply_markup(chat_id=user_id, message_id=call.message.id,
                                      reply_markup=bt.exact_product_ru(current_ammount, "minus"))
        else:
            pass
    elif call.data == "none":
        pass
    elif call.data == "to_cart":
        pr.add_to_cart(user_id=user_id, product_name=carts.get(user_id).get("pr_name"),
                       product_count=carts.get(user_id).get("pr_count"),
                       product_price=carts.get(user_id).get("pr_price"))
        carts.pop(user_id)
        bot.delete_message(chat_id=user_id, message_id=call.message.id)
        bot.send_message(user_id, "Продукт успешно добавлен в корзину")
        cats = pr.get_cats()
        bot.send_message(user_id, "Выберите действие", reply_markup=bt.categories_ru(cats))
    elif call.data == "clear_cart":
        bot.delete_message(chat_id=user_id, message_id=call.message.id)
        pr.delete_user_cart(user_id)
        bot.send_message(user_id, "Ваша корзина очищена")
        cats = pr.get_cats()
        bot.send_message(user_id, "Выберите действие", reply_markup=bt.categories_ru(cats))
    elif call.data == "main_menu":
        bot.delete_message(chat_id=user_id, message_id=call.message.id)
        bot.send_message(user_id, "Выберите действие", reply_markup=bt.main_menu_ru())
    elif call.data == "order":
        bot.delete_message(user_id, call.message.id)
        bot.send_message(user_id, "Хотите заказать дополнительный имбирь или васаби?", reply_markup=bt.accept_kb())
    elif call.data == "no":
        bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
        try:
            carts.pop(user_id)
        except:
            pass
        bot.send_message(user_id, "Отправьте свою локацию", reply_markup=bt.location_kb_ru())
        bot.register_next_step_handler(call.message, get_location)
    elif call.data == "yes":
        bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
        cats = pr.get_cats()
        bot.send_message(user_id, "Выберите действие", reply_markup=bt.categories_ru(cats))
    elif call.data == "get_base":
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "Выберите таблицу", reply_markup=bt.base_kb())
    elif call.data == "cats_excel":
        bot.delete_message(chat_id=user_id, message_id=call.message.id)
        try:
            file = convert_to_excel("category")
            excel_file = open(f"{file}.xlsx", "rb")
            bot.send_document(user_id, excel_file)
            excel_file.close()
            os.remove(f"{file}.xlsx")
        except:
            bot.send_message(user_id, "Произошла ошибка")
    elif call.data == "prods_excel":
        bot.delete_message(chat_id=user_id, message_id=call.message.id)
        try:
            file = convert_to_excel("product")
            excel_file = open(f"{file}.xlsx", "rb")
            bot.send_document(user_id, excel_file)
            excel_file.close()
            os.remove(f"{file}.xlsx")
        except:
            bot.send_message(user_id, "Произошла ошибка")
    elif call.data == "users_excel":
        bot.delete_message(chat_id=user_id, message_id=call.message.id)
        try:
            file = convert_to_excel("user")
            excel_file = open(f"{file}.xlsx", "rb")
            bot.send_document(user_id, excel_file)
            excel_file.close()
            os.remove(f"{file}.xlsx")
        except:
            bot.send_message(user_id, "Произошла ошибка")

    elif call.data == "admins_excel":
        bot.delete_message(chat_id=user_id, message_id=call.message.id)
        try:
            file = convert_to_excel("admin")
            excel_file = open(f"{file}.xlsx", "rb")
            bot.send_document(user_id, excel_file)
            excel_file.close()
            os.remove(f"{file}.xlsx")
        except:
            bot.send_message(user_id, "Произошла ошибка")
    elif call.data == "admin_product":
        bot.delete_message(chat_id=user_id, message_id=call.message.id)
        bot.send_message(user_id, "Выберите действие с продуктами", reply_markup=bt.admin_product_menu_kb())
    elif call.data == "add_product":
        bot.delete_message(chat_id=user_id, message_id=call.message.id)
        bot.send_message(user_id, "Введите имя продукта на русском", reply_markup=bt.cancel_kb())
        bot.register_next_step_handler(call.message, product_ru_name)
    elif call.data == "delete_product":
        bot.delete_message(chat_id=user_id, message_id=call.message.id)
        bot.send_message(user_id, "Введите имя удаляемого продукта на русском", reply_markup=bt.cancel_kb())
        bot.register_next_step_handler(call.message, delete_product)
    elif call.data == "admins":
        bot.delete_message(chat_id=user_id, message_id=call.message.id)
        bot.send_message(user_id, "Выберите действие", reply_markup=bt.admins_kb())
    elif call.data == "delete_admin":
        bot.delete_message(chat_id=user_id, message_id=call.message.id)
        bot.send_message(user_id, "Введите тг айди удаляемого админа", reply_markup=bt.cancel_kb())
        bot.register_next_step_handler(call.message, delete_admin)
    elif call.data == "add_admin":
        bot.delete_message(chat_id=user_id, message_id=call.message.id)
        bot.send_message(user_id, "Введите тг айди нового админа", reply_markup=bt.cancel_kb())
        bot.register_next_step_handler(call.message, add_admin)
    elif call.data == "change_product":
        bot.delete_message(chat_id=user_id, message_id=call.message.id)
        bot.send_message(user_id, "Выберите действие", reply_markup=bt.change_product_kb())
    elif call.data == "change_name":
        bot.delete_message(chat_id=user_id, message_id=call.message.id)
        bot.send_message(user_id, "Какое название изменить?", reply_markup=bt.change_product_name_kb())
    elif call.data == "change_desc":
        bot.delete_message(chat_id=user_id, message_id=call.message.id)
        bot.send_message(user_id, "Какое описание изменить?", reply_markup=bt.change_product_desc_kb())
    elif call.data == "change_cat":
        bot.delete_message(chat_id=user_id, message_id=call.message.id)
        bot.send_message(user_id, "Напишите айди изменяемого продукта", reply_markup=bt.cancel_kb())
        bot.register_next_step_handler(call.message, change_prod_cat)
    elif call.data == "change_photo":
        bot.delete_message(chat_id=user_id, message_id=call.message.id)
        bot.send_message(user_id, "Напишите айди изменяемого продукта", reply_markup=bt.cancel_kb())
        bot.register_next_step_handler(call.message, change_prod_photo)
    elif call.data == "change_price":
        bot.delete_message(chat_id=user_id, message_id=call.message.id)
        bot.send_message(user_id, "Напишите айди изменяемого продукта", reply_markup=bt.cancel_kb())
        bot.register_next_step_handler(call.message, change_prod_price)
    elif call.data == "change_ru_name":
        bot.delete_message(chat_id=user_id, message_id=call.message.id)
        bot.send_message(user_id, "Напишите айди изменяемого продукта", reply_markup=bt.cancel_kb())
        bot.register_next_step_handler(call.message, change_prod_ru_name)
    elif call.data == "change_uz_name":
        bot.delete_message(chat_id=user_id, message_id=call.message.id)
        bot.send_message(user_id, "Напишите айди изменяемого продукта", reply_markup=bt.cancel_kb())
        bot.register_next_step_handler(call.message, change_prod_uz_name)
    elif call.data == "change_ru_desc":
        bot.delete_message(chat_id=user_id, message_id=call.message.id)
        bot.send_message(user_id, "Напишите айди изменяемого продукта", reply_markup=bt.cancel_kb())
        bot.register_next_step_handler(call.message, change_prod_ru_desc)
    elif call.data == "change_uz_desc":
        bot.delete_message(chat_id=user_id, message_id=call.message.id)
        bot.send_message(user_id, "Напишите айди изменяемого продукта", reply_markup=bt.cancel_kb())
        bot.register_next_step_handler(call.message, change_prod_uz_desc)
    elif call.data == "send_prove":
        bot.send_message(user_id, "Отправьте скриншот/фото оплаты")
        bot.register_next_step_handler(call.message, send_screenshot)
    elif call.data == "accept_order":
        bot.send_message(user_id, "Введи айди пользователя для подтверждения заказа", reply_markup=bt.cancel_kb())
        bot.register_next_step_handler(call.message, admins_answer_ru, "accept")
    elif call.data == "cancel_order":
        bot.send_message(user_id, "Введи айди пользователя для отказа заказа", reply_markup=bt.cancel_kb())
        bot.register_next_step_handler(call.message, admins_answer_ru, "cancel")
    elif call.data == "send_message":
        bot.send_message(user_id, "Введи айди пользователя", reply_markup=bt.cancel_kb())
        bot.register_next_step_handler(call.message, admins_get_text_ru)
    elif call.data == "to_mm":
        checker = us.check_user_db(user_id=user_id)
        if checker == True:
            language = us.check_language_db(user_id)
            if language == "ru":
                cats = pr.get_cats()
                bot.send_message(user_id, "Выберите действие", reply_markup=bt.categories_ru(cats))

            elif language == "uz":
                cats = pr.get_cats_uz()
                bot.send_message(user_id, "Ҳаракатни танланг", reply_markup=bt.categories_uz(cats))
        elif checker == False:
            bot.send_message(user_id, "Добро пожаловать! Выберите язык \n\n"
                                      "Хуш келибсиз! Тилни танланг", reply_markup=bt.choose_language_kb())




@bot.callback_query_handler(lambda call: call.data in ["back_uz", "user_cart_uz", "plus_uz", "minus_uz",
                                                       "none", "to_cart_uz", "clear_cart_uz", "main_menu_uz",
                                                       "order_uz", "close_uz", "yes_uz", "no_uz", "uz_lang",
                                                       "send_prove_uz", "cancel_order_uz", "accept_order_uz",
                                                       "send_message_uz"])
def for_call_uz(call):
    user_id = call.message.chat.id
    if call.data == "back_uz":
        bot.delete_message(user_id, call.message.message_id)
        cats = pr.get_cats_uz()
        bot.send_message(user_id, "Ҳаракатни танланг", reply_markup=bt.categories_uz(cats))
    elif call.data == "uz_lang":
        bot.send_message(user_id, "Исмингизни киритинг")
        bot.register_next_step_handler(call.message, get_name_uz)
    elif call.data == "close_uz":
        bot.delete_message(user_id, call.message.message_id)
    elif call.data == "user_cart_uz":
        bot.delete_message(user_id, call.message.message_id)
        user_cart = pr.get_user_cart(user_id)
        full_text = f"Саватингиз \n\n"
        total_amount = 0
        for i in user_cart:
            full_text += f"{i[0]} x{i[1]} = {i[2]}\n"
            total_amount += i[2]
        full_text += f"\n\nУмумий сумма: {total_amount:,.0f} сўм"
        cart = pr.get_user_cart_id_name(user_id)
        pr_name = []
        for i in cart:
            pr_name.append(i[0])
        bot.send_message(user_id, full_text, reply_markup=bt.get_cart_kb_uz(cart))
    elif call.data == "plus_uz":
        current_ammount = carts[user_id]["pr_count"]
        carts[user_id]["pr_count"] += 1
        bot.edit_message_reply_markup(chat_id=user_id, message_id=call.message.id,
                                      reply_markup=bt.exact_product_uz(current_ammount, "plus"))
    elif call.data == "minus_uz":
        current_ammount = carts[user_id]["pr_count"]
        if current_ammount > 1:
            carts[user_id]["pr_count"] -= 1
            bot.edit_message_reply_markup(chat_id=user_id, message_id=call.message.id,
                                      reply_markup=bt.exact_product_uz(current_ammount, "minus"))
        else:
            pass
    elif call.data == "none":
        pass
    elif call.data == "to_cart_uz":
        pr.add_to_cart(user_id=user_id, product_name=carts.get(user_id).get("pr_name"),
                       product_count=carts.get(user_id).get("pr_count"),
                       product_price=carts.get(user_id).get("pr_price"))
        carts.pop(user_id)
        bot.delete_message(chat_id=user_id, message_id=call.message.id)
        bot.send_message(user_id, "Маҳсулот муваффақиятли саватга қўшилди")
        cats = pr.get_cats_uz()
        bot.send_message(user_id, "Ҳаракатни танланг", reply_markup=bt.categories_uz(cats))
    elif call.data == "clear_cart_uz":
        bot.delete_message(chat_id=user_id, message_id=call.message.id)
        pr.delete_user_cart(user_id)
        bot.send_message(user_id, "Саватингиз бўшатилди")
        cats = pr.get_cats_uz()
        bot.send_message(user_id, "Ҳаракатни танланг", reply_markup=bt.categories_uz(cats))
    elif call.data == "main_menu_uz":
        bot.delete_message(chat_id=user_id, message_id=call.message.id)
        bot.send_message(user_id, "Ҳаракатни танланг", reply_markup=bt.main_menu_uz())
    elif call.data == "order_uz":
        bot.delete_message(user_id, call.message.id)
        bot.send_message(user_id, "Бошқа нимани буюртмақчимисиз?", reply_markup=bt.accept_kb_uz())
    elif call.data == "no_uz":
        bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
        try:
            carts.pop(user_id)
        except:
            pass
        bot.send_message(user_id, "Локациянгизни юборинг", reply_markup=bt.location_kb_uz())
        bot.register_next_step_handler(call.message, get_location_uz)
    elif call.data == "yes_uz":
        bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
        cats = pr.get_cats_uz()
        bot.send_message(user_id, "Ҳаракатни танланг", reply_markup=bt.categories_uz(cats))
    elif call.data == "send_prove_uz":
        bot.send_message(user_id, "Тўлов расмини/скриншотини юборинг", reply_markup=bt.cancel_kb_uz())
        bot.register_next_step_handler(call.message, send_screenshot_uz)
    elif call.data == "accept_order_uz":
        bot.send_message(user_id, "Қўшимча имбир ёки восаби истайсизми?", reply_markup=bt.cancel_kb_uz())
        bot.register_next_step_handler(call.message, admins_answer_uz, "accept")
    elif call.data == "cancel_order_uz":
        bot.send_message(user_id, "Буюртмани рад этган фойдаланувчи идентификаторини киритинг", reply_markup=bt.cancel_kb_uz())
        bot.register_next_step_handler(call.message, admins_answer_uz, "cancel")
    elif call.data == "send_message_uz":
        bot.send_message(user_id, "Фойдаланувчи идентификаторини киритинг", reply_markup=bt.cancel_kb_uz())
        bot.register_next_step_handler(call.message, admins_get_text_uz)



@bot.callback_query_handler(lambda call: call.data in pr.get_all_cats_name() or call.data in pr.get_all_cats_name_uz())
def call_cats(call):
    user_id = call.message.chat.id
    language = us.check_language_db(user_id)
    bot.delete_message(user_id, call.message.message_id)
    if language == "ru":
        get_products = pr.get_products_by_cat(call.data)
        bot.send_message(user_id, f'{call.data}\n'
                                  f'Выберите продукт', reply_markup=bt.products_ru(get_products))
    elif language == "uz":
        get_products = pr.get_products_by_cat_uz(call.data)
        bot.send_message(user_id, f'{call.data}\n'
                                  f'Продуктни танланг', reply_markup=bt.products_uz(get_products))

@bot.callback_query_handler(lambda call: call.data in pr.get_all_products_name())
def call_products(call):
    user_id = call.message.chat.id
    try:
        product = pr.get_product(call.data)
        bot.delete_message(user_id, call.message.id)
        carts[user_id] = {}
        carts[user_id] = {"pr_name": product[0], "pr_count": 1, "pr_price": product[1]}
        bot.send_photo(user_id, photo=product[3], caption=f"{product[0]}\n"
                                                          f"<b>Описание</b>: {product[2]}\n"
                                                          f"<b>Цена</b>: {product[1]:,.0f} сум\n"
                                                          f"Выбрите количество: ", reply_markup=bt.exact_product_ru(),
                       parse_mode="HTML")
    except:
        pass
@bot.callback_query_handler(lambda call: call.data in pr.get_all_products_name_uz())
def call_products_uz(call):
    user_id = call.message.chat.id
    product = pr.get_product_uz(call.data)
    bot.delete_message(user_id, call.message.id)
    carts[user_id] = {}
    carts[user_id] = {"pr_name": product[0], "pr_count": 1, "pr_price": product[1]}

    bot.send_photo(user_id, photo=product[3], caption=f"{product[0]}\n"
                                                      f"<b>Тавсиф</b>: {product[2]}\n"
                                                      f"<b>Нарх</b>: {product[1]:,.0f} сўм\n"
                                                      f"Микдорни танланг: ", reply_markup=bt.exact_product_uz(),
                   parse_mode="HTML")


try:
    @bot.callback_query_handler(lambda call: call.data in pr.user_cart_ids(call.message.chat.id))
    def call_for_delete_cart(call):
        user_id = call.message.chat.id
        language = us.check_language_db(user_id)
        if language == "ru":
            pr.delete_exact_product_from_cart(call.data)
            user_cart = pr.get_user_cart(user_id)
            full_text = f"Ваша корзина \n\n"
            total_amount = 0
            for i in user_cart:
                full_text += f"{i[0]} x{i[1]} = {i[2]:,.0f}\n"
                total_amount += i[2]
            full_text += f"\n\nИтоговая сумма {total_amount:,.0f} сум"
            cart = pr.get_user_cart_id_name(user_id)
            bot.edit_message_text(chat_id=user_id, message_id=call.message.id, text=full_text,
                                  reply_markup=bt.get_cart_kb_ru(cart))
        elif language == "uz":
            pr.delete_exact_product_from_cart(call.data)
            user_cart = pr.get_user_cart(user_id)
            full_text = f"Саватингиз \n\n"
            total_amount = 0
            for i in user_cart:
                full_text += f"{i[0]} x{i[1]} = {i[2]:,.0f}\n"
                total_amount += i[2]
            full_text += f"\n\nУмумий сумма {total_amount:,.0f} сўм"
            cart = pr.get_user_cart_id_name(user_id)
            bot.edit_message_text(chat_id=user_id, message_id=call.message.id, text=full_text,
                                  reply_markup=bt.get_cart_kb_uz(cart))
except:
    pass
@bot.message_handler(content_types=["text"])
def mm(message):
    user_id = message.from_user.id
    language = us.check_language_db(user_id)
    text = message.text
    if language == "ru":
        if text == "🍽Меню":
            cats = pr.get_cats()
            bot.send_message(user_id, "Выберите действие", reply_markup=bt.categories_ru(cats))
        elif text == "✍️Оставить отзыв":
            bot.send_message(user_id, "Напишите свой отзыв", reply_markup=ReplyKeyboardRemove())
            bot.register_next_step_handler(message, feedback)
        elif text == "🛒Корзина":
            user_cart = pr.get_user_cart(user_id)
            full_text = f"Ваша корзина \n\n"
            total_amount = 0
            for i in user_cart:
                full_text += f"{i[0]} x{i[1]} = {i[2]:,.0f}\n"
                total_amount += i[2]
            full_text += f"\n\nИтоговая сумма {total_amount:,.0f} сум"
            cart = pr.get_user_cart_id_name(user_id)
            bot.send_message(user_id, full_text, reply_markup=bt.get_cart_kb_ru(cart))
        elif text == "🇺🇿O'zbek tili":
            us.change_language(user_id=user_id, new_language="uz")
            bot.send_message(user_id, "Ҳаракатни танланг", reply_markup=bt.main_menu_uz())


    elif language == "uz":
        if text == "🍽Меню":
            cats = pr.get_cats_uz()
            bot.send_message(user_id, "Ҳаракатни танланг", reply_markup=bt.categories_uz(cats))
        elif text == "✍️Фикр қолдириш":
            bot.send_message(user_id, "Фикрингизни ёзинг", reply_markup=ReplyKeyboardRemove())
            bot.register_next_step_handler(message, feedback_uz)
        elif text == "🛒Сават":
            user_cart = pr.get_user_cart(user_id)
            full_text = f"Саватингиз \n\n"
            total_amount = 0
            for i in user_cart:
                full_text += f"{i[0]} x{i[1]} = {i[2]:,.0f}\n"
                total_amount += i[2]
            full_text += f"\n\nУмумий сумма {total_amount:,.0f} сўм"
            cart = pr.get_user_cart_id_name(user_id)
            bot.send_message(user_id, full_text, reply_markup=bt.get_cart_kb_uz(cart))
        elif text == "🇷🇺Русский язык":
            us.change_language(user_id=user_id, new_language="ru")
            bot.send_message(user_id, "Выберите действие", reply_markup=bt.main_menu_ru())
    elif text == "❌Отменить":
        bot.send_message(user_id, "Дейcтdия отменены")
        bot.clear_step_handler(message)


def get_location(message):
    user_id = message.from_user.id
    if message.location:
        longitude = message.location.longitude
        latitude = message.location.latitude
        location = geolocators(latitude, longitude)
        user_cart = pr.get_user_cart(user_id)
        user_info = us.get_user_info(user_id)
        full_text = (f"Новый заказ от юзера <code>{user_id}</code>: \n"
                     f"<b>Номер</b>: +{user_info[0]}\n"
                     f"<b>Язык</b>: {user_info[1]}\n"
                     f"<b>Адрес</b>: <code>{location}</code>\n\n")
        total_amount = 0
        for i in user_cart:
            full_text += f"{i[0]} x{i[1]} = {i[2]}\n"
            total_amount += i[2]
        full_text += f"\n\nИтоговая сумма {total_amount}"
        bot.send_message(admins_group, full_text, parse_mode="HTML", reply_markup=bt.admin_accept_kb_ru())
        bot.send_message(user_id, f"Ваш заказ оформлен. Отправьте {total_amount:,.0f} сум "
                                  f"на карту:\n"
                                  f"<b>UZCARD</b>: <code>8600 4929 9818 5108</code>\n"
                                  f"<b>VISA</b>: <code>4278 3200 2178 0209</code>\n"
                                  f"и подтвердите платеж скриншотом",
                         reply_markup=bt.send_prove_kb(), parse_mode="HTML")
        pr.delete_user_cart(user_id)
        bot.send_message(user_id, "Выберите действие", reply_markup=bt.main_menu_ru())
    elif message.text == "❌Отмена":
        bot.send_message(user_id, "Вы отменили оформление заказа", reply_markup=ReplyKeyboardRemove())
        bot.send_message(user_id, "Выберите действие", reply_markup=bt.main_menu_ru())
    else:
        bot.send_message(user_id, "Отправьте локацию через кнопку")
        bot.register_next_step_handler(message, get_location)
def get_location_uz(message):
    user_id = message.from_user.id
    if message.location:
        longitude = message.location.longitude
        latitude = message.location.latitude
        location = geolocators(latitude, longitude)
        user_cart = pr.get_user_cart(user_id)
        user_info = us.get_user_info(user_id)
        full_text = (f"<b>Фойдаланувчи</b> <code>{user_id}</code>дан янги буюртма:\n"
                     f"<b>Телефон</b>: +{user_info[0]}\n"
                     f"<b>Til</b>: {user_info[1]}\n"
                     f"<b>Манзил</b>: <code>{location}</code>\n\n")
        total_amount = 0
        for i in user_cart:
            full_text += f"{i[0]} x{i[1]} = {i[2]}\n"
            total_amount += i[2]
        full_text += f"\n\nУмумий сумма {total_amount:,.0f} сўм"
        bot.send_message(admins_group, full_text, parse_mode="HTML", reply_markup=bt.admin_accept_kb_ru())
        bot.send_message(user_id, f"Сизнинг буюртмангиз қабул қилинди. {total_amount:,.0f} сўм "
                                  f"картага юборинг:\n"
                                  f"<b>UZCARD</b>: <code>8600 4929 9818 5108</code>\n"
                                  f"<b>VISA</b>: <code>4278 3200 2178 0209</code>\n"
                                  f"ва тасдиқлов учун расм юборинг",
                         reply_markup=bt.send_prove_kb(), parse_mode="HTML")
        pr.delete_user_cart(user_id)
        bot.send_message(user_id, "Ҳаракатни танланг", reply_markup=bt.main_menu_uz())
    elif message.text == "❌Бекор қилиш":
        bot.send_message(user_id, "Сиз буюртмани бекор қилдингиз", reply_markup=ReplyKeyboardRemove())
        bot.send_message(user_id, "Ҳаракатни танланг", reply_markup=bt.main_menu_uz())
    else:
        bot.send_message(user_id, "Локацияни юборинг")
        bot.register_next_step_handler(message, get_location_uz)

def feedback(message):
    user_id = message.from_user.id
    feedback_text = message.text
    full_text = (f"<b>Айди юзера</b>:<code>{user_id}</code>\n"
                 f"<b>Текст отзыва</b>: {feedback_text}")
    bot.send_message(user_id, "Спасибо за отзыв!\n"
                              "Выберите действие", reply_markup=bt.main_menu_ru())

    bot.send_message(admins_group, full_text, parse_mode="HTML")
def feedback_uz(message):
    user_id = message.from_user.id
    feedback_text = message.text
    full_text = (f"<b>Фойдаланувчи ID</b>:<code>{user_id}</code>\n"
                 f"<b>Фикр матни</b>: {feedback_text}")
    bot.send_message(user_id, "Фикрингиз учун рахмат!\n"
                              "Ҳаракатни танланг", reply_markup=bt.main_menu_uz())

    bot.send_message(admins_group, full_text, parse_mode="HTML")
def product_ru_name(message):
    user_id = message.from_user.id
    product_name = message.text
    if message.text == "❌Отменить":
        return bot.send_message(user_id, "Дейcтвия отменены", reply_markup=ReplyKeyboardRemove())
    bot.send_message(user_id, "Введите имя продукта на узбекском", reply_markup=bt.cancel_kb())
    bot.register_next_step_handler(message, product_uz_name, product_name)
def product_uz_name(message, product_name):
    user_id = message.from_user.id
    product_name_uz = message.text
    if message.text == "❌Отменить":
        return bot.send_message(user_id, "Дейcтвия отменены", reply_markup=ReplyKeyboardRemove())
    bot.send_message(user_id, "Введите описание к продукту на русском", reply_markup=bt.cancel_kb())
    bot.register_next_step_handler(message, product_ru_desc, product_name, product_name_uz)
def product_ru_desc(message, product_name, product_name_uz):
    user_id = message.from_user.id
    product_desc_ru = message.text
    if message.text == "❌Отменить":
        return bot.send_message(user_id, "Дейcтвия отменены", reply_markup=ReplyKeyboardRemove())
    bot.send_message(user_id, "Введите описание к продукту на узбекском", reply_markup=bt.cancel_kb())
    bot.register_next_step_handler(message, product_uz_desc, product_name, product_name_uz, product_desc_ru)
def product_uz_desc(message, product_name, product_name_uz, product_desc_ru):
    user_id = message.from_user.id
    product_desc_uz = message.text
    if message.text == "❌Отменить":
        return bot.send_message(user_id, "Дейcтвия отменены", reply_markup=ReplyKeyboardRemove())
    bot.send_message(user_id, "Введите цену продукта", reply_markup=bt.cancel_kb())
    bot.register_next_step_handler(message, product_prices, product_name, product_name_uz,
                                   product_desc_ru, product_desc_uz)
def product_prices(message, product_name, product_name_uz, product_desc_ru, product_desc_uz):
    user_id = message.from_user.id
    product_price = message.text
    if message.text == "❌Отменить":
        return bot.send_message(user_id, "Дейcтвия отменены", reply_markup=ReplyKeyboardRemove())
    bot.send_message(user_id, "Введите категорию продукта со всеми эмодзи", reply_markup=bt.cancel_kb())
    bot.register_next_step_handler(message, products_cat, product_name, product_name_uz,
                                   product_desc_ru, product_desc_uz, product_price)
def products_cat(message, product_name, product_name_uz, product_desc_ru, product_desc_uz, product_price):
    user_id = message.from_user.id
    cat = message.text
    if message.text == "❌Отменить":
        return bot.send_message(user_id, "Дейcтвия отменены", reply_markup=ReplyKeyboardRemove())

    bot.send_message(user_id, "Отправьте фотографию продукта не в виде файла(без сохранения качества)", reply_markup=bt.cancel_kb())
    bot.register_next_step_handler(message, product_photo, product_name, product_name_uz,
                                   product_desc_ru, product_desc_uz, product_price, cat)
def product_photo(message, product_name, product_name_uz, product_desc_ru, product_desc_uz, product_price, cat):
    user_id = message.from_user.id
    if message.photo:
            photo = message.photo[-1].file_id
            text = pr.register_product(product_name=product_name, product_name_uz=product_name_uz, product_price=product_price,
                                product_description=product_desc_ru, product_description_uz=product_desc_uz,
                                product_photo=photo, product_cat=cat)
            bot.send_message(user_id, text,
                             reply_markup=ReplyKeyboardRemove())
    elif message.text == "❌Отменить":
        return bot.send_message(user_id, "Дейcтвия отменены", reply_markup=ReplyKeyboardRemove())
    else:
        bot.send_message(user_id, "Отправьте фотографию в правильном формате")
        bot.register_next_step_handler(message, product_photo, product_name, product_name_uz,
                                       product_desc_ru, product_desc_uz, product_price, cat)

def delete_product(message):
    user_id = message.from_user.id
    text = message.text
    if message.text == "❌Отменить":
        return bot.send_message(user_id, "Дейcтвия отменены", reply_markup=ReplyKeyboardRemove())
    info = pr.delete_product(text)
    bot.send_message(user_id, info, reply_markup=ReplyKeyboardRemove())
def add_admin(message):
    user_id = message.from_user.id
    admin_id = message.text
    if message.text == "❌Отменить":
        return bot.send_message(user_id, "Дейcтвия отменены", reply_markup=ReplyKeyboardRemove())
    bot.send_message(user_id, "Введите имя нового админа", reply_markup=bt.cancel_kb())
    bot.register_next_step_handler(message, register_admin, admin_id)
def register_admin(message, admin_id):
    user_id = message.from_user.id
    name = message.text
    if message.text == "❌Отменить":
        return bot.send_message(user_id, "Дейcтвия отменены", reply_markup=ReplyKeyboardRemove())
    try:
        us.register_admin(int(admin_id), name)
        bot.send_message(user_id, "Админ успешно добавлен", reply_markup=ReplyKeyboardRemove())
    except:
        bot.send_message(user_id, "Не удалось добавить админа", reply_markup=ReplyKeyboardRemove())
def delete_admin(message):
    user_id = message.from_user.id
    admin_id = message.text
    if message.text == "❌Отменить":
        return bot.send_message(user_id, "Дейcтвия отменены", reply_markup=ReplyKeyboardRemove())
    try:
        us.delete_admin_db(admin_id)
        bot.send_message(user_id, "Админ удален", reply_markup=ReplyKeyboardRemove())
    except:
        bot.send_message(user_id, "Не удалось удалить админа", reply_markup=ReplyKeyboardRemove())
def change_prod_cat(message):
    user_id = message.from_user.id
    if message.text == "❌Отменить":
        return bot.send_message(user_id, "Дейcтвия отменены", reply_markup=ReplyKeyboardRemove())
    elif message.text.isdigit():
        product_id = int(message.text)
        column = "product_cat"
        bot.send_message(user_id, "Введите новую категорию для продукта", reply_markup=bt.cancel_kb())
        bot.register_next_step_handler(message, change_prod_info, product_id, column)
def change_prod_price(message):
    user_id = message.from_user.id
    if message.text == "❌Отменить":
        return bot.send_message(user_id, "Дейcтвия отменены", reply_markup=ReplyKeyboardRemove())
    elif message.text.isdigit():
        product_id = int(message.text)
        column = "product_price"
        bot.send_message(user_id, "Введите новую цену продукта", reply_markup=bt.cancel_kb())
        bot.register_next_step_handler(message, change_prod_info, product_id, column)
def change_prod_ru_name(message):
    user_id = message.from_user.id
    if message.text == "❌Отменить":
        return bot.send_message(user_id, "Дейcтвия отменены", reply_markup=ReplyKeyboardRemove())
    elif message.text.isdigit():
        product_id = int(message.text)
        column = "product_name"
        bot.send_message(user_id, "Введите новое русское название для продукта", reply_markup=bt.cancel_kb())
        bot.register_next_step_handler(message, change_prod_info, product_id, column)
def change_prod_uz_name(message):
    user_id = message.from_user.id
    if message.text == "❌Отменить":
        return bot.send_message(user_id, "Дейcтвия отменены", reply_markup=ReplyKeyboardRemove())
    elif message.text.isdigit():
        product_id = int(message.text)
        column = "product_name_uz"
        bot.send_message(user_id, "Введите новое узбекское название для продукта", reply_markup=bt.cancel_kb())
        bot.register_next_step_handler(message, change_prod_info, product_id, column)
def change_prod_ru_desc(message):
    user_id = message.from_user.id
    if message.text == "❌Отменить":
        return bot.send_message(user_id, "Дейcтвия отменены", reply_markup=ReplyKeyboardRemove())
    elif message.text.isdigit():
        product_id = int(message.text)
        column = "product_description"
        bot.send_message(user_id, "Введите новое русское описание продукта", reply_markup=bt.cancel_kb())
        bot.register_next_step_handler(message, change_prod_info, product_id, column)
def change_prod_uz_desc(message):
    user_id = message.from_user.id
    if message.text == "❌Отменить":
        return bot.send_message(user_id, "Дейcтвия отменены", reply_markup=ReplyKeyboardRemove())
    elif message.text.isdigit():
        product_id = int(message.text)
        column = "product_description_uz"
        bot.send_message(user_id, "Введите новое узбекское описание продукта", reply_markup=bt.cancel_kb())
        bot.register_next_step_handler(message, change_prod_info, product_id, column)
def change_prod_photo(message):
    user_id = message.from_user.id
    if message.text == "❌Отменить":
        return bot.send_message(user_id, "Дейcтвия отменены", reply_markup=ReplyKeyboardRemove())
    elif message.text.isdigit():
        product_id = int(message.text)
        column = "product_photo"
        bot.send_message(user_id, "Отправьте новое фото продукта(не в виде файла)", reply_markup=bt.cancel_kb())
        bot.register_next_step_handler(message, change_prod_photo_info, product_id, column)
def change_prod_info(message, product_id, column):
    user_id = message.from_user.id
    if message.text == "❌Отменить":
        return bot.send_message(user_id, "Дейcтвия отменены", reply_markup=ReplyKeyboardRemove())
    else:
        try:
            new_info = message.text
            pr.change_product_info(product_id=product_id, column=column, new_info=new_info)
            bot.send_message(user_id, "Информация успешно изменена", reply_markup=ReplyKeyboardRemove())
        except:
            bot.send_message(user_id, "Не удалось изменить информацию", reply_markup=ReplyKeyboardRemove())
def change_prod_photo_info(message, product_id, column):
    user_id = message.from_user.id
    if message.text == "❌Отменить":
        return bot.send_message(user_id, "Дейcтвия отменены", reply_markup=ReplyKeyboardRemove())
    elif message.photo:
            try:
                new_info = message.photo[-1].file_id
                pr.change_product_info(product_id=product_id, column=column, new_info=new_info)
                bot.send_message(user_id, "Информация успешно изменена", reply_markup=ReplyKeyboardRemove())
            except:
                bot.send_message(user_id, "Не удалось изменить информацию", reply_markup=ReplyKeyboardRemove())
    else:
        bot.send_message(user_id, "Отправьте фотографию в правильном формате", reply_markup=bt.cancel_kb())
        bot.register_next_step_handler(message, change_prod_photo_info, product_id, column)
def send_screenshot(message):
    user_id = message.from_user.id
    if message.text == "❌Отменить":
        return bot.send_message(user_id, "Дейcтвия отменены", reply_markup=ReplyKeyboardRemove())
    elif message.photo:
            try:
                photo = message.photo[-1].file_id
                bot.send_photo(chat_id=admins_group, photo=photo, caption=f"Подтвреждение оплаты от юзера <code> {user_id} </code>",
                               parse_mode="HTML", reply_markup=bt.admin_accept_kb_ru())
                bot.send_message(user_id, "Подтверждение отправлено. Ожидайте ответ")
            except:
                bot.send_message(user_id, "Не удалось подтвердить оплату, попробуйте заново", reply_markup=ReplyKeyboardRemove())
    else:
        bot.send_message(user_id, "Отправьте фотографию в правильном формате", reply_markup=bt.cancel_kb())
        bot.register_next_step_handler(message, send_screenshot)
def send_screenshot_uz(message):
    user_id = message.from_user.id
    if message.text == "❌Бекор қилиш":
        return bot.send_message(user_id, "Ҳаракат бекор қилинди", reply_markup=ReplyKeyboardRemove())
    elif message.photo:
            try:
                photo = message.photo[-1].file_id
                bot.send_photo(chat_id=admins_group, photo=photo, caption=f"Фойдаланувчидан тасдиқлов расми <code> {user_id} </code>",
                               parse_mode="HTML", reply_markup=bt.admin_accept_kb_uz())
                bot.send_message(user_id, "Тасдиқлов юборилди. Жавоб кутишингизни сўраймиз")
            except:
                bot.send_message(user_id, "Тўловни тасдиқлаш мумкин бўлмади, янгидан урунг", reply_markup=ReplyKeyboardRemove())
    else:
        bot.send_message(user_id, "Фотони тўғри форматда юборинг", reply_markup=bt.cancel_kb())
        bot.register_next_step_handler(message, send_screenshot)
def admins_get_text_ru(message):
    user_id = message.from_user.id
    type = "message"
    try:
        if message.text == "❌Отменить":
            return bot.send_message(user_id, "Дейcтвия отменены", reply_markup=ReplyKeyboardRemove())
        else:
            to_id = int(message.text)
            bot.send_message(admins_group, "Введите текст сообщение", reply_markup=bt.cancel_kb())
            bot.register_next_step_handler(message, admins_answer_ru, type, to_id)
    except:
        bot.send_message(admins_group, "Ошибка", reply_markup=ReplyKeyboardRemove())
def admins_get_text_uz(message):
    user_id = message.from_user.id
    type = "message"
    try:
        if message.text == "❌Бекор қилиш":
            return bot.send_message(user_id, "Ҳаракат бекор қилинди", reply_markup=ReplyKeyboardRemove())
        else:
            to_id = int(message.text)
            bot.send_message(admins_group, "Хабар матнини киритинг", reply_markup=bt.cancel_kb_uz())
            bot.register_next_step_handler(message, admins_answer_uz, type, to_id)
    except:
        bot.send_message(admins_group, "Хатолик", reply_markup=ReplyKeyboardRemove())


def admins_answer_ru(message, type, m_id=None):
    user_id = message.from_user.id
    to_id = message.text
    try:
        if message.text == "❌Отменить":
            return bot.send_message(admins_group, "Дейcтвия отменены", reply_markup=ReplyKeyboardRemove())
        elif type == "accept":
            bot.send_message(int(to_id), "Мы начали готовку вашего заказа")
            bot.send_message(admins_group, f"Заказ юзера <code>{to_id}</code> подтвержден ✅", parse_mode="HTML",
                             reply_markup=ReplyKeyboardRemove())
        elif type == "cancel":
            bot.send_message(int(to_id), "Ваш заказ отклонен")
            bot.send_message(admins_group, f"Заказ юзера <code>{to_id}</code> отколенен ❌", parse_mode="HTML",
                             reply_markup=ReplyKeyboardRemove())
        elif m_id:
            if type == "message":
                bot.send_message(m_id, to_id)
                bot.send_message(admins_group, f"Юзер <code>{m_id}</code> получил сообщение ☑️", parse_mode="HTML",
                                 reply_markup=ReplyKeyboardRemove())
    except:
        bot.send_message(admins_group, "Ошибка", reply_markup=ReplyKeyboardRemove())
def admins_answer_uz(message, type, m_id=None):
    user_id = message.from_user.id
    to_id = message.text
    try:
        if message.text == "❌Бекор қилиш":
            return bot.send_message(admins_group, "Ҳаракат бекор қилинди", reply_markup=ReplyKeyboardRemove())
        elif type == "accept":
            bot.send_message(int(to_id), "Сизнинг буюртмангизни тайёрлаб олишни бошладик")
            bot.send_message(admins_group, f"Фойдаланувчининг буюртмаси тасдиқланди ✅", parse_mode="HTML")
        elif type == "cancel":
            bot.send_message(int(to_id), "Сизнинг буюртмангиз рад этилди")
            bot.send_message(admins_group, f"Фойдаланувчининг буюртмаси рад этилди ❌", parse_mode="HTML",
                             reply_markup=ReplyKeyboardRemove())
        elif m_id and type == 'message':
            bot.send_message(m_id, to_id)
            bot.send_message(admins_group, f"Фойдаланувчига <code>{m_id}</code> хабар юборилди ☑️",
                             parse_mode="HTML", reply_markup=ReplyKeyboardRemove())
    except:
        bot.send_message(admins_group, "Ошибка", reply_markup=ReplyKeyboardRemove())
def send_message_to_user(target_id, text, photo):
    target = target_id
    if photo == None:
        try:
            time.sleep(0.1)
            bot.send_message(target, text, reply_markup=bt.for_mailing())
        except:
            pass
    else:
        try:
            time.sleep(0.1)
            bot.send_photo(target_id, photo=photo, caption=text, reply_markup=bt.for_mailing())
        except:
            pass


def mailing_to_all(message):
    user_id = message.from_user.id
    targets_id = us.get_all_users_id()
    if message.text == "Отмена❌":
        bot.send_message(user_id, "Рассылка отменена", reply_markup=ReplyKeyboardRemove())
    elif message.photo:
        photo = message.photo[-1].file_id
        text = message.caption
        for target_id in targets_id:
            thread = threading.Thread(target=send_message_to_user, args=(target_id, text, photo))
            thread.start()
    else:
        for target_id in targets_id:
            text = message.text
            photo = None
            thread = threading.Thread(target=send_message_to_user, args=(target_id, text, photo))
            thread.start()
    bot.send_message(user_id, "Рассылка завершена", reply_markup=ReplyKeyboardRemove())



bot.infinity_polling()