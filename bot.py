from telebot import TeleBot
from interactions.locator import geolocators
from interactions.converting import convert_to_excel
import os
from database import productservice as pr
from database import userservice as us
from telebot.types import ReplyKeyboardRemove
import buttons as bt
from database import Base, engine
from interactions.all_states import All_states
bot = TeleBot("6431087071:AAG2KPGLVYSZT93rzOZ2IAuVWGmq8w87Mdc")
Base.metadata.create_all(bind=engine)
carts = {}
admins_group = -4111231307

@bot.message_handler(commands=["start", "admin"])
def start(message):
    user_id = message.from_user.id
    check_admin = us.check_admin(user_id)
    checker = us.check_user_db(user_id=user_id)
    if message.text == "/start":
        if checker == True:
            bot.set_state(user_id, All_states.mm_st, user_id)
            bot.send_message(user_id, "Выберите действие", reply_markup=bt.main_menu_ru())
        elif checker == False:
            bot.send_message(user_id, "Добро пожаловать! Введите своё имя")
            bot.register_next_step_handler(message, get_name)
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
        us.register_user(user_id=user_id, user_name=name, phone_number=phone_number)
        bot.send_message(user_id, "Выберите действие", reply_markup=bt.main_menu_ru())
        bot.set_state(user_id, All_states.mm_st, user_id)
@bot.callback_query_handler(lambda call: call.data in ["back", "user_cart", "plus", "minus",
                                                       "none", "to_cart", "clear_cart", "main_menu",
                                                       "order", "close", 'cats_excel', "prods_excel",
                                                       "admins_excel", "get_base", "users_excel"])
def for_call(call):
    user_id = call.message.chat.id
    if call.data == "back":
        bot.delete_message(user_id, call.message.message_id)
        cats = pr.get_cats()
        bot.send_message(user_id, "Выберите действие", reply_markup=bt.categories_ru(cats))
    elif call.data == "close":
        bot.delete_message(user_id, call.message.message_id)
    elif call.data == "user_cart":
        bot.delete_message(user_id, call.message.message_id)
        user_cart = pr.get_user_cart(user_id)
        full_text = f"Ваша корзина \n\n"
        total_amount = 0
        for i in user_cart:
            full_text += f"{i[0]} x{i[1]} = {i[2]}\n"
            total_amount += i[2]
        full_text += f"\n\nИтоговая сумма {total_amount}"
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
        pr.add_to_cart(user_id=user_id, product_name=carts[user_id]["pr_name"],
                       product_count=carts[user_id]["pr_count"],
                       product_price=carts[user_id]["pr_price"])
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
        bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
        bot.send_message(user_id, "Отправьте свою локацию", reply_markup=bt.location_kb_ru())
        bot.register_next_step_handler(call.message, get_location)
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


@bot.callback_query_handler(lambda call: call.data in pr.get_all_cats_name())
def call_cats(call):
    user_id = call.message.chat.id
    bot.delete_message(user_id, call.message.message_id)
    get_products = pr.get_products_by_cat(call.data)
    bot.send_message(user_id, f'{call.data}\n'
                              f'Выберите продукт', reply_markup=bt.products_ru(get_products))
@bot.callback_query_handler(lambda call: call.data in pr.get_all_products_name())
def call_products(call):
    user_id = call.message.chat.id
    product = pr.get_product(call.data)
    bot.delete_message(user_id, call.message.id)
    carts[user_id] = {"pr_name": product[0], "pr_count": 1, "pr_price": product[1]}
    bot.send_photo(user_id, photo=product[3], caption=f"{product[0]}\n"
                                                      f"Описание: {product[2]}\n"
                                                      f"Цена: {product[1]}\n"
                                                      f"Выбрите количество: ", reply_markup=bt.exact_product_ru())
try:
    @bot.callback_query_handler(lambda call: int(call.data) in pr.user_cart_ids(call.message.chat.id))
    def call_for_delete_cart(call):
        user_id = call.message.chat.id
        pr.delete_exact_product_from_cart(call.data)
        user_cart = pr.get_user_cart(user_id)
        full_text = f"Ваша корзина \n\n"
        total_amount = 0
        for i in user_cart:
            full_text += f"{i[0]} x{i[1]} = {i[2]}\n"
            total_amount += i[2]
        full_text += f"\n\nИтоговая сумма {total_amount}"
        cart = pr.get_user_cart_id_name(user_id)
        bot.edit_message_text(chat_id=user_id, message_id=call.message.id, text=full_text,
                              reply_markup=bt.get_cart_kb_ru(cart))
except:
    pass
@bot.message_handler(content_types=["text"])
def mm(message):
    user_id = message.from_user.id
    text = message.text
    if text == "🍽Меню":
        cats = pr.get_cats()
        bot.send_message(user_id, "Выберите действие", reply_markup=bt.categories_ru(cats))
    elif text == "ℹ️Информация":
        bot.send_message(user_id, "Напишите свой отзыв")
        bot.register_next_step_handler(message, feedback)
    elif text == "✍️Оставить отзыв":
        bot.send_message(user_id, "Напишите свой отзыв", reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(message, feedback)
    elif text == "⚙️Настрйоки":
        pass
    elif text == "🛒Корзина":
        user_cart = pr.get_user_cart(user_id)
        full_text = f"Ваша корзина \n\n"
        total_amount = 0
        for i in user_cart:
            full_text += f"{i[0]} x{i[1]} = {i[2]}\n"
            total_amount += i[2]
        full_text += f"\n\nИтоговая сумма {total_amount}"
        cart = pr.get_user_cart_id_name(user_id)
        bot.send_message(user_id, full_text, reply_markup=bt.get_cart_kb_ru(cart))
    elif text == "🇺🇿O'zbek tili":
        pass
def get_location(message):
    user_id = message.from_user.id
    if message.location:
        longitude = message.location.longitude
        latitude = message.location.latitude
        location = geolocators(latitude, longitude)
        user_cart = pr.get_user_cart(user_id)
        user_info = us.get_user_info(user_id)
        full_text = (f"Новый заказ от юзера <code>{user_id}</code>: \n"
                     f"Номер: {user_info[0]}\n"
                     f"Язык: {user_info[1]}\n"
                     f"Адрес: {location}\n\n")
        total_amount = 0
        for i in user_cart:
            full_text += f"{i[0]} x{i[1]} = {i[2]}\n"
            total_amount += i[2]
        full_text += f"\n\nИтоговая сумма {total_amount}"
        bot.send_message(admins_group, full_text, parse_mode="HTML")
        bot.send_message(user_id, f"Ваш заказ оформлен. Отправьте {total_amount} "
                                  f"на карту ... .... и подтвердите платеж скриншотом",
                         reply_markup=ReplyKeyboardRemove())
        pr.delete_user_cart(user_id)
        bot.send_message(user_id, "Выберите действие", reply_markup=bt.main_menu_ru())
    elif message.text == "❌Отмена":
        bot.send_message(user_id, "Вы отменили оформление заказа", reply_markup=ReplyKeyboardRemove())
        bot.send_message(user_id, "Выберите действие", reply_markup=bt.main_menu_ru())
    else:
        bot.send_message(user_id, "Отправьте локацию через кнопку")
        bot.register_next_step_handler(message, get_location)
def feedback(message):
    user_id = message.from_user.id
    feedback_text = message.text
    full_text = (f"<b>Айди юзера</b>:<code>{user_id}</code>\n"
                 f"<b>Текст отзыва</b>: {feedback_text}")
    bot.send_message(user_id, "Спасибо за отзыв!")
    bot.send_message(admins_group, full_text, parse_mode="HTML")

bot.polling(non_stop=True)