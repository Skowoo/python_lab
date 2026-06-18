from pydantic import BaseModel, Field
from typing import Optional

class ItemBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., ge=0)
    description: Optional[str] = None

class ItemCreate(ItemBase):
    stock: int = Field(default=0, ge=0)

class ItemUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    price: Optional[float] = Field(None, ge=0)
    description: Optional[str] = None

class ItemInDBBase(ItemBase):
    id: int
    stock: int

    class Config:
        from_attributes = True

class Item(ItemInDBBase):
    pass
