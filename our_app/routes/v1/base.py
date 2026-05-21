# our_app/routes/v1/base.py   ← KEEP THE FILE, BUT CHANGE CONTENT
from fastapi import APIRouter

# Import the momo router
from our_app.routes.v1.momo_route import router as momo_router

# This is the main v1 router that main.py uses
api_router = APIRouter(prefix="/api/v1")

# Add all your feature routers here
api_router.include_router(momo_router, prefix="/momo", tags=["Momo Profit Predictor"])

