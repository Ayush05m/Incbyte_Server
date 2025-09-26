from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class SweetBase(BaseModel):
    name: str
    category: str
    description: str
    price: float = Field(..., gt=0)
    quantity: int = Field(..., gt=0)
    imageUrl: Optional[str] = None

class SweetCreate(SweetBase):
    pass

class SweetUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    quantity: Optional[int] = Field(None, gt=0)
    imageUrl: Optional[str] = None

class Sweet(SweetBase):
    id: int
    createdAt: datetime
    updatedAt: datetime

    class Config:
        orm_mode = True

class SweetPurchase(BaseModel):
    quantity: int = Field(..., gt=0)

class SweetRestock(BaseModel):
    quantity: int = Field(..., gt=0)
