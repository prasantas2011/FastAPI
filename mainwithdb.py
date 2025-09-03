from fastapi import FastAPI
from database import Base, engine
from routers import items

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI Items API",
    description="A simple CRUD API for managing items with FastAPI + SQLAlchemy",  
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


@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(items.router)


