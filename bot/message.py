from sqlalchemy.exc import IntegrityError
from config import config
from bot.models import Base, Message
from bot.database import AsyncSessionLocal

async def save_message(user_id, role, contents):
    async with AsyncSessionLocal() as session:
        content = ""
        for con in contents:
            content += con
        msg = Message(user_id=user_id, role=role, content=content)
        session.add(msg)
        try:
            await session.commit()
            await session.refresh(msg)
        except IntegrityError:
            await session.rollback()
            raise

async def get_history(user_id):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            Base.metadata.tables['messages'].select().where(Message.user_id==user_id).order_by(Message.id)
        )
        rows = result.fetchall()
    return [{"role": r.role, "content": r.content} for r in rows]

async def clear_history(user_id):
    async with AsyncSessionLocal() as session:
        await session.execute(
            Base.metadata.tables['messages'].delete().where(Message.user_id==user_id)
        )
        await session.commit()

def trim_history(history):
    if len(history) > config.MAX_HISTORY:
        return history[-config.MAX_HISTORY:]
    return history