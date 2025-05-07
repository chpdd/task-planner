from fastapi import APIRouter

from src.api_routers import tasks, days, users

api_router = APIRouter(prefix="/api")
api_router.include_router(tasks.router)
api_router.include_router(days.router)
api_router.include_router(users.router)
