from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text == "Орендувати сервер")
async def rent_hosting(message: Message):
    await message.answer(
        "Оберіть сервер для оренди:\n\n"
        "1. Basic – 2 CPU / 2 GB RAM\n"
        "2. Pro – 4 CPU / 8 GB RAM\n"
        "3. Ultra – 8 CPU / 16 GB RAM\n\n"
        "Відповідь: надішліть номер сервера для оренди."
    )
