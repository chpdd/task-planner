from datetime import timedelta, date, datetime
from copy import deepcopy


class InvalidDayError(Exception):
    """Error class for invalid Day"""
    pass


class TooDistantDateError(Exception):
    """Error class for raise if task too far away"""
    pass


class Day:
    __default_work_hours = 4

    def __init__(self, date_, **kwargs):
        if isinstance(date_, str):
            self.__date = datetime.strptime(date_, "%d.%m.%Y").date()
        elif isinstance(date_, date):
            self.__date = date_
        # self.__work_hours = timedelta(hours=int(kwargs.get("work_hours", 4)))
        self.__work_hours = int(kwargs.get("work_hours", self.__default_work_hours))
        self.__task_schedule = kwargs.get("task_schedule", {})

    def __repr__(self):
        return f"Day(date={self.__date}, day_work_hours={self.__work_hours})"

    def __str__(self):
        return f"Day date: {self.__date}, day_work_hours={self.__work_hours}"

    def __copy__(self):
        copy_tasks = deepcopy(self.__task_schedule)
        return Day(self.__date, wotk_hours=self.__work_hours, tasks=copy_tasks)

    @classmethod
    def set_default_work_hours(cls, default_work_hours):
        cls.__default_work_hours = default_work_hours

    def is_weekend(self):
        if self.__work_hours == timedelta(hours=0):
            return True
        return False

    def has_tasks(self):
        if len(self.__task_schedule) != 0:
            return True
        return False

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, date_):
        self.__date = date_

    @property
    def work_hours(self):
        return self.__work_hours

    @work_hours.setter
    def work_hours(self, work_hours):
        self.__work_hours = work_hours

    @property
    def tasks(self):
        return self.__task_schedule

    @tasks.setter
    def tasks(self, tasks):
        self.__task_schedule = tasks

    @property
    def task_schedule(self):
        return self.__task_schedule

    @task_schedule.setter
    def task_schedule(self, task_schedule):
        self.__task_schedule = task_schedule
