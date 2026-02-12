from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import  DeclarativeBase

from typing import AsyncGenerator
from src.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=True)

class Base(DeclarativeBase):
    pass

# В dependencies
async def get_db() -> AsyncGenerator:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def setup_database():
    import src.featureWeather.repository.models
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("База данных создана")
    return {"ok": True}

