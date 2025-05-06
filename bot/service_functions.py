import re

def exsuf(text):
    match = re.search(r'model_(\w+)', text)
    if match:
        return match.group(1)
    return None

def escape_md(text: str) -> str:
    # Экранирование всех символов MarkdownV2
    escape_chars = r"_*[]()~`>#+-=|{}.!"
    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)