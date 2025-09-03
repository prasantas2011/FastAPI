# tests/conftest.py
import os
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from databaseasync import Base, get_db
from mainwithdbasync import app

# Test DB file
TEST_DB_FILE = "test2.db"
TEST_DATABASE_URL = f"sqlite+aiosqlite:///./{TEST_DB_FILE}"

engine_test = create_async_engine(TEST_DATABASE_URL, future=True, echo=False)
TestingSessionLocal = sessionmaker(
    engine_test, expire_on_commit=False, class_=AsyncSession
)

# Override get_db for testing
async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db


# Ensure DB is fresh for this test session
@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db():
    # Remove old DB file if exists
    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)

    # Create tables
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    # Drop tables when tests finish
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

     # Delete DB file after all tests
    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)
        
# Async test client
@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
