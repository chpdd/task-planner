from pydantic import Field
import datetime as dt

from src.config import BaseSchema
from src.schemas.task_execution import CreateTaskExecutionSchema


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
