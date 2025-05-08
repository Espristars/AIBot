from aiogram.types import CallbackQuery

from bot.service_functions import exsuf_model, exsuf_sub
from bot.db.ai_models import set_model, models
from bot.subscription.payment import payment_sub
from bot.db.client import get_subscribe
from bot.subscription.subs import subs_check, subs

async def call_model(call: CallbackQuery):
    message = call.message
    chat_id = message.chat.id
    msg = await exsuf_model(call.data)
    sub = await get_subscribe(chat_id)
    if sub is None:
        await call.answer(f"Пустой ответ")
        return
    if models[msg] not in subs[sub[0]]:
        await call.answer(f"Вам недоступна эта модель. Купите подписку для получения новых моделей.")
    else:
        answer = await set_model(chat_id, msg)
        if answer:
            await call.answer(f"Модель ИИ изменена на {answer}")
        else:
            await call.answer(f"У вас уже выбрана эта модель")
    await call.message.delete()

async def call_subscription(call: CallbackQuery):
    message = call.message
    chat_id = message.chat.id
    msg = await exsuf_sub(call.data)
    sub = await get_subscribe(chat_id)
    if await subs_check(sub[0], msg[0]) < 0:
        await call.answer(f"Вы не можете купить подписку ниже вашей.")
    else:
        answer = await payment_sub(chat_id, msg[0], int(msg[1]))
        if answer:
            if msg[0] == answer[1]:
                await call.answer(f"Отлично! Ваша подписка {answer[1]} продлена до {answer[0]}.")
            else:
                await call.answer(f"Отлично! Вам выдана подписка {answer[1]} до {answer[0]}")
        else:
            await call.answer(f"Ошибка оплаты")
    await call.message.delete()