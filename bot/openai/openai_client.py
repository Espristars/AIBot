from openai import AsyncOpenAI

from config import config
from bot.db.message import get_history, trim_history
from bot.db.client import get_mode

client = AsyncOpenAI(api_key=config.OPENAI_API_KEY)

async def generate_response(user_id, model):
    history = await get_history(user_id)
    history = trim_history(history)

    mode = await get_mode(user_id)
    system_prompt = {
        "friendly": "Ты дружелюбный помощник.",
        "business": "Ты деловой помощник.",
        "ironic": "Ты отвечаешь с лёгкой иронией.",
        "bullying": "Ты отвечаешь с сильным издевательством"
    }.get(mode, "Ты дружелюбный помощник.")

    messages = [{"role": "system", "content": system_prompt}] + history
    response = await client.chat.completions.create(
        model=model,
        messages=messages
    )
    messages = await split_message(response.choices[0].message.content)
    return messages

async def split_message(message:str):
    max_length = 4000
    messages = []
    current_message = ""
    for line in message.split("\n"):
        if len(current_message) + len(line) + 1 <= max_length:
            current_message += line + "\n"
        else:
            messages.append(current_message.strip())
            current_message = line + "\n"

    if current_message.strip():
        messages.append(current_message.strip())
    return messages