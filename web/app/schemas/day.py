from pydantic import Field
import datetime as dt

from app.core.config import BaseSchema
from app.schemas.task_execution import CreateTaskExecutionSchema, TaskAndExecutionSchema


class CreateDaySchema(BaseSchema):
    date: dt.date = Field()
    work_hours: int | None = Field(ge=0, le=24)


class DaySchema(CreateDaySchema):
    id: int


class OwnerDaySchema(DaySchema):
    owner_id: int


class CreateTaskExecutionsDaySchema(CreateDaySchema):
    task_executions: list[CreateTaskExecutionSchema]


class TaskExecutionsDaySchema(CreateTaskExecutionsDaySchema):
    id: int


class TasksDaySchema(DaySchema):
    task_executions: list[TaskAndExecutionSchema]
