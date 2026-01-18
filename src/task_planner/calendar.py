import datetime as dt
from typing import Self
from pydantic import BaseModel, ConfigDict, Field, PrivateAttr, model_validator

from task_planner.day import Day, Task
from task_planner.settings import settings


class Calendar(BaseModel):
    model_config = ConfigDict(frozen=False, arbitrary_types_allowed=True)

    manual_days: list[Day] = Field(default_factory=list)
    start_date: dt.date = Field(default_factory=dt.date.today)
    max_date: dt.date | None = Field(default=None)

    _days: list[Day] = PrivateAttr(default_factory=list)
    _near_fillable_day_index: int = PrivateAttr(default=-1)
    _manual_date_work_hours: dict[dt.date, int] = PrivateAttr(default_factory=dict)

    @model_validator(mode='after')
    def changes_validator(self) -> Self:
        self._manual_date_work_hours = {day.date: day.work_hours for day in self.manual_days}
        if self.max_date is None:
            self.max_date = self.start_date
        while self.last_added_day_date <= self.max_date:
            self.add_day()
        self._near_fillable_day_index = -1
        self.next_fillable_day()
        return self

    def __getitem__(self, index: int) -> Day:
        return self.days[index]

    def __len__(self) -> int:
        return len(self.days)

    def __iter__(self):
        return iter(self.days)

    @property
    def days(self) -> list[Day]:
        return self._days

    @property
    def near_fillable_day(self) -> Day:
        return self.days[self._near_fillable_day_index]

    @property
    def last_added_day_date(self) -> dt.date:
        if len(self.days):
            return self.days[-1].date
        return self.start_date - dt.timedelta(days=1)

    def clean_calendar(self) -> None:
        for day in self.days:
            day.clean_schedule()
        self._near_fillable_day_index = -1
        self.next_fillable_day()

    def add_day(self) -> None:
        date = self.last_added_day_date + dt.timedelta(days=1)
        work_hours = self._manual_date_work_hours.get(date, settings.dflt_day_work_hours)
        self.days.append(Day(date=date, work_hours=work_hours))

    def next_fillable_day(self) -> None:
        self._near_fillable_day_index += 1
        while self._near_fillable_day_index >= len(self.days) or self.near_fillable_day.is_task_filled():
            if self._near_fillable_day_index >= len(self.days):
                self.add_day()
            elif self.near_fillable_day.is_task_filled():
                self._near_fillable_day_index += 1

    def next_fillable_day_v2(self) -> None:
        """
        Same as next_fillable_day, but no double-checking of conditions and more cumbersome.
        """
        max_day_flag, free_hours_flag = True, True
        while max_day_flag or free_hours_flag:
            if self._near_fillable_day_index >= len(self.days):
                self.add_day()
                max_day_flag = False
                continue
            else:
                max_day_flag = True

            self._near_fillable_day_index += 1
            if self.near_fillable_day.free_hours == 0:
                free_hours_flag = False
            else:
                free_hours_flag = True

    def add_task(self, task: Task, work_hours: int):
        day = self.near_fillable_day
        while work_hours:
            while day.is_task_filled():
                self.next_fillable_day()
                day = self.near_fillable_day
            work_hours = day.add_task(task, work_hours)

    def add_task_before_date(self, task: Task, work_hours: int, date: dt.date):
        day_i = len(self.days) - 1
        while self.days[day_i].date >= date:
            day_i -= 1
        while work_hours:
            while self.days[day_i].is_task_filled():
                day_i -= 1
            work_hours = self.days[day_i].add_task(task, work_hours)

    def get_free_hours_before_date(self, left_date: dt.date, right_date: dt.date) -> int:
        result = 0
        while right_date >= self.last_added_day_date:
            self.add_day()
        for day in self.days:
            if day.date >= right_date:
                break
            if day.date >= left_date:
                result += day.free_hours
        return result
