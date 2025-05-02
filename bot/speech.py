from openai import AsyncOpenAI
import aiohttp
import tempfile
import os
from config import config
from aiogram.types import Message

client = AsyncOpenAI(api_key=config.OPENAI_API_KEY)

async def transcribe_voice(msg: Message) -> str:
    file = await msg.bot.get_file(msg.voice.file_id)
    url = f"https://api.telegram.org/file/bot{config.BOT_TOKEN}/{file.file_path}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            audio_bytes = await resp.read()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as temp_file:
        temp_file.write(audio_bytes)
        temp_file_path = temp_file.name

    try:
        with open(temp_file_path, "rb") as audio_file:
            transcription = await client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )
        return transcription
    finally:
        os.remove(temp_file_path)