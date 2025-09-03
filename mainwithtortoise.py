from fastapi import FastAPI
from dbtortoise import init_db
from routers import itemstortoise


app = FastAPI()

# Initialize database start
#init_db(app)

#or below of comment below and uncomment above init_db(app)

from tortoise import Tortoise
@app.on_event("startup")
async def init_db():
    await Tortoise.init(
        db_url="sqlite://db.sqlite3",
        modules={"models": ["modelstortoise"]}
    )
    await Tortoise.generate_schemas()

# Initialize database end

app.include_router(itemstortoise.router)


@app.get("/")
async def read_root():
    return {"Hello": "World"}