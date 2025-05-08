import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import logging

from config import config
from bot.handlers.handlers import router
from bot.db.database import init_db, close_db
from bot.LogMiddleware import LoggingMiddleware

logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

file_handler = logging.FileHandler("bot_updates.log", mode="a")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

async def main():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.update.middleware(LoggingMiddleware())
    dp.include_routers(router)

    await init_db()

    await dp.start_polling(bot)
    await close_db()

if __name__ == '__main__':
    asyncio.run(main())
