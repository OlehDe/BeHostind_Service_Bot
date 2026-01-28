from aiogram.types import ReplyKeyboardMarkup, KeyboardButton #aiogram - це для створення ботів в тг приймати повідомлення, кнопки, команди, стани, платежі

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Купити хостинг")],
        [KeyboardButton(text="Орендувати сервер")],
        [KeyboardButton(text="Мої послуги")],
        [KeyboardButton(text="Баланс")],
        [KeyboardButton(text="Підтримка")]
    ],
    resize_keyboard=True
)
