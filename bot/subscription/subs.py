

subs = {
    "start": ["gpt-4o-mini"],
    "lite": ["gpt-4o-mini", "gpt-4.1"],
    "pro":["gpt-4o-mini", "gpt-4.1", "o1-mini", "o3-mini"]
}

async def subs_check(sub_type_now, sub_type_before):
    level = {'start': 0, 'lite': 1, 'pro': 2}
    return level[sub_type_now] - level[sub_type_before]