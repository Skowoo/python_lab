from fastapi import APIRouter

from api.v1.endpoints import items, deliveries, sales, auth

api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(deliveries.router, prefix="/deliveries", tags=["deliveries"])
api_router.include_router(sales.router, prefix="/sales", tags=["sales"])