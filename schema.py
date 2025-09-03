from pydantic import BaseModel

class ItemCreate(BaseModel):
    name : str
    description : str
    price : float
    tax : float = None

class ItemResponse(BaseModel):
    name : str
    description : str
    price : float

    class Config:
        from_attributes = True

class SuccessResponse(BaseModel):
    message: str

class ErrorResponse(BaseModel):
    error: str
