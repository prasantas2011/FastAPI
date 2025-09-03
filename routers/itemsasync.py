from fastapi import APIRouter, Depends, HTTPException, Body, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import schema
from modelssqlalchemyasync import Item
from databaseasync import get_db

router = APIRouter(
    prefix="/items",
    tags=["items"],  # ✅ Swagger groups these endpoints
)

#setup with sqlalchemy orm

@router.post("/" , response_model=schema.ItemResponse,status_code=status.HTTP_201_CREATED)
async def create_item(item: schema.ItemCreate, db: AsyncSession  = Depends(get_db)):
    db_item = Item(**item.model_dump())
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item) 
    return db_item

@router.get("/{item_id}", response_model=schema.ItemResponse, status_code=status.HTTP_200_OK)
async def read_item(item_id: int, db: AsyncSession = Depends(get_db)):
    item = await db.get(Item, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found"
        )
    
    return item

@router.get("/",status_code=status.HTTP_200_OK)
async def read_items(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item).order_by(Item.id.desc()))
    items = result.scalars().all()
    return items

@router.put("/{item_id}", response_model=schema.ItemResponse,status_code=status.HTTP_200_OK)
async def update_item(item_id: int, item: schema.ItemCreate = Body(
        ...,
        examples={
            "name": "Updated Phone",
            "description": "Latest model with 5G",
            "price": 999.99,
            "tax": 10.0
        },
    ), db: AsyncSession = Depends(get_db)):
    db_item = await db.get(Item, item_id)

    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found"
        )
    
    for key, value in item.model_dump().items():
        setattr(db_item, key, value)
    await db.commit()
    await db.refresh(db_item)
    return db_item

@router.delete("/{item_id}",status_code=status.HTTP_200_OK)
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
    db_item = await db.get(Item, item_id)
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found"
        )

    await db.delete(db_item)
    await db.commit()
    return f"Item {item_id} deleted successfully"