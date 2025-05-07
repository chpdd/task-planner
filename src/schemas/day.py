from pydantic import Field
import datetime as dt

from src.config import BaseSchema


class CreateDaySchema(BaseSchema):
    date: dt.date = Field()
    work_hours: int | None = Field(ge=1, le=24)


class DaySchema(CreateDaySchema):
    id: int
