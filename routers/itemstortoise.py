from fastapi import APIRouter, Depends, HTTPException, Body, status
from modelstortoise import Item
import schema

router = APIRouter(
    prefix="/items",
    tags=["items"],  # ✅ Swagger groups these endpoints
)

@router.post("/" , response_model=schema.ItemResponse,status_code=status.HTTP_201_CREATED)
async def create_item(item: schema.ItemCreate):
    obj = await Item.create(**item.dict())
    return obj

@router.get("/{item_id}", response_model=schema.ItemResponse, status_code=status.HTTP_200_OK)
async def read_item(item_id: int):
    item = await Item.get_or_none(id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found"
        )
    
    return item

@router.get("/",status_code=status.HTTP_200_OK)
async def read_items():
    items = await Item.all()
    return items

@router.put("/{item_id}", response_model=schema.ItemResponse,status_code=status.HTTP_200_OK)
async def update_item(item_id: int, item: schema.ItemCreate = Body(
        ...,
        example={
            "name": "Updated Phone",
            "description": "Latest model with 5G",
            "price": 999.99,
            "tax": 10.0
        },
    )):
    db_item = await Item.get_or_none(id=item_id)

    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found"
        )
    
    for key, value in item.dict().items():
        setattr(db_item, key, value)
    await db_item.save()
    return db_item

@router.delete("/{item_id}",status_code=status.HTTP_200_OK)
async def delete_item(item_id: int):
    db_item = await Item.get_or_none(id=item_id)
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found"
        )

    await db_item.delete()
    return f"Item {item_id} deleted successfully"