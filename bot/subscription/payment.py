

from bot.db.client import set_subscribe, get_subscribe
from bot.service_functions import days_left

async def payment_sub(user_id, sub_type, sub_days):
    #Здесь напишите свой код для оплаты
    payment = True
    if payment:
        sub = await get_subscribe(user_id)
        if sub[0] == sub_type:
            sub_days_now = await days_left(sub[1])
            sub_days += sub_days_now
            answer = await set_subscribe(user_id, sub_type, sub_days)
        else:
            answer = await set_subscribe(user_id, sub_type, sub_days)
        return [answer, sub]
    else:
        return None