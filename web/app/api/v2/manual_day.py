from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, get_user_id, get_admin_id

from app.crud import manual_day_crud
from app.schemas import manual_day as schemas

router = APIRouter(prefix="/manual_days", tags=["ManualDays"])


@router.get("")
async def list_manual_days(session: AsyncSession = Depends(get_db), user_id: int = Depends(get_user_id)) -> list[
    schemas.ManualDaySchema]:
    return await manual_day_crud.schema_owner_list(session, owner_id=user_id)


@router.post("")
async def create_manual_day(manual_day_schema: schemas.CreateManualDaySchema, session: AsyncSession = Depends(get_db),
                            user_id: int = Depends(get_user_id)) -> schemas.ManualDaySchema:
    manual_day_schema = await manual_day_crud.schema_owner_create(session, manual_day_schema, user_id)
    await session.commit()
    return manual_day_schema


@router.get("/{manual_day_id}")
async def get_manual_day(manual_day_id: int, session: AsyncSession = Depends(get_db),
                         user_id: int = Depends(get_user_id)) -> schemas.ManualDaySchema:
    return await manual_day_crud.schema_owner_get(session, manual_day_id, user_id)
