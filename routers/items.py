from fastapi import APIRouter, Depends, HTTPException, Body, status
from sqlalchemy.orm import Session
from typing import Union
import schema
from models import Item
from database import get_db

router = APIRouter(
    prefix="/items",
    tags=["items"],  # ✅ Swagger groups these endpoints
)

@router.post("/" , response_model=schema.ItemResponse,status_code=status.HTTP_201_CREATED)
def create_item(item: schema.ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/{item_id}", response_model=schema.ItemResponse, status_code=status.HTTP_200_OK)
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found"
        )
    
    return item

@router.get("/",status_code=status.HTTP_200_OK)
def read_items(db: Session = Depends(get_db)):
    items = db.query(Item).order_by(Item.id.desc()).all()
    return items

@router.put("/{item_id}", response_model=schema.ItemResponse,status_code=status.HTTP_200_OK)
def update_item(item_id: int, item: schema.ItemCreate = Body(
        ...,
        example={
            "name": "Updated Phone",
            "description": "Latest model with 5G",
            "price": 999.99,
            "tax": 10.0
        },
    ), db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()

    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found"
        )
    
    for key, value in item.dict().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/{item_id}",status_code=status.HTTP_200_OK)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found"
        )
    
    db.delete(db_item)
    db.commit()
    return f"Item {item_id} deleted successfully"