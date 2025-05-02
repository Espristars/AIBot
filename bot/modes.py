_modes = {}
async def toggle_mode(user_id):
    current = _modes.get(user_id, "friendly")
    new = {"friendly": "business", "business": "ironic", "ironic": "friendly"}[current]
    _modes[user_id] = new
    return new

async def get_mode(user_id):
    return _modes.get(user_id, "friendly")