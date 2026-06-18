from typing import Any, List
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from schemas.delivery import Delivery, DeliveryCreate
from services.delivery_service import delivery_service
from db.database import get_db
from core.security import check_user_role, get_current_user
from schemas.user import UserRole

router = APIRouter()

@router.get("/", response_model=List[Delivery])
def read_deliveries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> Any:
    """Retrieve deliveries."""
    deliveries = delivery_service.get_deliveries(db=db, skip=skip, limit=limit)
    return deliveries

@router.post("/", response_model=Delivery, status_code=status.HTTP_201_CREATED)
def create_delivery(
    delivery_in: DeliveryCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(check_user_role([UserRole.USER, UserRole.ADMIN]))
) -> Any:
    """Create new delivery and update stock. Only for USER or ADMIN role."""
    delivery = delivery_service.create_delivery(db=db, delivery_in=delivery_in)
    return delivery

@router.get("/{id}", response_model=Delivery)
def read_delivery(id: int, db: Session = Depends(get_db)) -> Any:
    """Get delivery by ID."""
    delivery = delivery_service.get_delivery(db=db, delivery_id=id)
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    return delivery
