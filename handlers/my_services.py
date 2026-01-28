from aiogram import Router, F
from aiogram.types import Message
from handlers.storage import orders
from handlers import balance

router = Router()

CANCEL_FEE = 50.0  # штраф за скасування


@router.message(F.text == "Мої послуги")
async def my_services(message: Message):
    user_id = message.from_user.id

    if user_id not in orders or not orders[user_id]:
        await message.answer(
            "У вас поки немає активних послуг.\n\n"
            "Ви можете придбати хостинг у головному меню."
        )
        return

    text = "Ваші активні послуги:\n\n"

    for i, service in enumerate(orders[user_id], start=1):
        text += (
            f"{i}. Тариф: {service['tariff']}\n"
            f"   Період: {service['period']}\n"
            f"   Ціна: {service['price']:.2f} ₴\n\n"
        )

    text += (
        "Щоб скасувати послугу, напишіть:\n"
        "Скасувати <номер>\n\n"
        "Приклад: Скасувати 1\n"
        f"Штраф за скасування: {CANCEL_FEE:.2f} ₴"
    )

    await message.answer(text)


@router.message(F.text.startswith("Скасувати"))
async def cancel_service(message: Message):
    user_id = message.from_user.id

    if user_id not in orders or not orders[user_id]:
        await message.answer("У вас немає активних послуг для скасування.")
        return

    parts = message.text.split()

    if len(parts) != 2 or not parts[1].isdigit():
        await message.answer("Неправильний формат. Використовуйте: Скасувати 1")
        return

    index = int(parts[1]) - 1

    if index < 0 or index >= len(orders[user_id]):
        await message.answer("Послуги з таким номером не існує.")
        return

    service = orders[user_id].pop(index)

    refund = service["price"] - CANCEL_FEE
    if refund < 0:
        refund = 0.0

    balance.update_balance(user_id, refund)

    await message.answer(
        "Послугу успішно скасовано.\n\n"
        f"Тариф: {service['tariff']}\n"
        f"Повернуто коштів: {refund:.2f} ₴\n"
        f"Штраф: {CANCEL_FEE:.2f} ₴\n\n"
        f"Ваш новий баланс: {balance.get_balance(user_id):.2f} ₴"
    )

    # Якщо послуг більше немає — видаляємо користувача зі сховища
    if not orders[user_id]:
        del orders[user_id]
