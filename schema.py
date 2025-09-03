from pydantic import BaseModel,ConfigDict
from typing import Optional

class ItemCreate(BaseModel):
    name : str
    description : str
    price : float
    tax: Optional[float] = None 

class ItemResponse(BaseModel):
    id : int
    name : str
    description : str
    price : float
    tax: Optional[float] = None 

    model_config = ConfigDict(from_attributes=True) 

class SuccessResponse(BaseModel):
    message: str

class ErrorResponse(BaseModel):
    error: str
