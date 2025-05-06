from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from bot.commands import handle_start, handle_help, handle_reset, handle_about, handle_mode, handle_model
from bot.openai_client import generate_response
from bot.speech import transcribe_voice
from bot.message import save_message
from bot.callback_handler import call_model
from bot.ai_models import get_model
from bot.service_functions import escape_md

router = Router()

router.message.register(handle_start, Command("start"))
router.message.register(handle_help, Command("help"))
router.message.register(handle_reset, Command("reset"))
router.message.register(handle_about, Command("about"))
router.message.register(handle_mode, Command("mode"))
router.message.register(handle_model, Command("model"))
router.callback_query.register(call_model, lambda call: call.data.startswith("model_"))

@router.message(F.voice)
async def handle_voice(msg: Message):
    text = await transcribe_voice(msg)
    model = await get_model(msg.from_user.id)
    await save_message(msg.from_user.id, "user", text)
    responses = await generate_response(msg.from_user.id, model)
    for response in responses:
        response = escape_md(response)
        await msg.answer(response, parse_mode="MarkdownV2")
    await save_message(msg.from_user.id, "assistant", responses)

@router.message(F.text)
async def handle_text(msg: Message):
    model = await get_model(msg.from_user.id)
    await save_message(msg.from_user.id, "user", msg.text)
    responses = await generate_response(msg.from_user.id, model)
    for response in responses:
        response = escape_md(response)
        await msg.answer(response, parse_mode="MarkdownV2")
    await save_message(msg.from_user.id, "assistant", responses)
