import datetime as dt

from fastapi import APIRouter, status, HTTPException
from sqlalchemy import select

from src.database import db_dep
from src.models import ManualDay
from src.schemas.manual_day import ManualDaySchema, CreateManualDaySchema, OwnerManualDaySchema
from src.security import actual_user_id_dep, BaseSchema, only_admin_dep

router = APIRouter(prefix="/manual_days", tags=["ManualDays"])


class DateSchema(BaseSchema):
    date: dt.date


@router.get("")
async def list_user_manual_manual_days(session: db_dep, user_id: actual_user_id_dep) -> list[ManualDaySchema]:
    request = select(ManualDay).where(ManualDay.owner_id == user_id)
    manual_days = (await session.execute(request)).scalars()
    return [ManualDaySchema.model_validate(manual_day) for manual_day in manual_days]


@router.get("/all")
async def list_all_manual_days(session: db_dep, user_id: only_admin_dep) -> list[OwnerManualDaySchema]:
    request = select(ManualDay)
    manual_days = (await session.execute(request)).scalars()
    return [OwnerManualDaySchema.model_validate(manual_day) for manual_day in manual_days]


@router.get("/{manual_day_id}")
async def retrieve_user_manual_day(manual_day_id: int, session: db_dep, user_id: actual_user_id_dep) -> ManualDaySchema:
    manual_day = await session.get(ManualDay, manual_day_id)
    if manual_day is None or manual_day.owner_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return ManualDaySchema.model_validate(manual_day)


@router.get("/by_date")
async def retrieve_user_manual_day_by_date(manual_day_id: int, date_schema: DateSchema, session: db_dep,
                                           user_id: actual_user_id_dep) -> ManualDaySchema:
    manual_day_stmt = select(ManualDay).where(ManualDay.date == date_schema.date, ManualDay.owner_id == user_id)
    manual_day = (await session.execute(manual_day_stmt)).scalar_one_or_none()
    if manual_day is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return ManualDaySchema.model_validate(manual_day)


@router.post("")
async def create_manual_day(manual_day_schema: CreateManualDaySchema, session: db_dep,
                            user_id: actual_user_id_dep) -> ManualDaySchema:
    manual_day = ManualDay(**manual_day_schema.model_dump(), owner_id=user_id)
    session.add(manual_day)
    await session.commit()
    await session.refresh(manual_day)
    return ManualDaySchema.model_validate(manual_day)


@router.post("/bulk")
async def create_manual_days(manual_day_schemas: list[CreateManualDaySchema], session: db_dep,
                             user_id: actual_user_id_dep) -> dict:
    manual_days = [ManualDay(**manual_day_schema.model_dump(), owner_id=user_id) for
                   manual_day_schema in manual_day_schemas]
    session.add_all(manual_days)
    await session.commit()
    return {"detail": "ManualDays added"}


@router.patch("/{manual_day_id}")
async def update_user_manual_day(manual_day_id: int, session: db_dep,
                                 user_id: actual_user_id_dep, work_hours: int = None) -> ManualDaySchema:
    manual_day = await session.get(ManualDay, manual_day_id)
    if manual_day is None or manual_day.owner_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ManualDay not found")
    manual_day.work_hours = work_hours
    await session.commit()
    await session.refresh(manual_day)
    return ManualDaySchema.model_validate(manual_day)


@router.delete("/{day_id}")
async def destroy_user_manual_day(day_id: int, session: db_dep, user_id: actual_user_id_dep) -> dict:
    day = await session.get(ManualDay, day_id)
    if day is None or day.owner_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Day not found")
    await session.delete(day)
    await session.commit()
    return {"detail": "Day deleted"}
