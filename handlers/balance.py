from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

router = Router()

# ------------------ FSM ------------------

class TopUpBalance(StatesGroup):
    enter_amount = State()

# ------------------ Дані ------------------

balances = {
    1182819676: 500.0
}

# ------------------ Клавіатури ------------------

balance_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Поповнити баланс")],
        [KeyboardButton(text="Назад")]
    ],
    resize_keyboard=True
)

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Купити хостинг"), KeyboardButton(text="Оренда хостингу")],
        [KeyboardButton(text="Мої послуги"), KeyboardButton(text="Баланс")]
    ],
    resize_keyboard=True
)

# ------------------ Функції ------------------

def get_balance(user_id: int) -> float:
    return balances.get(user_id, 0.0)

def update_balance(user_id: int, amount: float):
    balances[user_id] = get_balance(user_id) + amount

# ------------------ Обробники ------------------

@router.message(F.text == "Баланс")
async def show_balance(message: Message):
    user_id = message.from_user.id
    bal = get_balance(user_id)
    await message.answer(
        f"Ваш баланс: {bal:.2f} ₴",
        reply_markup=balance_menu
    )

@router.message(F.text == "Поповнити баланс")
async def start_topup(message: Message, state: FSMContext):
    await state.set_state(TopUpBalance.enter_amount)
    await message.answer(
        "Введіть суму поповнення (число):",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Назад")]],
            resize_keyboard=True
        )
    )

@router.message(TopUpBalance.enter_amount)
async def process_topup(message: Message, state: FSMContext):
    if message.text == "Назад":
        await state.clear()
        await message.answer("Головне меню:", reply_markup=main_menu)
        return

    try:
        amount = float(message.text)
        if amount <= 0:
            raise ValueError
    except ValueError:
        await message.answer("Введіть коректну суму (наприклад 100).")
        return

    user_id = message.from_user.id
    update_balance(user_id, amount)

    await message.answer(
        f"Баланс успішно поповнено на {amount:.2f} ₴\n"
        f"Новий баланс: {get_balance(user_id):.2f} ₴",
        reply_markup=main_menu
    )

    await state.clear()

@router.message(F.text == "Назад")
async def back_to_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Головне меню:", reply_markup=main_menu)
