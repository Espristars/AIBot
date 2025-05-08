import re
from datetime import datetime, timezone
import math


async def exsuf_model(text):
    match = re.search(r'model_(\w+)', text)
    if match:
        return match.group(1)
    return None


async def exsuf_sub(text):
    match = re.search(r'sub_(\w+)_(\w+)', text)
    if match:
        return [match.group(1), match.group(2)]
    return None


async def escape_md(text: str) -> str:
    escape_chars = r"_*[]()~`>#+-=|{}.!"
    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)


async def days_left(subscription_end_date):
    now = datetime.now(timezone.utc)
    delta = subscription_end_date - now
    days = math.ceil(delta.total_seconds() / 86400)
    return max(days, 0)