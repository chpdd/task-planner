from fastapi import APIRouter, status, HTTPException
from sqlalchemy import select

from src.models import Day
from src.schemas.day import DaySchema, CreateDaySchema

from src.database import db_dep
from src.security import actual_user_id_dep

router = APIRouter(prefix="/days", tags=["Days"])


@router.get("")
async def list_days(session: db_dep, user_id: actual_user_id_dep):
    request = select(Day).where(Day.owner_id == user_id)
    tours = (await session.execute(request)).scalars()
    return [DaySchema.model_validate(day) for day in tours]


@router.get("/{day_id}")
async def retrieve_day(day_id: int, session: db_dep, user_id: actual_user_id_dep):
    day = await session.get(Day, day_id)
    if day is None or day.owner_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return DaySchema.model_validate(day)


@router.post("")
async def create_day(day_schema: CreateDaySchema, session: db_dep, user_id: actual_user_id_dep):
    day = Day(**day_schema.model_dump(), owner_id=user_id)
    session.add(day)
    await session.commit()
    await session.refresh(day)
    return DaySchema.model_validate(day)


@router.post("/bulk")
async def create_days(day_schemas: list[CreateDaySchema], session: db_dep, user_id: actual_user_id_dep):
    days = [Day(**day_schema.model_dump(), owner_id=user_id) for day_schema in day_schemas]
    session.add_all(days)
    await session.commit()
    return "Days"


@router.patch("/{day_id}")
async def update_day(day_id: int, work_hours: int, session: db_dep,
                     user_id: actual_user_id_dep):
    day = await session.get(Day, day_id)
    if day is None or day.owner_id != user_id:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Day not found")
    day.work_hours = work_hours
    await session.commit()
    await session.refresh(day)
    return DaySchema.model_validate(day)


@router.delete("/{day_id}")
async def destroy_day(day_id: int, session: db_dep, user_id: actual_user_id_dep):
    day = await session.get(Day, day_id)
    if day is None or day.owner_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Day not found")
    await session.delete(day)
    await session.commit()
    return {"detail": "Day deleted"}
