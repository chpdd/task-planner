from typing import ClassVar
import datetime as dt
from pydantic import BaseModel, ConfigDict, Field, model_validator

from task_planner.task import Task
from task_planner.settings import settings


class Day(BaseModel):
    model_config = ConfigDict(frozen=False, arbitrary_types_allowed=True)

    _id_counter: ClassVar[int] = 0

    id: int | None = Field(default=None)
    date: dt.date
    work_hours: int = Field(default_factory=lambda: settings.dflt_day_work_hours)
    schedule: dict[Task, int] = Field(default_factory=dict)

    @model_validator(mode='after')
    def sync_id(self) -> 'Day':
        if self.id is None:
            self.id = Day._generate_id()
        else:
            if self.id >= Day._id_counter:
                Day._id_counter = self.id + 1
        return self

    @classmethod
    def _generate_id(cls) -> int:
        day_id = cls._id_counter
        cls._id_counter += 1
        return day_id

    def __repr__(self) -> str:
        return f"Day(date={self.date}, day_work_hours={self.work_hours}, task_schedule={self.schedule})"

    def __str__(self) -> str:
        return f"Day date: {self.date}, day_work_hours={self.work_hours}, task_schedule: {self.schedule}"

    @property
    def sum_hours(self) -> int:
        return sum(self.schedule.values())

    @property
    def free_hours(self) -> int:
        return self.work_hours - self.sum_hours

    def clean_schedule(self):
        self.schedule = dict()

    def add_task(self, task: Task, work_hours: int) -> int:
        if self.sum_hours + work_hours <= self.work_hours:
            add_work_hours = work_hours
        else:
            add_work_hours = self.work_hours - self.sum_hours
        return_work_hours = work_hours - add_work_hours
        self.schedule[task] = self.schedule.get(task, 0) + add_work_hours
        return return_work_hours

    def is_weekend(self) -> bool:
        return self.work_hours == 0

    def is_task_filled(self) -> bool:
        return self.work_hours == self.sum_hours

    def has_tasks(self) -> bool:
        return len(self.schedule) != 0
