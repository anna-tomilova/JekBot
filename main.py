import asyncio
from aiogram import Bot, Dispatcher
from bot.handlers import spin, start, balance
from bot.database import init_db
from bot.config_reader import config

# Временное решение — удалить таблицу и пересоздать
from bot.models import Base
from bot.database import engine

async def recreate_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
# Временное решение — удалить таблицу и пересоздать

async def main():
    # Инициализируем бота и диспетчер
    bot = Bot(token=config.bot_token, parse_mode="HTML")
    dp = Dispatcher()

    # Подключаем роутеры
    dp.include_router(spin.router)
    dp.include_router(start.router)
    dp.include_router(balance.router)
    await init_db()

    # Запуск бота в режиме long polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
