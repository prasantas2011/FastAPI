import os
import pytest
from fastapi.testclient import TestClient
from mainwithdb import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db

TEST_DB_FILE = "test4.db"
TEST_DATABASE_URL = f"sqlite:///./{TEST_DB_FILE}"


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    # --- Before tests ---
    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)

    engine_test = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    connection = engine_test.connect()
    TestingSessionLocal = sessionmaker(bind=connection)

    # Create tables fresh
    Base.metadata.create_all(bind=connection)

    # Override get_db
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    # Provide objects to tests if needed
    yield

    # --- After tests ---
    connection.close()
    engine_test.dispose()
    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
