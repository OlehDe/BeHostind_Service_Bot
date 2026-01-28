from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from keyboards import main_kb

router = Router()

@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "Вітаю у хостинг-боті!\nОберіть дію:",
        reply_markup=main_kb
    )
