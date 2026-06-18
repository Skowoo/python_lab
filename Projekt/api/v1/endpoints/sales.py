from typing import Any, List
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from schemas.sale import Sale, SaleCreate
from services.sale_service import sale_service
from db.database import get_db
from core.security import check_user_role, get_current_user
from schemas.user import UserRole

router = APIRouter()

@router.get("/", response_model=List[Sale])
def read_sales(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> Any:
    """Retrieve sales."""
    sales = sale_service.get_sales(db=db, skip=skip, limit=limit)
    return sales

@router.post("/", response_model=Sale, status_code=status.HTTP_201_CREATED)
def create_sale(
    sale_in: SaleCreate,
    db: Session = Depends(get_db),
    current_user = Depends(check_user_role([UserRole.USER, UserRole.ADMIN]))
) -> Any:
    """Create new sale and deduct stock. Only for USER or ADMIN role."""
    sale = sale_service.create_sale(db=db, sale_in=sale_in)
    return sale

@router.get("/{id}", response_model=Sale)
def read_sale(id: int, db: Session = Depends(get_db)) -> Any:
    """Get sale by ID."""
    sale = sale_service.get_sale(db=db, sale_id=id)
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale
