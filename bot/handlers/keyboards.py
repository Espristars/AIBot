from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

def change_model():
    model1 = types.InlineKeyboardButton(text='GPT-4o', callback_data="model_gpt_4o")
    model2 = types.InlineKeyboardButton(text='GPT-1o', callback_data="model_gpt_1o")
    model3 = types.InlineKeyboardButton(text='GPT-3o', callback_data="model_gpt_3o")
    model4 = types.InlineKeyboardButton(text='GPT-4o-turbo', callback_data="model_gpt_4o_turbo")

    markup = InlineKeyboardBuilder()
    markup.row(model1)
    markup.row(model2)
    markup.row(model3)
    markup.row(model4)

    return markup.as_markup()

def change_subscription():
    sub1 = types.InlineKeyboardButton(text='Подписка Pro на месяц', callback_data="sub_pro_30")
    sub2 = types.InlineKeyboardButton(text='Подписка Lite на месяц', callback_data="sub_lite_30")

    markup = InlineKeyboardBuilder()
    markup.row(sub1)
    markup.row(sub2)

    return markup.as_markup()