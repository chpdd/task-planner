from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


from app.core.dependencies import get_db, get_user_id, get_admin_id

from app.crud import task_crud
from app.schemas import task as schemas

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("")
async def list_tasks(session: AsyncSession = Depends(get_db), user_id: int = Depends(get_user_id)) -> list[schemas.TaskSchema]:
    return await task_crud.schema_owner_list(session, owner_id=user_id)


@router.post("")
async def create_task(task_schema: schemas.TaskSchema, session: AsyncSession = Depends(get_db),
                      user_id: int = Depends(get_user_id)) -> schemas.TaskSchema:
    task_schema = await task_crud.schema_owner_create(session, task_schema, user_id)
    await session.commit()
    return task_schema


@router.get("/{task_id}")
async def get_task(task_id: int, session: AsyncSession = Depends(get_db), user_id: int = Depends(get_user_id)) -> schemas.TaskSchema:
    return await task_crud.schema_owner_get(session, task_id, user_id)


@router.patch("/{task_id}")
async def update_task(task_schema: schemas.CreateTaskSchema, task_id: int, session: AsyncSession = Depends(get_db),
                      user_id: int = Depends(get_user_id)) -> schemas.TaskSchema:
    task_schema = await task_crud.schema_update_by_id(session, task_id, task_schema)
    session.commit()
    return task_schema
