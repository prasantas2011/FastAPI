from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Database URL (change as needed: mysql, postgresql, sqlite, etc.)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
# Example for PostgreSQL: "postgresql://user:password@localhost/dbname"
# Example for MySQL: "mysql+pymysql://user:password@localhost/dbname"

# Create engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}  # only for SQLite
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
