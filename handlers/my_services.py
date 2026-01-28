from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text == "Мої послуги")
async def my_services(message: Message):
    # Для початку просто повідомлення, пізніше можна підключити базу
    await message.answer(
        "Ваші поточні послуги:\n"
        "1. Сервер Pro – орендовано на 3 місяці\n"
        "2. Домен example.com – придбаний\n\n"
        "Пізніше тут буде інтеграція з базою користувача."
    )
