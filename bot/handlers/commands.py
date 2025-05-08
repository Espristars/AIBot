from aiogram.types import Message

from bot.db.message import clear_history
from bot.db.client import toggle_mode, save_client
from bot.handlers.keyboards import change_model, change_subscription

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
    mode = msg.text.split()[-1]
    if mode:
        answer = await toggle_mode(msg.from_user.id, mode)
        if answer == "Yes":
            await msg.answer(f"Режим общения переключён на {mode}")
        elif answer == "No way":
            await msg.answer(f"Доступные режимы: friendly, business, ironic, bullying")
        else:
            await msg.answer(f"Режим общения уже установлен на {mode}")
    else:
        await msg.answer(f"Напишите режим общения после команды (через пробел).\n Доступные режимы: friendly, business, ironic, bullying")
    await msg.delete()

async def handle_model(msg: Message):
    await msg.answer(f"Выбери модель:", reply_markup=change_model())
    await msg.delete()

async def buy_subscription(msg: Message):
    await msg.answer(f"Выбери подписку:", reply_markup=change_subscription())
    await msg.delete()