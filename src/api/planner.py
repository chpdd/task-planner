import datetime as dt
from enum import Enum

from fastapi import APIRouter
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

import task_planner as tp
from src.config import settings
from src.database import db_dep
from src.models import Task, FailedTask, TaskExecution, Day, ManualDay
from src.schemas.day import TaskExecutionsDaySchema, CreateTaskExecutionsDaySchema, TasksDaySchema
from src.schemas.task import OwnerTaskSchema
from src.schemas.manual_day import ManualDaySchema
from src.schemas.task_execution import CreateTaskExecutionSchema
from src.schemas.failed_task import FailedTaskSchema
from src.security import actual_user_id_dep

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
async def get_calendar(session: db_dep, user_id: actual_user_id_dep, start_date: dt.date = dt.date.today()
                       ) -> list[TaskExecutionsDaySchema]:
    days_stmt = select(Day).options(selectinload(Day.task_executions)).where(Day.owner_id == user_id,
                                                                             Day.date >= start_date)
    days = await session.scalars(days_stmt)
    days_schemas = []
    for day in days:
        if len(day.task_executions):
            days_schemas.append(TaskExecutionsDaySchema.model_validate(day))
    return days_schemas


@router.get("/calendar_with_tasks")
async def get_calendar_with_tasks(session: db_dep, user_id: actual_user_id_dep, start_date: dt.date = dt.date.today()
                            ) -> list[TasksDaySchema]:
    days_stmt = select(Day).options(selectinload(Day.task_executions).selectinload(TaskExecution.task)).where(
        Day.owner_id == user_id,
        Day.date >= start_date)
    days = await session.scalars(days_stmt)
    days_schemas = []
    for day in days:
        if len(day.task_executions):
            days_schemas.append(TasksDaySchema.model_validate(day))
    return days_schemas


@router.get("/failed_tasks")
async def list_failed_tasks(session: db_dep, user_id: actual_user_id_dep) -> list[FailedTaskSchema]:
    stmt = select(FailedTask).where(FailedTask.owner_id == user_id)
    failed_tasks_iter = await session.scalars(stmt)
    return [FailedTaskSchema.model_validate(failed_task) for failed_task in failed_tasks_iter]


@router.post("/allocate")
async def allocate_tasks(allocation_method: AllocationMethod, session: db_dep, user_id: actual_user_id_dep,
                         start_date: dt.date = dt.date.today()):
    # to display the parameter selection
    allocation_method = name_to_method.get(allocation_method, None)
    failed_tasks_delete_stmt = delete(FailedTask).where(FailedTask.owner_id == user_id)
    await session.execute(failed_tasks_delete_stmt)

    tasks_execution_delete_stmt = delete(TaskExecution).where(TaskExecution.owner_id == user_id)
    await session.execute(tasks_execution_delete_stmt)

    days_delete_stmt = delete(Day).where(Day.owner_id == user_id)
    await session.execute(days_delete_stmt)

    tasks_stmt = select(Task).where(Task.owner_id == user_id)
    task_iter = await session.scalars(tasks_stmt)
    task_schemas = [OwnerTaskSchema.model_validate(task_orm) for task_orm in task_iter]
    tasks = []
    for task_schema in task_schemas:
        task = tp.Task(**task_schema.model_dump(exclude={"id", "owner_id"}))
        task.db_id = task_schema.id
        tasks.append(task)

    manual_days_stmt = select(ManualDay).where(ManualDay.owner_id == user_id)
    manual_day_iter = await session.scalars(manual_days_stmt)
    manual_days_schemas = [ManualDaySchema.model_validate(manual_day_orm) for manual_day_orm in manual_day_iter]
    manual_days = [tp.Day(**manual_day_schema.model_dump(exclude={"id"})) for manual_day_schema in manual_days_schemas]

    planner = tp.Planner(tasks=tasks, manual_days=manual_days, start_date=start_date,
                         dflt_day_work_hours=settings.default_day_work_hours,
                         dflt_task_work_hours=settings.default_task_work_hours)
    allocation_method(planner)

    failed_tasks = [FailedTask(task_id=failed_task.db_id, owner_id=user_id) for failed_task in planner.failed_tasks]
    session.add_all(failed_tasks)

    day_schemas = []
    for day in planner.calendar.days:
        task_execution_schemas = [CreateTaskExecutionSchema(task_id=task.db_id, doing_hours=doing_hours) for
                                  task, doing_hours in day.schedule.items()]
        day_schema = CreateTaskExecutionsDaySchema(date=day.date, work_hours=day.work_hours,
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
