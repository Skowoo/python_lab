from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.delivery import Delivery
    from models.sale import Sale

class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(index=True)
    price: Mapped[float] = mapped_column(Float, index=True)
    description: Mapped[str] = mapped_column(index=True)
    stock: Mapped[int] = mapped_column(default=0)

    deliveries: Mapped[list["Delivery"]] = relationship(
        "Delivery", back_populates="item", cascade="all, delete-orphan"
    )
    sales: Mapped[list["Sale"]] = relationship(
        "Sale", back_populates="item", cascade="all, delete-orphan"
    )
