from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from states import BuyHosting
from handlers import balance  # імпорт балансу

router = Router()

orders = {}

tariffs = {
    "Basic - 2 CPU / 2 GB RAM": 100.0,
    "Pro - 4 CPU / 8 GB RAM": 250.0,
    "Ultra - 8 CPU / 16 GB RAM": 500.0
}

# Клавіатура головного меню
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Купити хостинг"), KeyboardButton(text="Оренда хостингу")],
        [KeyboardButton(text="Мої послуги"), KeyboardButton(text="Баланс")]
    ],
    resize_keyboard=True
)

# Кнопки тарифів з кнопкою Назад
def get_tariff_buttons():
    buttons = [[KeyboardButton(text=name)] for name in tariffs.keys()]
    buttons.append([KeyboardButton(text="Назад")])
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)

# Кнопки періоду з кнопкою Назад
def get_period_buttons():
    buttons = [
        [KeyboardButton(text="1 місяць")],
        [KeyboardButton(text="3 місяці")],
        [KeyboardButton(text="6 місяців")],
        [KeyboardButton(text="12 місяців")],
        [KeyboardButton(text="Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)

# --- Обробники ---

@router.message(F.text == "Купити хостинг")
async def buy_hosting(message: Message, state: FSMContext):
    await state.set_state(BuyHosting.choose_tariff)
    await message.answer("Оберіть тариф:", reply_markup=get_tariff_buttons())

# Вибір тарифу
@router.message(BuyHosting.choose_tariff)
async def choose_tariff(message: Message, state: FSMContext):
    if message.text == "Назад":
        await state.clear()
        await message.answer("Головне меню:", reply_markup=main_menu)
        return

    if message.text not in tariffs:
        await message.answer("Невідомий тариф, спробуйте ще раз.", reply_markup=get_tariff_buttons())
        return

    await state.update_data(tariff=message.text, price=tariffs[message.text])
    await state.set_state(BuyHosting.choose_period)
    await message.answer("Оберіть період оренди:", reply_markup=get_period_buttons())

# Вибір періоду
@router.message(BuyHosting.choose_period)
async def choose_period(message: Message, state: FSMContext):
    if message.text == "Назад":
        await state.set_state(BuyHosting.choose_tariff)
        await message.answer("Оберіть тариф:", reply_markup=get_tariff_buttons())
        return

    data = await state.get_data()
    tariff = data.get("tariff")
    price = data.get("price")
    period = message.text
    await state.update_data(period=period)

    # Перевірка балансу
    user_id = message.from_user.id
    user_balance = balance.get_balance(user_id)

    if user_balance < price:
        await message.answer(
            f"На вашому балансі {user_balance:.2f} ₴. "
            f"Цього недостатньо для тарифу '{tariff}' (ціна {price:.2f} ₴).",
            reply_markup=main_menu
        )
        await state.clear()
        return

    await state.set_state(BuyHosting.confirm)
    await message.answer(
        f"Ви обрали тариф: {tariff}\n"
        f"Період оренди: {period}\n"
        f"Ціна: {price:.2f} ₴\n\n"
        f"Підтвердьте покупку (так/ні)"
    )

# Підтвердження покупки
@router.message(BuyHosting.confirm)
async def confirm_purchase(message: Message, state: FSMContext):
    if message.text.lower() == "назад":
        await state.set_state(BuyHosting.choose_period)
        await message.answer("Оберіть період оренди:", reply_markup=get_period_buttons())
        return

    data = await state.get_data()
    tariff = data.get("tariff")
    period = data.get("period")
    price = data.get("price")
    user_id = message.from_user.id

    if message.text.lower() == "так":
        user_balance = balance.get_balance(user_id)
        if user_balance < price:
            await message.answer(
                "Недостатньо коштів на балансі для покупки.",
                reply_markup=main_menu
            )
        else:
            balance.update_balance(user_id, -price)
            orders[user_id] = {"tariff": tariff, "period": period, "price": price}
            await message.answer(
                f"Покупка успішно завершена! Ваш новий баланс: {balance.get_balance(user_id):.2f} ₴",
                reply_markup=main_menu
            )
    else:
        await message.answer("Покупка скасована.", reply_markup=main_menu)

    await state.clear()
