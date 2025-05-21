import asyncio
import signal
from aiogram import Bot, Dispatcher
from bot.handlers import spin, start, balance
from bot.database import init_db
from bot.config_reader import config

async def main():
    bot = Bot(token=config.bot_token, parse_mode="HTML")
    dp = Dispatcher()

    dp.include_router(spin.router)
    dp.include_router(start.router)
    dp.include_router(balance.router)

    await init_db()

    # Run polling in a separate task
    polling_task = asyncio.create_task(dp.start_polling(bot))

    # Create an event to wait on shutdown signal
    shutdown_event = asyncio.Event()

    def shutdown_handler():
        print("Shutdown signal received. Stopping polling...")
        shutdown_event.set()

    # Register signal handlers for SIGINT and SIGTERM
    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGINT, shutdown_handler)
    loop.add_signal_handler(signal.SIGTERM, shutdown_handler)

    # Wait until shutdown signal
    await shutdown_event.wait()

    # Gracefully stop polling
    await dp.stop_polling()
    await polling_task

    # Close bot session properly
    await bot.session.close()
    print("Bot stopped cleanly.")

if __name__ == "__main__":
    asyncio.run(main())
