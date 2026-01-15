import datetime as dt
from tabulate import tabulate

from task_planner.utils import date_to_normal_str, read_args_kwargs
from task_planner.calendar import Calendar, Task, Day


class Planner:
    def __init__(self, tasks: [Task] = None, manual_days: [Day] = None, start_date: dt.date = dt.date.today(),
                 dflt_day_work_hours: int = 4, dflt_task_work_hours: int = 2) -> None:
        self._tasks = list(filter(lambda task: task.deadline is None or task.deadline > start_date,
                                  tasks)) if tasks is not None else []
        self._deadline_tasks: {Task} = set()
        self._no_deadline_tasks: {Task} = set()
        self.init_filter_tasks()
        max_date = max(map(lambda task: task.deadline, self.deadline_tasks)) if len(self.deadline_tasks) else None
        self._calendar: [Day] = Calendar(manual_days=manual_days, start_date=start_date,
                                         dflt_day_work_hours=dflt_day_work_hours,
                                         dflt_task_work_hours=dflt_task_work_hours, max_date=max_date)
        self._failed_tasks: [Task] = []

    @property
    def tasks(self) -> [Task]:
        return self._tasks

    @tasks.setter
    def tasks(self, tasks: [Task]) -> None:
        self._tasks = list(
            filter(lambda task: task.deadline is None or task.deadline > self.calendar.start_date, tasks))
        self.clean_calendar()
        self.init_filter_tasks()

    @property
    def manual_days(self) -> [Day]:
        return self.calendar.manual_days

    @manual_days.setter
    def manual_days(self, manual_days: [Day]) -> None:
        self.calendar.manual_days = manual_days

    @property
    def deadline_tasks(self) -> {Task}:
        return self._deadline_tasks

    @property
    def no_deadline_tasks(self) -> {Task}:
        return self._no_deadline_tasks

    @property
    def dflt_day_work_hours(self) -> int:
        return self.calendar.dflt_day_work_hours

    @dflt_day_work_hours.setter
    def dflt_day_work_hours(self, dflt_day_work_hours: int) -> None:
        self.calendar.dflt_day_work_hours = dflt_day_work_hours

    @property
    def dflt_task_work_hours(self) -> int:
        return self.calendar.dflt_task_work_hours

    @dflt_task_work_hours.setter
    def dflt_task_work_hours(self, dflt_task_work_hours: int) -> None:
        self.calendar.dflt_task_work_hours = dflt_task_work_hours

    @property
    def calendar(self) -> Calendar:
        return self._calendar

    @property
    def failed_tasks(self) -> {Task}:
        return self._failed_tasks

    @failed_tasks.setter
    def failed_tasks(self, tasks: {Task}) -> None:
        self._failed_tasks = tasks

    def init_filter_tasks(self) -> None:
        deadline_tasks = set()
        no_deadline_tasks = set()
        for task in self.tasks:
            if task.deadline:
                deadline_tasks.add(task)
            else:
                no_deadline_tasks.add(task)
        self._deadline_tasks = deadline_tasks
        self._no_deadline_tasks = no_deadline_tasks

    @staticmethod
    def read_tasks_from_file(tasks_file_name: str, dflt_tasks_work_hours: int = 2) -> [Task]:
        task_positional_attr_names = ["name"]
        tasks: [Task] = []
        for args, kwargs in read_args_kwargs(tasks_file_name, task_positional_attr_names):
            kwargs["work_hours"] = kwargs.get("work_hours", dflt_tasks_work_hours)
            tasks.append(Task(*args, **kwargs))
        return tasks

    @staticmethod
    def read_days_from_file(days_file_name: str, dflt_days_work_hours: int = 4) -> [Day]:
        day_pos_attr_names = ["date"]
        manual_days: [Day] = []
        for args, kwargs in read_args_kwargs(days_file_name, day_pos_attr_names):
            kwargs["work_hours"] = kwargs.get("work_hours", dflt_days_work_hours)
            manual_days.append(Day(*args, **kwargs))
        return manual_days

    def write_result_to_file(self, file_name: str, allocation_type) -> None:
        result = "\n".join([self.tasks_str_table_rus(self.tasks, "Таблица задач"),
                            f"Тип распределения: {allocation_type}",
                            self.failed_tasks_str_table_rus(),
                            self.calendar_str_tables_rus()])

        with open(file_name, "w", encoding="utf-8") as f:
            f.write(result)

    def tasks_str_table_rus(self, tasks=None, title="Таблица задач") -> str:
        result = ""
        if tasks is None:
            tasks = self.tasks
        if len(self.tasks):
            result += f"{title}\n"
            headers = ["id", "Название", "Дедлайн", "Интерес(от 1 до 10)", "Важность(от 1 до 10)",
                       "Время выполнения(в часах)"]
            tasks_lists = []
            for task in tasks:
                task_list = [task.id, task.name, date_to_normal_str(task.deadline), task.interest, task.importance,
                             task.work_hours]
                tasks_lists.append(task_list)
            result += tabulate(tasks_lists, headers=headers, tablefmt="pretty") + "\n"
        return result

    def failed_tasks_str_table_rus(self) -> str:
        return self.tasks_str_table_rus(tasks=sorted(self.failed_tasks, key=lambda task: task.id),
                                        title="Невыполненные задачи")

    def tasks_str_rus(self, tasks=None, title="Задачи:") -> str:
        if tasks is None:
            tasks = self.tasks
        result = ""
        if len(self.tasks):
            result += f"{title}\n"
            for task in self.tasks:
                result += task.str_present_rus() + "\n"
            result += "\n"
        return result

    def failed_tasks_str_rus(self) -> str:
        return self.tasks_str_rus(tasks=sorted(self.failed_tasks, key=lambda task: task.id),
                                  title="Невыполненные задачи")

    def calendar_str_rus(self, title="Календарь с распределёнными задачами") -> str:
        result = f"{title}\n"
        for day in self.calendar:
            if day.has_tasks():
                result += f"{(date_to_normal_str(day.date))} есть {day.work_hours} рабочий/их час/ов:\n"
                for task, work_hours in day.schedule.items():
                    result += f'Делать задачу "{task.name}" на протяжении {work_hours} часов/а\n'
                result += "\n"
        return result

    def calendar_str_tables_rus(self, title="Календарь с распределёнными задачами") -> str:
        result = f"{title}\n"
        for day in self.calendar:
            if day.has_tasks():
                result += f"{(date_to_normal_str(day.date))} есть {day.work_hours} рабочий/их час/ов:\n"
                tasks_lists = []
                for task, work_hours in day.schedule.items():
                    headers = ["id", "Название", "Дедлайн", "Интерес(от 1 до 10)", "Важность(от 1 до 10)",
                               "Время выполнения задачи(в часах)", "Время работы над задачей(в часах)"]
                    task_list = [task.id, task.name, date_to_normal_str(task.deadline), task.interest,
                                 task.importance, task.work_hours, work_hours]
                    tasks_lists.append(task_list)
                result += tabulate(tasks_lists, headers=headers, tablefmt="pretty") + "\n"
                result += "\n"
        return result

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
        self.failed_tasks: {Task} = set()

    def validate_allocation(self) -> None:
        failed_tasks = set()
        for day in self.calendar:
            for task, work_hours in day.schedule.items():
                if task.deadline is not None and day.date >= task.deadline:
                    failed_tasks.add(task)
        self.failed_tasks = failed_tasks

    def allocate_tasks(self, tasks) -> None:
        self.clean_calendar()
        failed_tasks = set()

        for task in tasks:
            if (not task.deadline) or (task.deadline > self.calendar.start_date and self.can_place_task_before_date(
                    task.work_hours, task.deadline)):
                self.add_task(task, task.work_hours)
            else:
                failed_tasks.add(task)
        self.failed_tasks = failed_tasks

    @classmethod
    def get_allocation_methods(cls):
        result = [
            cls.importance_allocation, cls.interest_allocation, cls.interest_importance_allocation,
            cls.points_allocation, cls.force_procrastination_allocation
        ]
        return result

    def custom_allocation(self, func, rev_bool: bool = False) -> None:
        sorted_tasks = sorted(self.tasks, key=func, reverse=rev_bool)
        self.allocate_tasks(sorted_tasks)

    def importance_allocation(self) -> None:
        sorted_deadline_tasks = sorted(self.deadline_tasks,
                                       key=lambda task: (task.importance <= 5, task.deadline, 1 / task.interest))
        sorted_no_deadline_tasks = sorted(self.no_deadline_tasks,
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
        imp_srt = sorted(self._deadline_tasks, key=lambda t: (1 / t.importance, t.deadline, 1 / t.interest))
        int_srt = sorted(self._no_deadline_tasks, key=lambda t: (t.interest, t.importance), reverse=True)
        self.clean_calendar()
        failed_tasks = set()

        for task in imp_srt:
            if self.can_place_task_before_date(task.work_hours, task.deadline):
                self.add_task_before_date(task)
            else:
                failed_tasks.add(task)

        for task in int_srt:
            self.add_task(task)
        self.failed_tasks = failed_tasks

    def procrastination_allocation(self):
        self.force_procrastination_allocation()
