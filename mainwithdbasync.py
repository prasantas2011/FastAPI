from fastapi import FastAPI
from contextlib import asynccontextmanager
from databaseasync import get_db, init_db
from routers import itemsasync
#from routers import itemsasyncclassbased


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: run DB initialization
    await init_db()
    yield
    # Shutdown: add any cleanup if needed

app = FastAPI(lifespan=lifespan,
    title="FastAPI Items API",
    description="A simple CRUD API for managing items with FastAPI + SQLAlchemy Async",  
    version="1.0.0",
    contact={
        "name": "Prasanta Sahoo",
        "url": "https://github.com/prasantas2011",
        "email": "prasantakus@gmail.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Create all tables
'''
@app.on_event("startup")
async def on_startup():
    await init_db()
'''

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(itemsasync.router)
#class based
#app.include_router(itemsasyncclassbased.router)
