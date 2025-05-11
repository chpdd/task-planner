from fastapi import APIRouter

from src.api_routers import task, day, user, auth

api_router = APIRouter(prefix="/api")
api_router.include_router(task.router)
api_router.include_router(day.router)
api_router.include_router(user.router)
api_router.include_router(auth.router)
