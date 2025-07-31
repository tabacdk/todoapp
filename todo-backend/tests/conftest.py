# tests/conftest.py
import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app
from app.database import async_session_maker, init_db, AsyncSession
from app import config

@pytest.fixture(scope="session", autouse=True)
def override_settings():
    config.get_settings.cache_clear()
    config.get_settings(".env.pytest")

@pytest.fixture(autouse=True, scope="module")
async def setup_database():
    await init_db()
    yield

@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.fixture
async def session() -> AsyncSession:
    async with async_session_maker() as s:
        yield s
