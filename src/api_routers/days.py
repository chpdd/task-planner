from fastapi import APIRouter
from sqlalchemy import select

from src.database import db_dep

router = APIRouter(prefix="/days", tags=["Days"])


@router.get("")
async def list_days(session: db_dep):
    select()
