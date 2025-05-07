from pydantic import Field
import datetime as dt

from src.config import BaseSchema


class CreateTaskSchema(BaseSchema):
    name: str = Field(max_length=128)
    deadline: dt.date | None = Field()
    interest: int | None = Field(ge=1, le=10)
    importance: int | None = Field(ge=1, le=10)
    work_hours: int | None = Field(ge=1)


class TaskSchema(CreateTaskSchema):
    id: int
