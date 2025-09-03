from fastapi import FastAPI
from dbtortoise import init_db
from routers import itemstortoise


# Initialize database start
# app = FastAPI()
# init_db(app)

#or below of comment below and uncomment above init_db(app)

from tortoise import Tortoise
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize Tortoise
    await Tortoise.init(
        db_url="sqlite://db.sqlite3",
        modules={"models": ["modelstortoise"]}
    )
    await Tortoise.generate_schemas()
    yield
    # Shutdown: close connections
    await Tortoise.close_connections()
# Initialize database end

app = FastAPI(lifespan=lifespan)

app.include_router(itemstortoise.router)


@app.get("/")
async def read_root():
    return {"Hello": "World"}