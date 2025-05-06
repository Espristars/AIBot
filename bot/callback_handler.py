from aiogram.types import CallbackQuery
from bot.service_functions import exsuf
from bot.ai_models import set_model

async def call_model(call: CallbackQuery):
    message = call.message
    chat_id = message.chat.id
    msg = exsuf(call.data)
    answer = await set_model(chat_id, msg)
    if answer:
        await call.answer(f"Модель ИИ изменена на {answer}")
    else:
        await call.answer(f"У вас уже выбрана эта модель")