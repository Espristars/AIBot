from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, BigInteger, String, Text
from config import config

Base = declarative_base()

def get_engine():
    return create_async_engine(config.DATABASE_URL, echo=False)

async_engine = get_engine()
AsyncSessionLocal = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, index=True)
    role = Column(String)
    content = Column(Text)

async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_db():
    await async_engine.dispose()

async def save_message(user_id, role, content):
    async with AsyncSessionLocal() as session:
        msg = Message(user_id=user_id, role=role, content=content)
        session.add(msg)
        await session.commit()

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