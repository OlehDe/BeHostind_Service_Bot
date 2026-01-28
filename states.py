from aiogram.fsm.state import State, StatesGroup #aiogram - це для створення ботів в тг приймати повідомлення, кнопки, команди, стани, платежі

class BuyHosting(StatesGroup):
    choose_tariff = State()
    choose_period = State()
    confirm = State()
