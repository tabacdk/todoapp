# app/database.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import (
    create_async_engine, async_sessionmaker,
    AsyncEngine, AsyncSession
)
from app.models import Base
from app.config import get_settings

engine: AsyncEngine | None = None
async_session_maker: async_sessionmaker[AsyncSession] | None = None

# Bruges i f.eks. tests til at overskrive databasen
def configure_engine(database_url: str, echo: bool = False):
    global engine, async_session_maker
    engine = create_async_engine(database_url, echo=echo)
    async_session_maker = async_sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

if engine is None or async_session_maker is None:
    settings = get_settings()
    configure_engine(settings.database_url, echo=True)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    async with async_session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
