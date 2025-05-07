from fastapi import APIRouter
from sqlalchemy import select

from src.database import db_dep

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("")
async def list_tasks(session: db_dep):
    ...
