from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from bot.models import Base
from bot.config_reader import config

engine = create_async_engine(config.database_url, echo=False)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
