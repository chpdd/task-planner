import datetime as dt

from tasks_planner.utils import date_to_normal_str


class Task:
    __id_counter = 0

    def __init__(self, name: str, deadline: dt.date = None, interest: int = 5, work_hours: int = 2,
                 importance: int = 5) -> None:
        self._id: int = Task.__generate_id()
        self._name: str = name
        self._deadline: dt.date = deadline
        self._interest: int = interest
        self._work_hours: int = work_hours
        self._importance: int = importance

    def __str__(self) -> str:
        return (f"Task with id: {self.id}, name: {self.name}, deadline: {self.deadline}, "
                f"interest: {self.interest}/10, work_hours: {self.work_hours}, "
                f"importance: {self.importance}/10 ")

    def __repr__(self) -> str:
        return (f"Task(task_id={self.id}, name={self.name}, deadline={self.deadline}, "
                f"interest={self.interest}, work_hours={self.work_hours}, "
                f"importance={self.importance})")

    @classmethod
    def __generate_id(cls) -> int:
        task_id = cls.__id_counter
        cls.__id_counter += 1
        return task_id

    @property
    def id(self) -> int:
        return self._id

    @property
    def interest(self) -> int:
        return self._interest

    @interest.setter
    def interest(self, interest) -> None:
        self._interest = interest

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name) -> None:
        self._name = name

    @property
    def deadline(self) -> dt.date:
        return self._deadline

    @deadline.setter
    def deadline(self, deadline: dt.date) -> None:
        self._deadline = deadline

    @property
    def importance(self) -> int:
        return self._importance

    @importance.setter
    def importance(self, importance: int) -> None:
        self._importance = importance

    @property
    def work_hours(self) -> int:
        return self._work_hours

    @work_hours.setter
    def work_hours(self, work_hours: int) -> None:
        self._work_hours = work_hours

    @property
    def sum_interest(self) -> int:
        return self._work_hours * self.interest

    def has_deadline(self) -> bool:
        if self.deadline is not None:
            return True
        return False

    def str_present_rus(self) -> str:
        present_str = f"{self.id}. {self.name},"
        if self.deadline:
            present_str += f" дедлайн {date_to_normal_str(self.deadline)}"
        present_str += (f" интерес: {self.interest}/10, время выполнения в часах: {self.work_hours},"
                        f" важность: {self.importance}")
        return present_str
