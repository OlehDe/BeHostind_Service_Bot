from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

router = Router()

ADMIN_ID = 1182819676

class SupportState(StatesGroup):
    waiting_message = State()

@router.message(F.text == "Підтримка")
async def support_start(message: Message, state: FSMContext):
    await message.answer(
        "Опишіть вашу проблему одним повідомленням.\n"
        "Ми передамо її адміністратору."
    )
    await state.set_state(SupportState.waiting_message)

@router.message(SupportState.waiting_message)
async def support_message(message: Message, state: FSMContext):
    user = message.from_user

    text_for_admin = (
        "Нове повідомлення в підтримку:\n\n"
        f"Від: {user.full_name}\n"
        f"Username: @{user.username if user.username else 'немає'}\n"
        f"User ID: {user.id}\n\n"
        f"Повідомлення:\n{message.text}"
    )

    await message.bot.send_message(ADMIN_ID, text_for_admin)

    await message.answer(
        "Ваше повідомлення надіслано в підтримку.\n"
        "Відповідь надійде протягом 24 годин."
    )

    await state.clear()
