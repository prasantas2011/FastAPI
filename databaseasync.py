from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite+aiosqlite:///./testasync.db"

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Create async session
AsyncSessionLocal = sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

Base = declarative_base()

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
# Dependency
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
