import datetime as dt

from fastapi import APIRouter, status, HTTPException
from sqlalchemy import select

from app.api.dependencies import user_id_dep, admin_id_dep, db_dep
from app.config import BaseSchema
from app.models import Day
from app.schemas.day import DaySchema

router = APIRouter(prefix="/days", tags=["Days"])


class DateSchema(BaseSchema):
    date: dt.date


@router.get("/{owner_id}")
async def list_user_days(owner_id: int, session: db_dep, user_id: admin_id_dep) -> list[DaySchema]:
    request = select(Day).where(Day.owner_id == owner_id)
    days = (await session.execute(request)).scalars()
    return [DaySchema.model_validate(day) for day in days]


@router.get("/all")
async def list_all_days(session: db_dep, user_id: admin_id_dep) -> list[DaySchema]:
    request = select(Day)
    days = (await session.execute(request)).scalars()
    return [DaySchema.model_validate(day) for day in days]


@router.get("/{day_id}")
async def retrieve_user_day(day_id: int, session: db_dep, user_id: admin_id_dep) -> DaySchema:
    day = await session.get(Day, day_id)
    if day is None or day.owner_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return DaySchema.model_validate(day)


@router.get("/by_date")
async def retrieve_user_day_by_date(day_id: int, date_schema: DateSchema, session: db_dep,
                                    user_id: user_id_dep) -> DaySchema:
    day_stmt = select(Day).where(Day.date == date_schema.date, Day.owner_id == user_id)
    day = (await session.execute(day_stmt)).scalar_one_or_none()
    if day is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return DaySchema.model_validate(day)
