from typing import ClassVar
import datetime as dt
from pydantic import BaseModel, ConfigDict, Field, model_validator

from task_planner.settings import settings


class Task(BaseModel):
    model_config = ConfigDict(frozen=False, arbitrary_types_allowed=True)

    _id_counter: ClassVar[int] = 0

    id: int | None = Field(default=None)
    name: str
    deadline: dt.date | None = None
    interest: int = 5
    work_hours: int = Field(default_factory=lambda: settings.dflt_task_work_hours)
    importance: int = 5

    @model_validator(mode='after')
    def sync_id(self) -> 'Task':
        if self.id is None:
            self.id = Task._generate_id()
        else:
            # If ID is provided, ensure counter is ahead of it to prevent conflicts
            if self.id >= Task._id_counter:
                Task._id_counter = self.id + 1
        return self

    @classmethod
    def _generate_id(cls) -> int:
        task_id = cls._id_counter
        cls._id_counter += 1
        return task_id

    def __str__(self) -> str:
        return (f"Task with id: {self.id}, name: {self.name}, deadline: {self.deadline}, "
                f"interest: {self.interest}/10, work_hours: {self.work_hours}, "
                f"importance: {self.importance}/10 ")

    def __repr__(self) -> str:
        return (f"Task(task_id={self.id}, name={self.name}, deadline={self.deadline}, "
                f"interest={self.interest}, work_hours={self.work_hours}, "
                f"importance={self.importance})")

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if not isinstance(other, Task):
            return False
        return self.id == other.id

    @property
    def sum_interest(self) -> int:
        return self.work_hours * self.interest

    def has_deadline(self) -> bool:
        return self.deadline is not None
