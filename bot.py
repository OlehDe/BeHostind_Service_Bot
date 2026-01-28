import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN

# Імпортуємо всі хендлери
from handlers import start, hosting, balance, support, rent, my_services

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()  # Створюємо Dispatcher

    # Підключаємо хендлери
    dp.include_router(start.router)
    dp.include_router(hosting.router)
    dp.include_router(balance.router)
    dp.include_router(support.router)
    dp.include_router(rent.router)
    dp.include_router(my_services.router)

    # Запуск поллінгу
    try:
        print("Бот запущено...")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
