from pydantic import Field
import datetime as dt
from typing import Annotated

from src.config import BaseSchema, settings


class CreateTaskExecutionSchema(BaseSchema):
    doing_hours: Annotated[int, Field(ge=1)]
    task_id: int


class IdTaskExecutionSchema(CreateTaskExecutionSchema):
    id: int


class TaskExecutionSchema(IdTaskExecutionSchema):
    day_id: int


class OwnerTaskExecutionSchema(TaskExecutionSchema):
    owner_id: int
