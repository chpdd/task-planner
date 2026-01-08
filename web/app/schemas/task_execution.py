from pydantic import Field
from typing import Annotated

from app.core.config import BaseSchema
from app.schemas.task import TaskSchema


class CreateTaskExecutionSchema(BaseSchema):
    doing_hours: Annotated[int, Field(ge=1)]
    task_id: int


class IdTaskExecutionSchema(CreateTaskExecutionSchema):
    id: int


class TaskExecutionSchema(IdTaskExecutionSchema):
    day_id: int


class OwnerTaskExecutionSchema(TaskExecutionSchema):
    owner_id: int


class TaskAndExecutionSchema(BaseSchema):
    doing_hours: int
    task: TaskSchema
