from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from bot.commands import handle_start, handle_help, handle_reset, handle_about, handle_mode
from bot.openai_client import generate_response
from bot.speech import transcribe_voice
from bot.storage import save_message

router = Router()

router.message.register(handle_start, Command("start"))
router.message.register(handle_help, Command("help"))
router.message.register(handle_reset, Command("reset"))
router.message.register(handle_about, Command("about"))
router.message.register(handle_mode, Command("mode"))

@router.message(F.voice)
async def handle_voice(msg: Message):
    text = await transcribe_voice(msg)
    await save_message(msg.from_user.id, "user", text)
    response = await generate_response(msg.from_user.id)
    await msg.answer(response, parse_mode="Markdown")
    await save_message(msg.from_user.id, "assistant", response)

@router.message(F.text)
async def handle_text(msg: Message):
    await save_message(msg.from_user.id, "user", msg.text)
    response = await generate_response(msg.from_user.id)
    await msg.answer(response, parse_mode="Markdown")
    await save_message(msg.from_user.id, "assistant", response)
