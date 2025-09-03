import pytest_asyncio
from tortoise import Tortoise
from httpx import AsyncClient, ASGITransport
import modelstortoise
from mainwithtortoise import app

TEST_DB_URL = "sqlite://:memory:"  # in-memory DB for tests

# Use async fixture for Tortoise initialization
@pytest_asyncio.fixture(scope="session", autouse=True)
async def init_tortoise():
    await Tortoise.init(
        db_url=TEST_DB_URL,
        modules={"models": ["modelstortoise"]},  # your models
        _create_db=True  # auto-create DB if needed
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()

# Async test client fixture
@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
