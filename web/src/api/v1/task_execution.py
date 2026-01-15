from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload


from src.core.dependencies import db_dep, get_user_id, get_admin_id

from src.models import TaskExecution
from src.schemas.task_execution import TaskExecutionSchema, CreateTaskExecutionSchema

router = APIRouter(prefix="/task_executions", tags=["TaskExecutions"])


@router.get("")
async def list_task_executions(session: db_dep, user_id: int = Depends(get_user_id)):
    request = select(TaskExecution).where(TaskExecution.owner_id == user_id)
    task_executions = (await session.execute(request)).scalars()
    return [TaskExecutionSchema.model_validate(task_execution) for task_execution in task_executions]


@router.get("/all")
async def list_all_task_executions(session: db_dep, user_id: int = Depends(get_admin_id)):
    request = select(TaskExecution).options(selectinload(TaskExecution.day.date)).order_by(TaskExecution.day.date)
    task_executions = (await session.execute(request)).scalars()
    return [TaskExecutionSchema.model_validate(task_execution) for task_execution in task_executions]


@router.get("/{task_execution_id}")
async def retrieve_task_execution(task_execution_id: int, session: db_dep,
                                  user_id: int = Depends(get_user_id)):
    task_execution = await session.get(TaskExecution, task_execution_id)
    if task_execution is None or task_execution.owner_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return TaskExecutionSchema.model_validate(task_execution)


@router.post("")
async def create_task_execution(task_execution_schema: CreateTaskExecutionSchema,
                                session: db_dep,
                                user_id: int = Depends(get_user_id)):
    task_execution = TaskExecution(**task_execution_schema.model_dump())
    task_execution.owner_id = user_id
    session.add(task_execution)
    await session.commit()
    await session.refresh(task_execution)
    return TaskExecutionSchema.model_validate(task_execution)


@router.post("/bulk")
async def create_task_executions(task_execution_schemas: list[CreateTaskExecutionSchema],
                                 session: db_dep,
                                 user_id: int = Depends(get_user_id)):
    task_executions = [TaskExecution(**task_execution_schema.model_dump(), owner_id=user_id) for task_execution_schema
                       in task_execution_schemas]
    session.add_all(task_executions)
    await session.commit()
    return "TaskExecutions"


@router.delete("/{task_execution_id}")
async def destroy_task_execution(task_execution_id: int, session: db_dep, user_id: int = Depends(get_user_id)):
    task_execution = await session.get(TaskExecution, task_execution_id)
    if task_execution is None or task_execution.owner_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TaskExecution not found")
    await session.delete(task_execution)
    await session.commit()
    return {"detail": "TaskExecution deleted"}
