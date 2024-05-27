from datetime import timedelta, date, datetime
from copy import deepcopy

from .exceptions import *
from .utils import date_to_normal_str


class Day:
    __default_work_hours = 4
    __actual_date = datetime.today()

    def __init__(self, date_, **kwargs):
        if isinstance(date_, str):
            self.__date = datetime.strptime(date_, "%d.%m.%Y").date()
        elif isinstance(date_, date):
            self.__date = date_
        # self.__work_hours = timedelta(hours=int(kwargs.get("work_hours", 4)))
        self.__work_hours = int(kwargs.get("work_hours", self.__default_work_hours))
        self.__task_schedule = kwargs.get("task_schedule", {})

    def __repr__(self):
        return f"Day(date={self.__date}, day_work_hours={self.__work_hours}, task_schedule={self.__task_schedule})"

    def __str__(self):
        return f"Day date: {self.__date}, day_work_hours={self.__work_hours}, task_schedule: {self.__task_schedule}"

    def __copy__(self):
        copy_tasks = deepcopy(self.__task_schedule)
        return Day(self.__date, wotk_hours=self.__work_hours, tasks=copy_tasks)

    @classmethod
    def get_default_work_hours(cls):
        return cls.__default_work_hours

    @classmethod
    def set_default_work_hours(cls, default_work_hours):
        cls.__default_work_hours = default_work_hours

    @classmethod
    def get_actual_date(cls):
        return cls.__actual_date

    @classmethod
    def set_actual_date(cls, actual_date):
        cls.__actual_date = actual_date

    def is_weekend(self):
        if self.__work_hours == 0:
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


class Task:
    """Work_hours in day for class"""
    __default_work_hours = 4
    __actual_date = date.today()
    """ID counter"""
    __id_counter = 0

    def __init__(self, name: str, **kwargs):
        # if (kwargs.get("deadline", None) is None
        #         and kwargs.get("must_do", None) is None):
        #     raise InvalidTaskError(
        #         "You can't have deadline and must_do empty at the same time")

        """Validate deadline"""
        if ("deadline" in kwargs and
                datetime.strptime(kwargs["deadline"], "%d.%m.%Y").date() > Task.__actual_date + timedelta(days=365)):
            raise TooDistantDateError("The planned date is too far away.")

        """Initialize id"""
        self.__task_id = Task.__generate_id()

        """Initialize name"""
        self.__name = name

        """
        Initialize deadline

        by default deadline = today + 90 days
        """
        if "deadline" in kwargs:
            self.__deadline = datetime.strptime(kwargs["deadline"], "%d.%m.%Y").date()
        else:
            self.__deadline = Task.__actual_date + timedelta(days=90)

        """
        Initialize interest 

        value from 1 to 10, by default=5
        """
        self.__interest = int(kwargs.get("interest", 5))

        """
        Initialize work hours
        """
        # if "work_hours" in kwargs:
        #     self.__work_hours = timedelta(hours=int(kwargs["work_hours"]))
        # else:
        #     self.__work_hours = self.__day_work_hours
        self.__work_hours = int(kwargs.get("work_hours", self.__default_work_hours))

        """
        Initialize must_do

        must_do is an attribute that stores
         True if the task is mandatory and
          False if the task is optional
        """
        self.__must_do = False if kwargs.get("must_do", None) == "False" else True

    def __str__(self):
        return (f"Task with id: {self.__task_id}, name: {self.__name}, deadline: {self.__deadline}, "
                f"interest: {self.__interest}/10, work_hours: {self.__work_hours}, "
                f"must_do: {self.__must_do} ")

    def __repr__(self):
        return (f"Task(tasK_id={self.__task_id}, name={self.__name}, deadline={self.__deadline}, "
                f"interest={self.__interest}, work_hours={self.__work_hours}, "
                f"must_do={self.__must_do})")

    def present_print_rus(self):
        print(f"{self.__task_id}. {self.__name}, "
                f"дедлайн: {date_to_normal_str(self.__deadline)}, интерес: {self.__interest}/10,"
                f" время выполнения в часах: {self.__work_hours}, обязательно: {'Да' if self.__must_do else 'Нет'}")

    @classmethod
    def get_default_work_hours(cls):
        return cls.__default_work_hours

    @classmethod
    def set_default_work_hours(cls, default_work_hours):
        cls.__default_work_hours = default_work_hours

    @classmethod
    def set_actual_date(cls, actual_date):
        cls.__actual_date = actual_date

    @classmethod
    def __generate_id(cls):
        cls.__id_counter += 1
        return cls.__id_counter

    @property
    def interest(self):
        return self.__interest

    @interest.setter
    def interest(self, interest):
        self.interest = interest

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def deadline(self):
        return self.__deadline

    @deadline.setter
    def deadline(self, deadline: datetime.date):
        self.__deadline = deadline

    @property
    def must_do(self):
        return self.__must_do

    @must_do.setter
    def must_do(self, must_do):
        self.__must_do = must_do

    @property
    def task_id(self):
        return self.__task_id

    @property
    def work_hours(self):
        return self.__work_hours

    @work_hours.setter
    def work_hours(self, work_hours):
        self.__work_hours = work_hours

    @property
    def sum_interest(self):
        return self.__work_hours * self.__interest
