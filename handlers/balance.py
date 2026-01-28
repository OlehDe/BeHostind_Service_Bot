from aiogram import Router, F
from aiogram.types import Message

router = Router()

# Тимчасова база балансів користувачів
balances = {
    # user_id: баланс
    # для тесту можна додати будь-який id
    1182819676: 500.0  # користувач з 500 ₴
}

def get_balance(user_id: int) -> float:
    """Повертає баланс користувача"""
    return balances.get(user_id, 0.0)

def update_balance(user_id: int, amount: float):
    """Змінює баланс користувача на amount (може бути від'ємне значення)"""
    current = balances.get(user_id, 0.0)
    balances[user_id] = current + amount

@router.message(F.text == "Баланс")
async def show_balance(message: Message):
    user_id = message.from_user.id
    print("Ваш user_id:", user_id)  # додай це для перевірки
    bal = get_balance(user_id)
    await message.answer(f"Ваш баланс: {bal:.2f} ₴")
