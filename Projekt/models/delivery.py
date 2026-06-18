from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from db.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.item import Item

class Delivery(Base):
    __tablename__ = "deliveries"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"), index=True)
    quantity: Mapped[int]
    supplier: Mapped[str] = mapped_column(String, index=True, nullable=True)
    delivery_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    item: Mapped["Item"] = relationship("Item", back_populates="deliveries")
