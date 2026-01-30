import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN

from handlers import start, hosting, balance, support, profile, my_services

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(hosting.router)
    dp.include_router(balance.router)
    dp.include_router(support.router)
    dp.include_router(profile.router)
    dp.include_router(my_services.router)

    try:
        print("Бот запущено...")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
