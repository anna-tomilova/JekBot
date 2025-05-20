import asyncio
import os
from aiogram import Bot, Dispatcher
from bot.handlers import spin
from bot.database import init_db
from bot.config_reader import config

port = int(os.environ.get("PORT", 5000))  # Default fallback port 5000
app.run(host="0.0.0.0", port=port)

async def main():
    bot = Bot(token=config.bot_token, parse_mode="HTML")
    dp = Dispatcher()
    dp.include_router(spin.router)
    await init_db()
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())
