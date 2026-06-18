from sqlalchemy import Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from db.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.item import Item

class Sale(Base):
    __tablename__ = "sales"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"), index=True)
    quantity: Mapped[int]
    total_price: Mapped[float] = mapped_column(Float)
    customer_info: Mapped[str] = mapped_column(String, index=True, nullable=True)
    sale_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    item: Mapped["Item"] = relationship("Item", back_populates="sales")
