from openai import AsyncOpenAI
from config import config
from bot.modes import get_mode
from bot.storage import get_history, trim_history

client = AsyncOpenAI(api_key=config.OPENAI_API_KEY)

async def generate_response(user_id):
    history = await get_history(user_id)
    history = trim_history(history)

    mode = await get_mode(user_id)
    system_prompt = {
        "friendly": "Ты дружелюбный помощник.",
        "business": "Ты деловой помощник.",
        "ironic": "Ты отвечаешь с лёгкой иронией."
    }.get(mode, "Ты дружелюбный помощник.")

    messages = [{"role": "system", "content": system_prompt}] + history
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    return response.choices[0].message.content