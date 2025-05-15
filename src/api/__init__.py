from fastapi import APIRouter

from src.api import task, day, manual_day, user, auth, planner

api_router = APIRouter(prefix="/api")

api_router.include_router(user.router)
api_router.include_router(auth.router)

api_router.include_router(task.router)
api_router.include_router(day.router)
api_router.include_router(planner.router)
api_router.include_router(manual_day.router)
