import datetime as dt

from task_planner.task import Task


class Day:
    def __init__(self, date: dt.date, work_hours: int = 2, schedule: {Task: int} = None) -> None:
        self._date: dt.date = date
        self._work_hours: int = work_hours
        self._schedule: {Task: int} = {} if schedule is None else schedule

    def __repr__(self) -> str:
        return f"Day(date={self.date}, day_work_hours={self.work_hours}, task_schedule={self.schedule})"

    def __str__(self) -> str:
        return f"Day date: {self.date}, day_work_hours={self.work_hours}, task_schedule: {self.schedule}"

    @property
    def date(self) -> dt.date:
        return self._date

    @date.setter
    def date(self, date: dt.date) -> None:
        self._date = date

    @property
    def work_hours(self) -> int:
        return self._work_hours

    @work_hours.setter
    def work_hours(self, work_hours: int) -> None:
        self._work_hours = work_hours

    @property
    def schedule(self) -> {Task: int}:
        return self._schedule

    @schedule.setter
    def schedule(self, schedule: {Task: int}) -> None:
        self._schedule = schedule

    @property
    def sum_hours(self) -> int:
        return sum(self.schedule.values())

    @property
    def free_hours(self) -> int:
        return self.work_hours - self.sum_hours

    def clean_schedule(self):
        self.schedule = {}

    def add_task(self, task: Task, work_hours: int) -> int:
        if self.sum_hours + work_hours <= self.work_hours:
            add_work_hours = work_hours
        else:
            add_work_hours = self.work_hours - self.sum_hours
        return_work_hours = work_hours - add_work_hours
        self.schedule[task] = self.schedule.get(task, 0) + add_work_hours
        return return_work_hours

    def is_weekend(self) -> bool:
        if self.work_hours == 0:
            return True
        return False

    def is_task_filled(self) -> bool:
        if self.work_hours == self.sum_hours:
            return True
        return False

    def has_tasks(self) -> bool:
        if len(self.schedule) != 0:
            return True
        return False
