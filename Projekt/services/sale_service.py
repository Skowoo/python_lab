from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from schemas.sale import SaleCreate
from models.sale import Sale as SaleModel
from models.item import Item as ItemModel
from fastapi import HTTPException
from datetime import datetime, timedelta

class SaleService:
    def get_sales(self, db: Session, skip: int = 0, limit: int = 100) -> List[SaleModel]:
        return db.query(SaleModel).offset(skip).limit(limit).all()

    def get_sale(self, db: Session, sale_id: int) -> Optional[SaleModel]:
        return db.query(SaleModel).filter(SaleModel.id == sale_id).first()

    def create_sale(self, db: Session, sale_in: SaleCreate) -> SaleModel:
        # Select item with lock to prevent race conditions during checkout
        item = db.query(ItemModel).filter(ItemModel.id == sale_in.item_id).with_for_update().first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")

        if item.stock < sale_in.quantity:
            raise HTTPException(status_code=400, detail="Not enough stock available")

        # Calculate total price
        total_price = item.price * sale_in.quantity

        # Create sale
        sale_data = sale_in.model_dump()
        db_sale = SaleModel(**sale_data, total_price=total_price)
        db.add(db_sale)
        
        # Decrease item stock
        item.stock -= sale_in.quantity
        
        db.commit()
        db.refresh(db_sale)
        return db_sale

    def get_product_statistics(
        self, 
        db: Session, 
        days: Optional[int] = None
    ) -> List[dict]:
        """
        Get sales statistics for all products.
        If days is provided, only include sales from last N days.
        """
        query = db.query(
            ItemModel.id,
            ItemModel.title,
            ItemModel.price,
            func.count(SaleModel.id).label("transaction_count"),
            func.sum(SaleModel.quantity).label("total_units_sold"),
            func.sum(SaleModel.total_price).label("total_revenue"),
            func.max(SaleModel.sale_date).label("last_sale_date")
        ).outerjoin(SaleModel).group_by(ItemModel.id, ItemModel.title, ItemModel.price)
        
        if days:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            query = query.filter(SaleModel.sale_date >= cutoff_date)
        
        results = query.all()
        
        statistics = []
        for row in results:
            transaction_count = row.transaction_count or 0
            total_units = row.total_units_sold or 0
            total_revenue = row.total_revenue or 0.0
            
            stats = {
                "item_id": row.id,
                "title": row.title,
                "price": row.price,
                "transaction_count": transaction_count,
                "total_units_sold": total_units,
                "total_revenue": total_revenue,
                "average_price_per_transaction": (
                    total_revenue / transaction_count if transaction_count > 0 else 0
                ),
                "average_units_per_transaction": (
                    total_units / transaction_count if transaction_count > 0 else 0
                ),
                "last_sale_date": row.last_sale_date,
            }
            statistics.append(stats)
        
        return statistics

    def get_product_statistics_by_id(
        self, 
        db: Session, 
        item_id: int,
        days: Optional[int] = None
    ) -> Optional[dict]:
        """
        Get sales statistics for a specific product.
        If days is provided, only include sales from last N days.
        """
        query = db.query(
            ItemModel.id,
            ItemModel.title,
            ItemModel.price,
            func.count(SaleModel.id).label("transaction_count"),
            func.sum(SaleModel.quantity).label("total_units_sold"),
            func.sum(SaleModel.total_price).label("total_revenue"),
            func.max(SaleModel.sale_date).label("last_sale_date")
        ).filter(ItemModel.id == item_id).outerjoin(SaleModel).group_by(
            ItemModel.id, ItemModel.title, ItemModel.price
        )
        
        if days:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            query = query.filter(SaleModel.sale_date >= cutoff_date)
        
        row = query.first()
        
        if not row:
            return None
        
        transaction_count = row.transaction_count or 0
        total_units = row.total_units_sold or 0
        total_revenue = row.total_revenue or 0.0
        
        return {
            "item_id": row.id,
            "title": row.title,
            "price": row.price,
            "transaction_count": transaction_count,
            "total_units_sold": total_units,
            "total_revenue": total_revenue,
            "average_price_per_transaction": (
                total_revenue / transaction_count if transaction_count > 0 else 0
            ),
            "average_units_per_transaction": (
                total_units / transaction_count if transaction_count > 0 else 0
            ),
            "last_sale_date": row.last_sale_date,
        }

sale_service = SaleService()
