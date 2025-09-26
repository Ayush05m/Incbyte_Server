from pydantic import BaseModel
from datetime import datetime

class PurchaseBase(BaseModel):
    sweet_id: int
    quantity: int

class PurchaseCreate(PurchaseBase):
    pass

class Purchase(PurchaseBase):
    id: int
    user_id: int
    total_price: float
    purchase_date: datetime
    order_id: str

    class Config:
        orm_mode = True
