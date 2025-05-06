import re

def exsuf(text):
    match = re.search(r'model_(\w+)', text)
    if match:
        return match.group(1)
    return None