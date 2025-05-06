from sqlalchemy.exc import IntegrityError
from bot.models import Base, Clients
from bot.database import AsyncSessionLocal

async def save_client(user_id, username):
    if await check_client(user_id):
        async with AsyncSessionLocal() as session:
            client = Clients(user_id=user_id, username=username, model="gpt-4o-mini")
            session.add(client)
            try:
                await session.commit()
                await session.refresh(client)
            except IntegrityError:
                await session.rollback()
                raise

async def check_client(user_id):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            Base.metadata.tables['clients'].select().where(Clients.user_id == user_id)
        )
        existing = result.scalar()
        if existing:
            return False
    return True