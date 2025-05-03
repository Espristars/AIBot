import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import logging
from config import config
from bot.handlers import router
from bot.database import init_db, close_db

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def main():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(router)

    await init_db()

    await dp.start_polling(bot)
    await close_db()

if __name__ == '__main__':
    asyncio.run(main())
