import datetime as dt
from copy import deepcopy, copy
from collections import namedtuple

from .utils import date_to_normal_str, read_class_instances, to_str_instance, get_instance_by_attr, read_args_kwargs


class Task:
    """ID counter"""
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

    def present_print_rus(self) -> None:
        print_str = f"{self.id}. {self.name},"
        if self.deadline:
            print_str += f" дедлайн {date_to_normal_str(self.deadline)}"
        print_str += f" интерес: {self.interest}/10, время выполнения в часах: {self.work_hours}, важность: {self.importance}"
        print(print_str)


class Day:
    def __init__(self, date: dt.date, work_hours: int = 2, schedule: {Task: int} = None) -> None:
        self._date: dt.date = date
        self._work_hours: int = work_hours
        self._schedule: {Task: int} = {} if schedule is None else schedule

    def __repr__(self) -> str:
        return f"Day(date={self.date}, day_work_hours={self.work_hours}, task_schedule=\n{self.schedule})"

    def __str__(self) -> str:
        return f"Day date: {self.date}, day_work_hours={self.work_hours}, task_schedule: \n{self.schedule}"

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

    def add_task(self, task: Task, work_hours: int) -> (Task, int):
        if self.sum_hours + work_hours <= self.work_hours:
            add_work_hours = work_hours
        else:
            add_work_hours = self.work_hours - self.sum_hours
        return_work_hours = work_hours - add_work_hours
        self.schedule[task] = self.schedule.get(task, 0) + add_work_hours
        return task, return_work_hours

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


class Calendar:
    def __init__(self, manual_days: [Day] = None, start_date: dt.date = dt.date.today(),
                 dflt_day_work_hours: int = 4, dflt_task_work_hours: int = 2) -> None:
        self._manual_days: [Day] = [] if manual_days is None else manual_days
        self._manual_date_work_hours: {dt.date: int} = {day.date: day.work_hours for day in self.manual_days}
        self._dflt_day_work_hours: int = dflt_day_work_hours
        self._dflt_task_work_hours: int = dflt_task_work_hours
        self._start_date: dt.date = start_date
        self._actual_date: dt.date = start_date
        self._days: [Day] = []
        self._filling_day_index: int = -1

        self.next_filling_day()

    def __getitem__(self, index: int) -> Day:
        return self._days[index]

    def __len__(self) -> int:
        return len(self._days)

    @property
    def start_date(self) -> dt.date:
        return self._start_date

    @property
    def _filling_day(self) -> Day:
        return self._days[self._filling_day_index]

    @property
    def dflt_day_work_hours(self) -> int:
        return self._dflt_day_work_hours

    @dflt_day_work_hours.setter
    def dflt_day_work_hours(self, work_hours: int) -> None:
        self._dflt_day_work_hours = work_hours

    @property
    def dflt_task_work_hours(self) -> int:
        return self._dflt_task_work_hours

    @dflt_task_work_hours.setter
    def dflt_task_work_hours(self, work_hours: int) -> None:
        self._dflt_task_work_hours = work_hours

    @property
    def manual_days(self) -> [Day]:
        return self._manual_days

    @manual_days.setter
    def manual_days(self, manual_days: [Day]) -> None:
        self._manual_days = manual_days
        self._manual_date_work_hours: {dt.date: int} = {day.date: day.work_hours for day in manual_days}
        self.reset_days()

    @property
    def manual_date_work_hours(self) -> {dt.date: int}:
        return self._manual_date_work_hours

    def reset_days(self) -> None:
        self._days: [Day] = []
        self._filling_day_index: int = -1
        self._actual_date = self.start_date
        self.next_filling_day()

    def increment_act_date(self) -> None:
        self._actual_date += dt.timedelta(days=1)

    def add_day(self) -> None:
        date = self._actual_date
        work_hours = self._manual_date_work_hours.get(date, self.dflt_day_work_hours)
        self._days.append(Day(date=date, work_hours=work_hours))
        self.increment_act_date()

    def next_filling_day(self) -> None:
        self.add_day()
        self._filling_day_index += 1

    def add_task(self, task: Task, work_hours: int) -> None:
        while work_hours:
            day = self._filling_day
            task, work_hours = day.add_task(task, work_hours)
            if day.is_task_filled():
                self.next_filling_day()

    def get_work_hours_before_deadline(self, deadline: dt.date) -> int:
        act_date = self._filling_day.date
        if act_date < deadline:
            hours_before_deadline = self._filling_day.work_hours - self._filling_day.sum_hours
            act_date += dt.timedelta(days=1)
            while act_date < deadline:
                hours_before_deadline += self._manual_date_work_hours.get(act_date, self._dflt_day_work_hours)
                act_date += dt.timedelta(days=1)
            return hours_before_deadline
        return 0


class Planner:
    # class PlannerTask(Task):
    #     def __init__(self, name: str, deadline: dt.date = None, interest: int = 5, work_hours: int = 2,
    #                  importance: int = 5, planner = None) -> None:
    #         super().__init__(name, deadline, interest, work_hours, importance)
    #         self._planner = pla
    #     @property
    #     def free_hours(self, added_hours: int = None):
    #         added_hours =  super(). is None
    #         return

    def __init__(self, tasks: [Task] = None, manual_days: [Day] = None, start_date: dt.date = dt.date.today(),
                 dflt_day_work_hours: int = 4, dflt_task_work_hours: int = 2) -> None:
        self._tasks = list(filter(lambda task: task.deadline is None or task.deadline > start_date,
                                  tasks)) if tasks is not None else []
        self._deadline_tasks: [Task] = []
        self._no_deadline_tasks: [Task] = []
        self._calendar: [Day] = Calendar(manual_days=manual_days, start_date=start_date,
                                         dflt_day_work_hours=dflt_day_work_hours,
                                         dflt_task_work_hours=dflt_task_work_hours)
        self._hours_before_date_dict: {dt.date: int} = {}
        self._added_hours: int = 0
        self._failed_tasks: [Task] = []

        self._init_filter_tasks()
        self._init_hours_before_date_dict()

    @property
    def tasks(self) -> [Task]:
        return self._tasks

    @tasks.setter
    def tasks(self, tasks: [Task]) -> None:
        self._tasks = list(
            filter(lambda task: task.deadline is None or task.deadline > self.calendar.start_date, tasks))
        self.clean_calendar()
        self._init_filter_tasks()
        self._init_hours_before_date_dict()

    @property
    def manual_days(self) -> [Day]:
        return self.calendar.manual_days

    @manual_days.setter
    def manual_days(self, manual_days: [Day]) -> None:
        self.calendar.manual_days = manual_days
        self._init_hours_before_date_dict()

    @property
    def deadline_tasks(self) -> [Task]:
        return self._deadline_tasks

    @property
    def no_deadline_tasks(self) -> [Task]:
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

    def _init_filter_tasks(self) -> None:
        deadline_tasks = []
        no_deadline_tasks = []
        for task in self.tasks:
            if task.deadline:
                deadline_tasks.append(task)
            else:
                no_deadline_tasks.append(task)
        self._deadline_tasks = deadline_tasks
        self._no_deadline_tasks = no_deadline_tasks

    def _init_hours_before_date_dict(self) -> None:
        hours_before_date_dict: {dt.date: int} = {}
        if len(self.tasks):
            act_date = self.calendar.start_date
            max_deadline_date = max(self.deadline_tasks, key=lambda task: task.deadline).deadline
            hours_counter = 0
            while act_date < max_deadline_date:
                hours_counter += self.calendar.manual_date_work_hours.get(act_date, self.calendar.dflt_day_work_hours)
                hours_before_date_dict[act_date + dt.timedelta(days=1)] = hours_counter
                act_date += dt.timedelta(days=1)
        self._hours_before_date_dict = hours_before_date_dict
        self._added_hours = 0

    def add_task(self, task: Task, work_hours: int = None) -> None:
        work_hours = task.work_hours if work_hours is None else work_hours
        self.calendar.add_task(task, work_hours)
        self._added_hours += work_hours

    def clean_calendar(self) -> None:
        self.calendar.reset_days()
        self.failed_tasks: {Task} = set()

    def _hours_before_date(self, date: dt.date, added_hours: int = None) -> int:
        added_hours = self._added_hours if added_hours is None else added_hours
        return self._hours_before_date_dict[date] - added_hours

    def simplify_tasks(self, tasks) -> [Task]:
        new_tasks = []
        i = 0
        while i < len(tasks):
            if i == 0:
                act_task = tasks[0]
                c = 1
                continue
            new_tasks = []

    def allocate_tasks(self, tasks) -> None:
        self.clean_calendar()
        failed_tasks = set()

        for task in tasks:
            if (task.deadline and task.deadline > self.calendar.start_date and
                    self._hours_before_date(task.deadline) >= task.work_hours):
                self.add_task(task, task.work_hours)
            else:
                failed_tasks.add(task)
        self.failed_tasks = failed_tasks

    def importance_sort(self) -> None:
        sorted_deadline_tasks = sorted(self.deadline_tasks,
                                       key=lambda task: (task.importance <= 5, task.deadline, 1 / task.interest))
        sorted_no_deadline_tasks = sorted(self.no_deadline_tasks,
                                          key=lambda task: (task.importance * task.interest),
                                          reverse=True)
        self.allocate_tasks(sorted_deadline_tasks + sorted_no_deadline_tasks)

    def interest_sort(self) -> None:
        sorted_tasks = sorted(self.tasks, key=lambda task: (task.interest, task.importance, task.has_deadline()),
                              reverse=True)
        self.allocate_tasks(sorted_tasks)

    def interest_importance_sort(self) -> None:
        sorted_tasks = sorted(self.tasks, key=lambda task: task.interest * task.importance, reverse=True)
        self.allocate_tasks(sorted_tasks)

    def points_sort(self) -> None:
        sorted_tasks = sorted(self.tasks,
                              key=lambda task: (task.importance * task.work_hours, task.interest * task.work_hours),
                              reverse=True)
        self.allocate_tasks(sorted_tasks)

    def procrastinate_sort_v1(self) -> None:

        def check_deadlines(tasks: [Task], added_hours: int = self._added_hours):
            CheckResult = namedtuple("CheckResult", ["close_deadline", "task"])
            tasks_free_hours_before_date = []
            for task in tasks:
                task_free_hours = self._hours_before_date(task.deadline,
                                                          added_hours=self._added_hours + 1) - task.work_hours
                if task_free_hours >= 0:
                    tasks_free_hours_before_date.append([task, task_free_hours])

            def rec(task_hours_pairs: [(Task, int)] = tasks_free_hours_before_date,
                    added_hours: int = added_hours) -> CheckResult:
                if len(task_hours_pairs) == 0:
                    return CheckResult(close_deadline=False, task=None)
                result = CheckResult(close_deadline=False, task=None)
                for i in range(len(task_hours_pairs)):
                    for j in range(len(task_hours_pairs)):
                        if i != j:
                            task_hours_pairs[j][1] -= task.work_hours
                    print(f"main task id={i} -> " + ", ".join(
                        map(lambda pair: f"{pair[0].id}:{pair[1]}", task_hours_pairs)))
                    min_hours_task = min(task_hours_pairs, key=lambda pair: pair[1])
                    if min_hours_task[1] < 0:
                        return CheckResult(close_deadline=True, task=min_hours_task[0])
                    result = max(result, rec(task_hours_pairs[:i] + task_hours_pairs[i + 1:],
                                             added_hours + task_hours_pairs[i][0].work_hours),
                                 key=lambda res: res.close_deadline)

                return result

            return rec()

        self.clean_calendar()
        failed_tasks = set()

        srt_int: [Task] = sorted(self.tasks, key=lambda task: (task.interest, task.importance),
                                 reverse=True)
        # sorted_free_hours_importance_tasks: [Task] = sorted(self.deadline_tasks, key=lambda task: (
        #     self._hours_before_date(task.deadline) - task.work_hours, 1 / task.importance, 1 / task.interest))

        srt_imp: [Task] = sorted(self.deadline_tasks, key=lambda task: (1 / task.importance, task.deadline))

        tasks_set: {Task} = set(self.tasks)
        int_i: int = 0
        imp_i: int = 0
        while len(tasks_set):
            while int_i < len(srt_int) and (
                    srt_int[int_i] not in tasks_set or srt_int[int_i].work_hours == 0 or srt_int[
                int_i].work_hours > self._hours_before_date(
                    srt_int[int_i].deadline)):
                tasks_set.discard(srt_int[int_i])
                int_i += 1
            if int_i < len(srt_int):
                int_task = srt_int[int_i]
            while imp_i < len(srt_imp) and (
                    srt_imp[imp_i] not in tasks_set or srt_imp[imp_i].work_hours == 0 or srt_imp[
                imp_i].work_hours > self._hours_before_date(
                srt_imp[imp_i].deadline)):
                tasks_set.discard(srt_imp[imp_i])
                imp_i += 1
            if imp_i < len(srt_imp):
                imp_task = srt_imp[imp_i]
            print("Входим в рекурсию")
            check_result = check_deadlines(srt_imp[imp_i:], self._added_hours + 1)
            if not check_result.close_deadline and int_i < len(srt_int):
                self.add_task(int_task, 1)
                print(f"Добавляем 1 час {int_task}")
                int_task.work_hours -= 1
            elif check_result.close_deadline and imp_i < len(srt_imp):
                self.add_task(imp_task, 1)
                print(f"Добавляем 1 часов {imp_task}")
                imp_task.work_hours -= 1

        self.failed_tasks = failed_tasks

    def procrastinate_sort_v2(self) -> None:
        def check_deadlines_rec_v2(tasks: [Task], added_hours: int = self._added_hours, max_added_hours: int = None):
            print(tasks)
            if len(tasks) == 0:
                return CheckResult(close_deadline=False, task=None, max_added_hours=max_added_hours)
            max_added_hours = min(list(map(lambda t: t.work_hours, tasks)) + [max_added_hours])
            for i in range(len(tasks)):
                task = tasks[i]
                task_free_hours_to_deadline = self._hours_before_date(task.deadline, added_hours) - task.work_hours
                if task_free_hours_to_deadline == 0:
                    return CheckResult(close_deadline=True, task=task, max_added_hours=0)
                next_tasks = tasks[:i] + tasks[i + 1:]
                return check_deadlines_rec(next_tasks, added_hours + task.work_hours, max_added_hours)

    def rec_sort(self) -> None:
        """
        sorting, where we count the different types of sorting and choose the one with the most points
        """
        pass

    def custom_sort(self, func, reverse: bool = False) -> None:
        sorted_tasks = sorted(self.tasks, key=func, reverse=reverse)
        self.allocate_tasks(sorted_tasks)

    def validate_allocation(self) -> None:
        failed_tasks = set()
        for day in self.calendar:
            for task, work_hours in day.schedule.items():
                if task.deadline is not None and day.date >= task.deadline:
                    failed_tasks.add(task)
        self.failed_tasks = failed_tasks

    def read_tasks_from_file(self, tasks_file_name: str) -> None:
        task_positional_attr_names = ["name"]
        tasks: [Task] = []
        for args, kwargs in read_args_kwargs(tasks_file_name, task_positional_attr_names):
            kwargs["work_hours"] = kwargs.get("work_hours", self.calendar.dflt_task_work_hours)
            tasks.append(Task(*args, **kwargs))
        self.tasks = tasks

    def read_days_from_file(self, days_file_name: str) -> None:
        day_pos_attr_names = ["date"]
        manual_days: [Day] = []
        for args, kwargs in read_args_kwargs(days_file_name, day_pos_attr_names):
            manual_days.append(Day(*args, **kwargs))
        self.manual_days = manual_days

    def read_tasks_days_from_file(self, tasks_file_name: str, days_file_name: str) -> None:
        self.read_days_from_file(days_file_name)
        self.read_tasks_from_file(tasks_file_name)

    def print_present_tasks_rus(self) -> None:
        if len(self.tasks):
            print("Все задачи")
            for task in self.tasks:
                task.present_print_rus()
        print()

    def print_failed_tasks_rus(self) -> None:
        if len(self.failed_tasks):
            print("Невыполненные задачи:")
            for task in self.failed_tasks:
                task.present_print_rus()
        print()

    def print_calendar_with_schedule(self) -> None:
        for day in self.calendar:
            if day.has_tasks():
                print(f"Day {day.date} with work_hours={day.work_hours} have tasks:")
                for task, work_hours in day.schedule.items():
                    output_attrs = ["name", "deadline", "interest", "importance"]
                    print(f"{work_hours} work hours at {to_str_instance(task, *output_attrs)}")
                print()
        print()

    def print_calendar_with_schedule_rus(self) -> None:
        print("Календарь с распределёнными задачами:")
        for day in self.calendar:
            if day.has_tasks():
                print(f"{(date_to_normal_str(day.date))} есть {day.work_hours} рабочий/их час/ов:")
                for task, work_hours in day.schedule.items():
                    print(f'Делать {task} на протяжении {work_hours} часов/а')
                print()
        print()
