from typing import List, Optional
from sqlalchemy.orm import Session
from schemas.delivery import DeliveryCreate
from models.delivery import Delivery as DeliveryModel
from models.item import Item as ItemModel
from fastapi import HTTPException

class DeliveryService:
    def get_deliveries(self, db: Session, skip: int = 0, limit: int = 100) -> List[DeliveryModel]:
        return db.query(DeliveryModel).offset(skip).limit(limit).all()

    def get_delivery(self, db: Session, delivery_id: int) -> Optional[DeliveryModel]:
        return db.query(DeliveryModel).filter(DeliveryModel.id == delivery_id).first()

    def create_delivery(self, db: Session, delivery_in: DeliveryCreate) -> DeliveryModel:
        # Check if item exists
        item = db.query(ItemModel).filter(ItemModel.id == delivery_in.item_id).with_for_update().first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")

        # Create delivery
        db_delivery = DeliveryModel(**delivery_in.model_dump())
        db.add(db_delivery)
        
        # Increase item stock
        item.stock += delivery_in.quantity
        
        db.commit()
        db.refresh(db_delivery)
        return db_delivery

delivery_service = DeliveryService()
