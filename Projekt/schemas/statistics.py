from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProductStatistics(BaseModel):
    item_id: int
    title: str
    price: float
    transaction_count: int = Field(description="Liczba transakcji sprzedaży")
    total_units_sold: int = Field(description="Całkowita ilość sprzedanych sztuk")
    total_revenue: float = Field(description="Całkowity przychód ze sprzedaży")
    average_price_per_transaction: Optional[float] = Field(
        description="Średnia cena na jedną transakcję"
    )
    average_units_per_transaction: Optional[float] = Field(
        description="Średnia ilość jednostek na transakcję"
    )
    last_sale_date: Optional[datetime] = Field(
        description="Data ostatniej sprzedaży"
    )
    
    class Config:
        from_attributes = True

class ProductStatisticsResponse(BaseModel):
    statistics: list[ProductStatistics]
    total_products: int
    total_transactions: int
    total_units_sold: int
    total_revenue: float
