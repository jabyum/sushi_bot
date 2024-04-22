from telebot.handler_backends import State, StatesGroup

class All_states(StatesGroup):
    mm_st = State()
    cat_st = State()
    products_st = State()
    count_st = State()
    cart_st = State()
