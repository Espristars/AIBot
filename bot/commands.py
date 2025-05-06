from aiogram.types import Message
from bot.message import clear_history
from bot.modes import toggle_mode
from bot.client import save_client
from bot.keyboards import change_model

async def handle_start(msg: Message):
    await save_client(user_id=msg.from_user.id,username=msg.from_user.username)
    await clear_history(msg.from_user.id)
    await msg.answer("Привет, я ИИ-бот. И я почти живой")

async def handle_help(msg: Message):
    await msg.answer("Список команд: /start, /help, /reset, /about, /mode, /voice")

async def handle_reset(msg: Message):
    await clear_history(msg.from_user.id)
    await msg.answer("Контекст очищен.")

async def handle_about(msg: Message):
    await msg.answer("Я использую GPT-4o-mini и Whisper для общения и распознавания речи. Обращайся ко мне с любым вопросом!")

async def handle_mode(msg: Message):
    mode = await toggle_mode(msg.from_user.id)
    await msg.answer(f"Режим общения переключён на: {mode}")
    await msg.delete()

async def handle_model(msg: Message):
    await msg.answer(f"Выбери модель:", reply_markup=change_model())
    await msg.delete()