from pydantic import Field
import datetime as dt

from app.core.config import BaseSchema


class CreateManualDaySchema(BaseSchema):
    date: dt.date = Field()
    work_hours: int | None = Field(ge=0, le=24)


class ManualDaySchema(CreateManualDaySchema):
    id: int


class OwnerManualDaySchema(ManualDaySchema):
    owner_id: int
