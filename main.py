import asyncio
from aiogram import Bot, Dispatcher
from bot.handlers import spin
from bot.database import init_db
from bot.config_reader import config

async def main():
    # Инициализируем бота и диспетчер
    bot = Bot(token=config.bot_token, parse_mode="HTML")
    dp = Dispatcher()

    # Подключаем роутеры
    dp.include_router(spin.router)
    dp.include_router(start.router)
    await init_db()

    # Запуск бота в режиме long polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
