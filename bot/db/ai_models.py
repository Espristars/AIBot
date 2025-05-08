from sqlalchemy import update, select

from bot.db.models import Clients
from bot.db.database import AsyncSessionLocal

models = {
    "gpt_4o": "gpt-4o-mini",
    "gpt_1o": "o1-mini",
    "gpt_3o": "o3-mini",
    "gpt_4o_turbo": "gpt-4.1"
}

async def set_model(user_id: int, model: str):
    async with AsyncSessionLocal() as session:
        last_model = await get_model(user_id)
        model = models.get(model)
        if last_model == model:
            return None
        else:
            try:
                await session.execute(
                    update(Clients).where(Clients.user_id == user_id).values(last_model=model).execution_options(synchronize_session="fetch")
                )
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
            return model

async def get_model(user_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Clients).where(Clients.user_id == user_id)
        )
        client = result.scalar_one_or_none()
        if client is None:
            return None
        return client.last_model

