import pytest
from fastapi.testclient import TestClient
from mainwithdb import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db

# In-memory SQLite with shared connection
TEST_DATABASE_URL = "sqlite:///:memory:"
engine_test = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Single connection
connection = engine_test.connect()
TestingSessionLocal = sessionmaker(bind=connection)

# Create tables on this connection
Base.metadata.create_all(bind=connection)

# Override get_db
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
