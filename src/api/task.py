from fastapi import APIRouter, status, HTTPException
from sqlalchemy import select

from src.database import db_dep
from src.models import Task
from src.schemas.task import TaskSchema, CreateTaskSchema, UpdateTaskSchema
from src.security import actual_user_id_dep, only_admin_dep

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("")
async def list_tasks(session: db_dep, user_id: actual_user_id_dep):
    request = select(Task).where(Task.owner_id == user_id)
    tasks = (await session.execute(request)).scalars()
    return [TaskSchema.model_validate(task) for task in tasks]


@router.get("/all")
async def list_all_tasks(session: db_dep, user_id: only_admin_dep):
    request = select(Task)
    tasks = (await session.execute(request)).scalars()
    return [TaskSchema.model_validate(task) for task in tasks]


@router.get("/{task_id}")
async def retrieve_task(task_id: int, session: db_dep, user_id: actual_user_id_dep):
    task = await session.get(Task, task_id)
    if task is None or task.owner_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return TaskSchema.model_validate(task)


@router.post("")
async def create_task(task_schema: CreateTaskSchema, session: db_dep, user_id: actual_user_id_dep):
    task = Task(**task_schema.model_dump())
    task.owner_id = user_id
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return TaskSchema.model_validate(task)


@router.post("/bulk")
async def create_tasks(task_schemas: list[CreateTaskSchema], session: db_dep, user_id: actual_user_id_dep) -> dict:
    tasks = [Task(**task_schema.model_dump(), owner_id=user_id) for task_schema in task_schemas]
    session.add_all(tasks)
    await session.commit()
    return {"detail": "Tasks added"}


@router.patch("/{task_id}")
async def update_task(task_id: int, task_schema: UpdateTaskSchema, session: db_dep,
                      user_id: actual_user_id_dep):
    task = await session.get(Task, task_id)
    if task is None or task.owner_id != user_id:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    for attr, value in task_schema.model_dump().items():
        setattr(task, attr, value)
    await session.commit()
    await session.refresh(task)
    return TaskSchema.model_validate(task)


@router.delete("/{task_id}")
async def destroy_task(task_id: int, session: db_dep, user_id: actual_user_id_dep):
    task = await session.get(Task, task_id)
    if task is None or task.owner_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    await session.delete(task)
    await session.commit()
    return {"detail": "Task deleted"}
