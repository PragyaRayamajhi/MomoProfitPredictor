from fastapi import APIRouter
from our_app.routes.v1.momo_route import router as momo_router
from .base import api_router

__all__ = ["api_router"]
api_router = APIRouter(prefix="/api/v1")
api_router.include_router(momo_router, prefix="/momo", tags=["Momo Profit Predictor"])