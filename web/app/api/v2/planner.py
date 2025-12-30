import datetime as dt
from enum import Enum

from fastapi import Depends, APIRouter
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

import task_planner as tp


from app.core.dependencies import get_db, get_user_id, get_admin_id

from app.core.config import settings

from app import schemas
from app.models import Task, FailedTask, TaskExecution, Day, ManualDay
from app.crud import failed_task_crud, task_execution_crud, day_crud, task_crud, manual_day_crud

router = APIRouter(prefix="/planner", tags=["Planner"])


class AllocationMethod(Enum):
    interest = "interest"
    importance = "importance"
    interest_importance = "interest_importance"
    points_allocation = "points_allocation"
    force_procrastinate = "force_procrastinate"


name_to_method = {
    AllocationMethod.interest: tp.Planner.interest_allocation,
    AllocationMethod.importance: tp.Planner.importance_allocation,
    AllocationMethod.interest_importance: tp.Planner.interest_importance_allocation,
    AllocationMethod.points_allocation: tp.Planner.points_allocation,
    AllocationMethod.force_procrastinate: tp.Planner.force_procrastination_allocation
}


@router.get("/calendar")
async def get_calendar(session: AsyncSession = Depends(get_db), user_id: int = Depends(get_user_id), start_date: dt.date = dt.date.today()
                       ) -> list[schemas.day.TaskExecutionsDaySchema]:
    days_stmt = select(Day).options(selectinload(Day.task_executions)).where(Day.owner_id == user_id,
                                                                             Day.date >= start_date)
    days = await session.scalars(days_stmt)
    days_schemas = []
    for day in days:
        if len(day.task_executions):
            days_schemas.append(schemas.day.TaskExecutionsDaySchema.model_validate(day))
    return days_schemas


@router.get("/calendar_with_tasks")
async def get_calendar_with_tasks(session: AsyncSession = Depends(get_db), user_id: int = Depends(get_user_id), start_date: dt.date = dt.date.today()
                                  ) -> list[schemas.day.TasksDaySchema]:
    days_stmt = select(Day).options(selectinload(Day.task_executions).selectinload(TaskExecution.task)).where(
        Day.owner_id == user_id,
        Day.date >= start_date)
    days = await session.scalars(days_stmt)
    days_schemas = []
    for day in days:
        if len(day.task_executions):
            days_schemas.append(schemas.day.TasksDaySchema.model_validate(day))
    return days_schemas


@router.get("/failed_tasks")
async def list_failed_tasks(session: AsyncSession = Depends(get_db), user_id: int = Depends(get_user_id)) -> list[schemas.failed_task.FailedTaskSchema]:
    return await failed_task_crud.schema_owner_list(session, owner_id=user_id)


@router.post("/allocate")
async def allocate_tasks(allocation_method: AllocationMethod, session: AsyncSession = Depends(get_db), user_id: int = Depends(get_user_id),
                         start_date: dt.date = dt.date.today()):
    allocation_method = name_to_method.get(allocation_method, None)

    await failed_task_crud.owner_all_delete(session, user_id)
    await task_execution_crud.owner_all_delete(session, user_id)
    await day_crud.owner_all_delete(session, user_id)

    task_schemas = await task_crud.schema_owner_list(session, user_id)
    tasks = []
    for task_schema in task_schemas:
        task = tp.Task(**task_schema.model_dump(exclude={"id", "owner_id"}))
        task.db_id = task_schema.id
        tasks.append(task)

    manual_days_schemas = await manual_day_crud.schema_owner_list(session, user_id)
    manual_days = [tp.Day(**manual_day_schema.model_dump(exclude={"id"})) for manual_day_schema in manual_days_schemas]

    planner = tp.Planner(tasks=tasks, manual_days=manual_days, start_date=start_date,
                         dflt_day_work_hours=settings.default_day_work_hours,
                         dflt_task_work_hours=settings.default_task_work_hours)
    allocation_method(planner)

    failed_tasks = [FailedTask(task_id=failed_task.db_id, owner_id=user_id) for failed_task in planner.failed_tasks]
    session.add_all(failed_tasks)

    day_schemas = []
    for day in planner.calendar.days:
        task_execution_schemas = [
            schemas.task_execution.CreateTaskExecutionSchema(task_id=task.db_id, doing_hours=doing_hours) for
            task, doing_hours in day.schedule.items()]
        day_schema = schemas.day.CreateTaskExecutionsDaySchema(date=day.date, work_hours=day.work_hours,
                                                               task_executions=task_execution_schemas)
        day_schemas.append(day_schema)
    days = [
        Day(
            **day_schema.model_dump(exclude={"task_executions"}),
            owner_id=user_id,
            task_executions=[
                TaskExecution(**task_execution_schema.model_dump(), owner_id=user_id) for task_execution_schema in
                day_schema.task_executions]
        )
        for day_schema in day_schemas]
    session.add_all(days)

    await session.commit()
    return {"detail": "Allocation is successful"}
