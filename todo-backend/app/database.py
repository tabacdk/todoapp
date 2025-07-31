from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import (
    create_async_engine, async_sessionmaker,
    AsyncEngine, AsyncSession
)
from app.models import Base
from app.config import get_settings

settings = get_settings()
DATABASE_URL = settings.database_url

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@asynccontextmanager
async def get_session():
    async with AsyncSessionLocal() as session:
        yield session

async def close_session(session):
    await session.close()

async def get_db():
    async with get_session() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await close_session(session)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    try:
        yield
    finally:
        async with get_session() as session:
            try:
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
