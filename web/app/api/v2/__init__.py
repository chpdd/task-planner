from fastapi import APIRouter

from app.api.v2 import auth, manual_day, planner, task, user, logger_check, admin

v2_router = APIRouter(prefix="/v2")

v2_router.include_router(auth.router)
v2_router.include_router(user.router)
v2_router.include_router(manual_day.router)
v2_router.include_router(task.router)
v2_router.include_router(planner.router)
v2_router.include_router(logger_check.router)
v2_router.include_router(admin.router)
