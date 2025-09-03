import pytest_asyncio
from tortoise import Tortoise
from httpx import AsyncClient, ASGITransport
import modelstortoise
from mainwithtortoise import app
import os

TEST_DB_FILE = "test3.db"
TEST_DB_URL = f"sqlite://./{TEST_DB_FILE}"

@pytest_asyncio.fixture(scope="session", autouse=True)
async def init_tortoise():
    # Remove old DB file if exists
    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)

    # Init new DB
    await Tortoise.init(
        db_url=TEST_DB_URL,
        modules={"models": ["modelstortoise"]},
        _create_db=True
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()

     # Delete DB file after all tests
    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)

# Async test client fixture
@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
