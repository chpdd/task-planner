from fastapi import APIRouter

from app.api.v1 import task, day, manual_day, user, auth, planner

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(user.router)
v1_router.include_router(auth.router)

v1_router.include_router(task.router)
v1_router.include_router(day.router)
v1_router.include_router(planner.router)
v1_router.include_router(manual_day.router)
