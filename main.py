from fastapi import FastAPI
from typing import Union
from pydantic import BaseModel
import json
import os
app = FastAPI(
    title="FastAPI Items API with Data store on json",
    description="A simple CRUD API for managing items with FastAPI + Json file",  
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


class ItemCreate(BaseModel):
    name : str
    description : str
    price : float
    tax : float = None

class ItemResponse(BaseModel):
    name : str
    description : str
    price : float


class ErrorResponse(BaseModel):
    error: str

list_items = []
try:
    if os.path.exists("data.json"):
        with open("data.json", "r") as f:
            list_items = json.load(f)
except json.JSONDecodeError:
    # file empty or invalid JSON
    list_items = []
    


@app.post("/item/{item_id}" , response_model=Union[ItemResponse, ErrorResponse])
def create_item(item_id: int, item: ItemCreate):
    # create new item
    # check if item already exists
    for i in list_items:
        if i["id"] == item_id:
            return {"error": f"Item {item_id} already exists"}
    
    # create new item
    new_item = {"id": item_id, **item.dict()}
    list_items.append(new_item)
    list_items.sort(key=lambda x: x["id"])

    # save to file
    with open("data.json", "w") as f:
        json.dump(list_items, f, indent=4)

    return new_item

@app.get("/item/{item_id}")
def read_item(item_id : int, q: Union[str,None] = None, limit : int = 10):
    item = next((item for item in list_items if item["id"] == item_id), None)
    if item:
        return {"item": item, "q": q, "limit": limit}
    return {"error": "Item not found"}

@app.get("/items/")
def read_items():
    return {"items": list_items}


@app.put("/item/{item_id}", response_model=Union[ItemResponse, ErrorResponse])
def update_item(item_id: int, item: ItemCreate):
    for i, existing_item in enumerate(list_items):
        if existing_item["id"] == item_id:
            list_items[i] = {"id": item_id, **item.dict()}
            list_items.sort(key=lambda x : x["id"])
            with open("data.json", "w") as f:
                 json.dump(list_items, f, indent=4)
            return item
    return {"error": f"Item {item_id} not found"}
    



@app.delete("/item/{item_id}")
def delete_item(item_id: int):
    for item in list_items:
        if item["id"] == item_id:
            list_items.remove(item)
            with open("data.json", "w") as f:
                json.dump(list_items, f, indent=4)
            return {"message": "Item deleted"}
        return {"error": "Item not found"}