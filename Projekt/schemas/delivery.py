from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DeliveryBase(BaseModel):
    item_id: int
    quantity: int = Field(..., gt=0)
    supplier: Optional[str] = None

class DeliveryCreate(DeliveryBase):
    pass

class DeliveryInDBBase(DeliveryBase):
    id: int
    delivery_date: datetime

    class Config:
        from_attributes = True

class Delivery(DeliveryInDBBase):
    pass
