import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import logging
from config import config
from bot.handlers import router
from bot.database import init_db, close_db
from bot.LogMiddleware import LogMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    filename="bot_updates.log",
    filemode="a"
)

async def main():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.update.middleware(LogMiddleware)
    dp.include_routers(router)

    await init_db()

    await dp.start_polling(bot)
    await close_db()

if __name__ == '__main__':
    asyncio.run(main())
