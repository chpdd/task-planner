from pydantic import Field
import datetime as dt
from typing import Annotated

from app.core.config import BaseSchema


class CreateTaskSchema(BaseSchema):
    name: str = Field(max_length=128)
    deadline: Annotated[dt.date | None, Field(default=None)]
    interest: Annotated[int | None, Field(ge=1, le=10, default=None)]
    importance: Annotated[int | None, Field(ge=1, le=10, default=None)]
    work_hours: Annotated[int | None, Field(ge=1, default=None)]


class UpdateTaskSchema(BaseSchema):
    name: str | None = Field(max_length=128)


class TaskSchema(CreateTaskSchema):
    id: int


class OwnerTaskSchema(TaskSchema):
    owner_id: int
