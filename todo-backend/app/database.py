from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
# from sqlalchemy.orm import sessionmaker
from app.models import Base

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

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
        # Forsøg at commit og lukke session, hvis der er en åben
        async with get_session() as session:
            try:
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
