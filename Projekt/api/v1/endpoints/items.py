from typing import Any, List, Optional
from fastapi import APIRouter, HTTPException, Depends, Response, Query
from sqlalchemy.orm import Session

from schemas.item import Item, ItemCreate, ItemUpdate
from schemas.statistics import ProductStatistics
from services.item_service import item_service
from services.sale_service import sale_service
from db.database import get_db
from core.security import check_user_role, get_current_user
from schemas.user import UserRole

router = APIRouter()

@router.get("/", response_model=List[Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> Any:
    """Retrieve items. Available to all users."""
    items = item_service.get_items(db=db, skip=skip, limit=limit)
    return items

@router.get("/statistics", response_model=List[ProductStatistics])
def get_all_product_statistics(
    days: Optional[int] = Query(None, description="Statystyki z ostatnich N dni"),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get sales statistics for all products.
    Available to all users.
    
    Query Parameters:
    - days: Optional. Include only sales from last N days
    """
    stats = sale_service.get_product_statistics(db=db, days=days)
    return stats

@router.post("/", response_model=Item, status_code=201)
def create_item(
    item_in: ItemCreate,
    db: Session = Depends(get_db),
    current_user = Depends(check_user_role([UserRole.ADMIN]))
) -> Any:
    """Create new item. Only for ADMIN role."""
    item = item_service.create_item(db=db, item_in=item_in)
    return item

@router.get("/{id}", response_model=Item)
def read_item(id: int, db: Session = Depends(get_db)) -> Any:
    """Get item by ID. Available to all users."""
    item = item_service.get_item(db=db, item_id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.get("/{id}/statistics", response_model=ProductStatistics)
def get_product_statistics(
    id: int,
    days: Optional[int] = Query(None, description="Statystyki z ostatnich N dni"),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get sales statistics for a specific product by ID.
    Available to all users.
    
    Query Parameters:
    - days: Optional. Include only sales from last N days
    """
    stats = sale_service.get_product_statistics_by_id(db=db, item_id=id, days=days)
    if not stats:
        raise HTTPException(status_code=404, detail="Item not found or no sales data")
    return stats

@router.put("/{id}", response_model=Item)
def update_item(
    id: int,
    item_in: ItemUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(check_user_role([UserRole.ADMIN]))
) -> Any:
    """Update item. Only for ADMIN role."""
    item = item_service.update_item(db=db, item_id=id, item_in=item_in)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.delete("/{id}", status_code=204)
def delete_item(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(check_user_role([UserRole.ADMIN]))
):
    """Delete item. Only for ADMIN role."""
    result = item_service.delete_item(db=db, item_id=id)
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return Response(status_code=204)