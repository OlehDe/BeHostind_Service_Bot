from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from handlers.user_storage import users
from handlers.storage import orders
from handlers import balance
from states import RegisterUser

router = Router()

@router.message(F.text == "Мій кабінет")
async def my_account(message: Message, state: FSMContext):
    user_id = message.from_user.id

    if user_id not in users:
        await message.answer(
            "Ви ще не зареєстровані.\n"
            "Для користування кабінетом потрібно пройти реєстрацію.\n\n"
            "Введіть ваше імʼя:"
        )
        await state.set_state(RegisterUser.name)
        return

    user = users[user_id]
    user_balance = balance.get_balance(user_id)
    services_count = len(orders.get(user_id, []))

    await message.answer(
        "Ваш кабінет:\n\n"
        f"Імʼя: {user['name']}\n"
        f"Прізвище: {user['surname']}\n"
        f"Контакт: {user['contact']}\n"
        f"Банківська карта: {user['card']}\n"
        f"Баланс: {user_balance:.2f} ₴\n"
        f"Активні послуги: {services_count}"
    )

@router.message(RegisterUser.name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(RegisterUser.surname)
    await message.answer("Введіть ваше прізвище:")

@router.message(RegisterUser.surname)
async def register_surname(message: Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await state.set_state(RegisterUser.contact)
    await message.answer("Введіть контакт (телефон):")


@router.message(RegisterUser.contact)
async def register_contact(message: Message, state: FSMContext):
    phone = message.text.strip()

    if not phone.isdigit() or len(phone) != 12:
        await message.answer(
            "Невірний номер телефону.\n"
            "Він повинен містити рівно 12 цифр.\n"
            "Спробуйте ще раз:"
        )
        return

    await state.update_data(contact=phone)
    await state.set_state(RegisterUser.card)
    await message.answer(
        "Введіть номер банківської картки (16 цифр, без пробілів):"
    )

@router.message(RegisterUser.card)
async def register_card(message: Message, state: FSMContext):
    card = message.text.strip()

    if not card.isdigit() or len(card) != 16:
        await message.answer(
            "Невірний номер картки.\n"
            "Він повинен містити рівно 16 цифр.\n"
            "Спробуйте ще раз:"
        )
        return

    data = await state.get_data()
    user_id = message.from_user.id

    users[user_id] = {
        "name": data["name"],
        "surname": data["surname"],
        "contact": data["contact"],
        "card": card
    }

    await state.clear()

    await message.answer(
        "Реєстрація успішно завершена.\n\n"
     
        "Тепер вам доступний Мій кабінет."
    )