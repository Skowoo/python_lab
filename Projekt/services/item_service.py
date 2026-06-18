from typing import List, Optional
from sqlalchemy.orm import Session
from schemas.item import ItemCreate, ItemUpdate
from models.item import Item as ItemModel

class ItemService:
    def get_items(self, db: Session, skip: int = 0, limit: int = 100) -> List[ItemModel]:
        return db.query(ItemModel).offset(skip).limit(limit).all()

    def get_item(self, db: Session, item_id: int) -> Optional[ItemModel]:
        return db.query(ItemModel).filter(ItemModel.id == item_id).first()

    def create_item(self, db: Session, item_in: ItemCreate) -> ItemModel:
        db_item = ItemModel(**item_in.model_dump())
        db.add(db_item)
        try:
            db.commit()
            db.refresh(db_item)
        except Exception:
            db.rollback()
            raise
        return db_item

    def update_item(self, db: Session, item_id: int, item_in: ItemUpdate) -> Optional[ItemModel]:
        item = self.get_item(db, item_id)
        if not item:
            return None
        
        update_data = item_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(item, field, value)
            
        db.add(item)
        try:
            db.commit()
            db.refresh(item)
        except Exception:
            db.rollback()
            raise
        return item
    
    def delete_item(self, db: Session, item_id: int) -> bool:
        item = self.get_item(db, item_id)
        if not item:
            return False
        
        db.delete(item)
        db.commit()
        return True

item_service = ItemService()

