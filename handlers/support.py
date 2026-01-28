from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text == "Підтримка")
async def support(message: Message):
    await message.answer(
        "Опишіть вашу проблему, і адміністратор скоро відповість."
    )
