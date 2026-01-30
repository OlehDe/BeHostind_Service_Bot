from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from states import BuyHosting
from handlers import balance
from handlers.storage import orders
from keyboards import main_kb

router = Router()

tariffs = {
    "Basic - 2 CPU / 2 GB RAM": 100.0,
    "Pro - 4 CPU / 8 GB RAM": 250.0,
    "Ultra - 8 CPU / 16 GB RAM": 500.0
}

period_prices = {
    "1 місяць": 50.0,
    "3 місяці": 100.0,
    "6 місяців": 190.0,
    "12 місяців": 350.0
}

def get_tariff_buttons():
    buttons = [[KeyboardButton(text=name)] for name in tariffs.keys()]
    buttons.append([KeyboardButton(text="Назад")])
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=True
    )

def get_period_buttons():
    buttons = [[KeyboardButton(text=name)] for name in period_prices.keys()]
    buttons.append([KeyboardButton(text="Назад")])
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=True
    )

@router.message(F.text == "Купити хостинг")
async def buy_hosting(message: Message, state: FSMContext):
    await state.set_state(BuyHosting.choose_tariff)
    await message.answer("Оберіть тариф:", reply_markup=get_tariff_buttons())

@router.message(BuyHosting.choose_tariff)
async def choose_tariff(message: Message, state: FSMContext):
    if message.text == "Назад":
        await state.clear()
        await message.answer("Головне меню:", reply_markup=main_kb)
        return

    if message.text not in tariffs:
        await message.answer(
            "Невідомий тариф.",
            reply_markup=get_tariff_buttons()
        )
        return

    await state.update_data(
        tariff=message.text,
        tariff_price=tariffs[message.text]
    )

    await state.set_state(BuyHosting.choose_period)
    await message.answer("Оберіть період:", reply_markup=get_period_buttons())

@router.message(BuyHosting.choose_period)
async def choose_period(message: Message, state: FSMContext):
    if message.text == "Назад":
        await state.set_state(BuyHosting.choose_tariff)
        await message.answer("Оберіть тариф:", reply_markup=get_tariff_buttons())
        return

    if message.text not in period_prices:
        await message.answer(
            "Невідомий період.",
            reply_markup=get_period_buttons()
        )
        return

    data = await state.get_data()
    tariff = data["tariff"]
    tariff_price = data["tariff_price"]
    period = message.text
    period_price = period_prices[period]

    total_price = tariff_price + period_price

    user_id = message.from_user.id
    user_balance = balance.get_balance(user_id)

    if user_balance < total_price:
        await message.answer(
            f"Баланс: {user_balance:.2f} ₴\n"
            f"Вартість: {total_price:.2f} ₴\n"
            f"Недостатньо коштів.",
            reply_markup=main_kb
        )
        await state.clear()
        return

    await state.update_data(
        period=period,
        total_price=total_price
    )

    await state.set_state(BuyHosting.confirm)
    await message.answer(
        f"Тариф: {tariff}\n"
        f"Період: {period}\n"
        f"Ціна тарифу: {tariff_price:.2f} ₴\n"
        f"Ціна періоду: {period_price:.2f} ₴\n"
        f"Загальна ціна: {total_price:.2f} ₴\n\n"
        f"Підтвердити покупку? (так/ні)"
    )

@router.message(BuyHosting.confirm)
async def confirm_purchase(message: Message, state: FSMContext):
    if message.text.lower() == "назад":
        await state.set_state(BuyHosting.choose_period)
        await message.answer("Оберіть період:", reply_markup=get_period_buttons())
        return

    data = await state.get_data()
    tariff = data["tariff"]
    period = data["period"]
    total_price = data["total_price"]
    user_id = message.from_user.id

    if message.text.lower() == "так":
        if balance.get_balance(user_id) < total_price:
            await message.answer(
                "Недостатньо коштів.",
                reply_markup=main_kb
            )
        else:
            balance.update_balance(user_id, -total_price)
            if user_id not in orders:
                orders[user_id] = []

            orders[user_id].append({
                "tariff": tariff,
                "period": period,
                "price": total_price
            })

            await message.answer(
                f"Покупка успішна.\n"
                f"Новий баланс: {balance.get_balance(user_id):.2f} ₴",
                reply_markup=main_kb
            )
    else:
        await message.answer("Покупка скасована.", reply_markup=main_kb)

    await state.clear()
