from fastapi import APIRouter, HTTPException, status

from app.api.dependencies import user_id_dep, admin_id_dep, db_dep
from app.crud import manual_day_crud
from app.schemas import manual_day as schemas

router = APIRouter(prefix="/manual_days", tags=["ManualDays"])


@router.get("")
async def list_manual_days(session: db_dep, user_id: user_id_dep) -> list[schemas.ManualDaySchema]:
    return await manual_day_crud.schema_owner_list(session, owner_id=user_id)


@router.post("")
async def create_manual_day(manual_day_schema: schemas.CreateManualDaySchema, session: db_dep,
                            user_id: user_id_dep) -> schemas.ManualDaySchema:
    manual_day_schema = await manual_day_crud.schema_owner_create(session, manual_day_schema, user_id)
    await session.commit()
    return manual_day_schema


@router.get("/{manual_day_id}")
async def get_manual_day(manual_day_id: int, session: db_dep, user_id: user_id_dep) -> schemas.ManualDaySchema:
    return await manual_day_crud.schema_owner_get(session, manual_day_id, user_id)
