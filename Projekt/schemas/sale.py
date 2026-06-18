from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class SaleBase(BaseModel):
    item_id: int
    quantity: int = Field(..., gt=0)
    customer_info: Optional[str] = None

class SaleCreate(SaleBase):
    pass

class SaleInDBBase(SaleBase):
    id: int
    total_price: float
    sale_date: datetime

    class Config:
        from_attributes = True

class Sale(SaleInDBBase):
    pass
