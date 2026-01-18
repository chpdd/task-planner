from typing import Any, Self
import datetime as dt
from pydantic import BaseModel, ConfigDict, Field, PrivateAttr, model_validator

from task_planner.calendar import Calendar, Task, Day


class Planner(BaseModel):
    model_config = ConfigDict(frozen=False, arbitrary_types_allowed=True)

    tasks: list[Task] = Field(default_factory=list)
    manual_days: list[Day] = Field(default_factory=list)
    start_date: dt.date = Field(default_factory=dt.date.today)

    _calendar: Calendar = PrivateAttr()
    _failed_tasks: set[Task] = PrivateAttr(default_factory=set)
    _deadline_tasks: set[Task] = PrivateAttr(default_factory=set)
    _no_deadline_tasks: set[Task] = PrivateAttr(default_factory=set)

    def __init__(self, tasks: list[Task] | None = None, manual_days: list[Day] | None = None, **data) -> None:
        if tasks is not None:
            data["tasks"] = tasks
        if manual_days is not None:
            data["manual_days"] = manual_days
        super().__init__(**data)

    @model_validator(mode='after')
    def changes_validator(self) -> Self:
        self.tasks = list(filter(lambda task: task.deadline is None or task.deadline > self.start_date,
                                 self.tasks))
        self._deadline_tasks, self._no_deadline_tasks = set(), set()
        for task in self.tasks:
            self._deadline_tasks.add(task) if task.deadline else self._no_deadline_tasks.add(task)
        max_date = max(map(lambda task: task.deadline, self._deadline_tasks)) if len(self._deadline_tasks) else None
        self._calendar = Calendar(manual_days=self.manual_days, start_date=self.start_date, max_date=max_date)
        return self

    @property
    def calendar(self):
        return self._calendar

    @property
    def failed_tasks(self):
        return self._failed_tasks

    def add_task(self, task: Task, work_hours: int | None = None) -> None:
        work_hours = task.work_hours if work_hours is None else work_hours
        self.calendar.add_task(task, work_hours)

    def add_task_before_date(self, task: Task, work_hours: int | None = None, date: dt.date | None = None) -> None:
        work_hours = task.work_hours if work_hours is None else work_hours
        date = task.deadline if date is None else date
        self.calendar.add_task_before_date(task, work_hours, date)

    def get_free_hours_before_date(self, left_date: dt.date, right_date: dt.date):
        return self.calendar.get_free_hours_before_date(left_date, right_date)

    def can_place_task_before_date(self, work_hours: int, date: dt.date) -> bool:
        sum_hours = 0
        for day in self.calendar.days[::-1]:
            if day.date < date:
                sum_hours += day.free_hours
                if sum_hours >= work_hours:
                    return True
        return False

    def clean_calendar(self) -> None:
        self.calendar.clean_calendar()
        self._failed_tasks = set()

    def validate_allocation(self) -> None:
        failed_tasks = set()
        for day in self.calendar:
            for task, work_hours in day.schedule.items():
                if task.deadline is not None and day.date >= task.deadline:
                    failed_tasks.add(task)
        self._failed_tasks = failed_tasks

    def allocate_tasks(self, tasks: list[Task]) -> None:
        self.clean_calendar()
        failed_tasks = set()

        for task in tasks:
            if (not task.deadline) or (task.deadline > self.calendar.start_date and self.can_place_task_before_date(
                    task.work_hours, task.deadline)):
                self.add_task(task, task.work_hours)
            else:
                failed_tasks.add(task)
        self._failed_tasks = failed_tasks

    @classmethod
    def get_allocation_methods(cls):
        return [
            cls.importance_allocation, cls.interest_allocation, cls.interest_importance_allocation,
            cls.points_allocation, cls.force_procrastination_allocation
        ]

    def custom_allocation(self, func: Any, rev_bool: bool = False) -> None:
        sorted_tasks = sorted(self.tasks, key=func, reverse=rev_bool)
        self.allocate_tasks(sorted_tasks)

    def importance_allocation(self) -> None:
        sorted_deadline_tasks = sorted(list(self._deadline_tasks),
                                       key=lambda task: (task.importance <= 5, task.deadline, 1 / task.interest))
        sorted_no_deadline_tasks = sorted(list(self._no_deadline_tasks),
                                          key=lambda task: (task.importance * task.interest),
                                          reverse=True)
        self.allocate_tasks(sorted_deadline_tasks + sorted_no_deadline_tasks)

    def interest_allocation(self) -> None:
        sorted_tasks = sorted(self.tasks, key=lambda task: (task.interest, task.importance, task.has_deadline()),
                              reverse=True)
        self.allocate_tasks(sorted_tasks)

    def interest_importance_allocation(self) -> None:
        sorted_tasks = sorted(self.tasks, key=lambda task: task.interest * task.importance, reverse=True)
        self.allocate_tasks(sorted_tasks)

    def points_allocation(self) -> None:
        sorted_tasks = sorted(self.tasks,
                              key=lambda task: (task.importance * task.importance * task.work_hours),
                              reverse=True)
        self.allocate_tasks(sorted_tasks)

    def force_procrastination_allocation(self) -> None:
        imp_srt = sorted(list(self._deadline_tasks), key=lambda t: (1 / t.importance, t.deadline, 1 / t.interest))
        int_srt = sorted(list(self._no_deadline_tasks), key=lambda t: (t.interest, t.importance), reverse=True)
        self.clean_calendar()
        failed_tasks = set()

        for task in imp_srt:
            if self.can_place_task_before_date(task.work_hours, task.deadline):
                self.add_task_before_date(task)
            else:
                failed_tasks.add(task)

        for task in int_srt:
            self.add_task(task)
        self._failed_tasks = failed_tasks

    def procrastination_allocation(self):
        self.force_procrastination_allocation()
