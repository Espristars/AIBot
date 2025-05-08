from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from datetime import datetime, timedelta

from bot.db.models import Base, Clients
from bot.db.database import AsyncSessionLocal
from bot.modes import modes

async def save_client(user_id, username):
    if await check_client(user_id):
        async with AsyncSessionLocal() as session:
            client = Clients(user_id=user_id, username=username, last_model="gpt-4o-mini")
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

async def toggle_mode(user_id, mode):
    if mode == await get_mode(user_id):
        return "Yet"
    if mode not in modes:
        return "No way"
    async with AsyncSessionLocal() as session:
        await session.execute(
            Base.metadata.tables['clients'].update().where(Clients.user_id == user_id).values(last_mode=mode)
        )
        try:
            await session.commit()
            return "Yes"
        except IntegrityError:
            await session.rollback()
            raise

async def get_mode(user_id):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Clients).where(Clients.user_id == user_id)
        )
        client = result.scalar_one_or_none()
    return client.last_mode

async def set_subscribe(user_id, sub_type, sub_days):
    async with AsyncSessionLocal() as session:
        sub_date = datetime.now() + timedelta(days=sub_days)

        try:
            result = await session.execute(
                select(Clients).where(Clients.user_id == user_id)
            )
            client = result.scalar_one_or_none()
            if not client:
                raise

            client.subscription_type = sub_type
            client.subscription_end_date = sub_date

            await session.commit()
            await session.refresh(client)
            return client.subscription_end_date
        except IntegrityError:
            await session.rollback()
            raise

async def get_subscribe(user_id):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            Base.metadata.tables['clients'].select().where(Clients.user_id == user_id)
        )
        client = result.scalar()
    return [client.subscription_type, client.subscription_end_date]