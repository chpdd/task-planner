from fastapi import APIRouter

from app.api.v1 import v1_router as v1_router
from app.api.v2 import v2_router as v2_router
from app.api.logger_check import router as check_router

api_router = APIRouter(prefix="/api")

# api_router.include_router(v1_router)
api_router.include_router(v2_router)
api_router.include_router(check_router)

