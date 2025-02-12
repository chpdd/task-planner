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
        return f"Day(date={self.date}, day_work_hours={self.work_hours}, task_schedule={self.schedule})"

    def __str__(self) -> str:
        # return_str = f"Day date: {self.date}, day_work_hours={self.work_hours}, task_schedule: "
        # if len(self.schedule):
        #     return_str += f"\n{self.schedule}"
        # else:
        #     return_str += f"{self.schedule}"
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
                 dflt_day_work_hours: int = 4, dflt_task_work_hours: int = 2, max_date: dt.date = None) -> None:
        self._manual_days: [Day] = [] if manual_days is None else manual_days
        self._manual_date_work_hours: {dt.date: int} = {day.date: day.work_hours for day in self.manual_days}
        self._dflt_day_work_hours: int = dflt_day_work_hours
        self._dflt_task_work_hours: int = dflt_task_work_hours
        self._start_date: dt.date = start_date
        self._last_added_day_date: dt.date = start_date - dt.timedelta(days=1)
        self._days: [Day] = []
        self._near_fillable_day_index: int = -1

        self.init_days(max_date)

    def __getitem__(self, index: int) -> Day:
        return self._days[index]

    def __len__(self) -> int:
        return len(self._days)

    @property
    def start_date(self) -> dt.date:
        return self._start_date

    @property
    def near_fillable_day(self) -> Day:
        return self._days[self._near_fillable_day_index]

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
        self.init_days()

    @property
    def manual_date_work_hours(self) -> {dt.date: int}:
        return self._manual_date_work_hours

    @property
    def days(self):
        return self._days

    def init_days(self, max_date: dt.date = None) -> None:
        max_date = self.start_date if max_date is None else max_date
        self._days: [Day] = []
        print(f"max_date: {date_to_normal_str(max_date)}")
        while self._last_added_day_date <= max_date:
            print(f"last_added_day:{date_to_normal_str(self._last_added_day_date)} <= {date_to_normal_str(max_date)}")
            self.add_day()
        self._near_fillable_day_index: int = -1
        self.next_fillable_day()
        print(f"len days={len(self.days)}")
        print(f"days:\n{self.days}")
        print(f"last_added_day_date={date_to_normal_str(self._last_added_day_date)}")

    def clean_calendar(self):
        for day in self.days:
            day.clean_schedule()
        self._near_fillable_day_index = -1
        self.next_fillable_day()

    def _increment_last_added_day(self) -> None:
        self._last_added_day_date += dt.timedelta(days=1)

    def add_day(self) -> None:
        date = self._last_added_day_date + dt.timedelta(days=1)
        work_hours = self._manual_date_work_hours.get(date, self.dflt_day_work_hours)
        self._days.append(Day(date=date, work_hours=work_hours))
        self._increment_last_added_day()

    def next_fillable_day(self) -> None:
        self._near_fillable_day_index += 1
        while self._near_fillable_day_index >= len(self.days) or self.near_fillable_day.free_hours == 0:
            if self._near_fillable_day_index >= len(self.days):
                self.add_day()
            elif self.near_fillable_day.free_hours == 0:
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

    def add_task(self, task: Task, work_hours: int) -> None:
        while work_hours:
            day = self.near_fillable_day
            task, work_hours = day.add_task(task, work_hours)
            if day.is_task_filled():
                self.next_fillable_day()

    def add_task_before_date(self, task: Task, work_hours: int, date: dt.date) -> None:
        day_i = len(self.days) - 1
        while self.days[day_i].date >= date:
            day_i -= 1
        while work_hours:
            while self.days[day_i].is_task_filled():
                day_i -= 1
            task, work_hours = self.days[day_i].add_task(task, work_hours)
    def get_free_hours_before_date(self, left_date: dt.date, right_date: dt.date) -> int:
        result = 0
        while right_date >= self._last_added_day_date:
            self.add_day()
        for day in self.days:
            if day.date >= right_date:
                break
            if day.date >= left_date:
                result += day.free_hours
        return result


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

    def add_task(self, task: Task, work_hours: int = None) -> None:
        work_hours = task.work_hours if work_hours is None else work_hours
        self.calendar.add_task(task, work_hours)

    def add_task_before_date(self, task: Task, work_hours: int = None, date: dt.date = None) -> None:
        work_hours = task.work_hours if work_hours is None else work_hours
        date = task.deadline if date is None else date
        self.calendar.add_task_before_date(task, work_hours, date)

    def get_free_hours_before_date(self, left_date: dt.date, right_date: dt.date):
        return self.calendar.get_free_hours_before_date(left_date, right_date)

    def can_place_task_before_date(self, work_hours: int, date: dt.date) -> bool:
        print(f"Can place {work_hours} hours before date={date_to_normal_str(date)}?")
        sum_hours = 0
        for day in self.calendar.days[::-1]:
            print(date_to_normal_str(day.date), end=" ")
            if day.date < date:
                sum_hours += day.free_hours
                print(f"< {date_to_normal_str(date)}, sum_hours={sum_hours}")
                if sum_hours >= work_hours:
                    return True
            else:
                print(f">= {date_to_normal_str(date)}, sum_hours={sum_hours}")
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
            if task.deadline and task.deadline > self.calendar.start_date and self.can_place_task_before_date(
                    task.work_hours, task.deadline):
                self.add_task(task, task.work_hours)
            else:
                failed_tasks.add(task)
            self.failed_tasks = failed_tasks

    def custom_sort(self, func, reverse: bool = False) -> None:
        sorted_tasks = sorted(self.tasks, key=func, reverse=reverse)
        self.allocate_tasks(sorted_tasks)

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

    def force_procrastinate_sort(self):
        imp_srt = sorted(self._deadline_tasks, key=lambda task: (1 / task.importance, task.deadline, 1 / task.interest))
        int_srt = sorted(self._no_deadline_tasks, key=lambda task: (task.interest, task.importance), reverse=True)
        print("Imp srt", *imp_srt, sep="\n")
        print("Int srt", *int_srt, sep="\n")
        self.clean_calendar()
        failed_tasks = set()

        for task in imp_srt:
            print(
                f"{task.name} with {task.work_hours} work_hours can be placed? {self.can_place_task_before_date(task.work_hours, task.deadline)}")
            if self.can_place_task_before_date(task.work_hours, task.deadline):
                self.add_task_before_date(task)
            else:
                failed_tasks.add(task)

        for task in int_srt:
            self.add_task(task)
        self.failed_tasks = failed_tasks

    def procrastinate_sort_v1(self) -> None:

        def check_deadlines(tasks: [Task], added_hours: int = self._added_hours):
            CheckResult = namedtuple("CheckResult", ["close_deadline", "task", "max_free_hours"])
            tasks_free_hours = []
            for task in filter(lambda t: t in self.deadline_tasks, tasks):
                task_free_hours = self._hours_before_date(task.deadline,
                                                          added_hours=self._added_hours + 1) - task.work_hours
                if task_free_hours >= 0:
                    tasks_free_hours.append([task, task_free_hours])

            def rec(task_hours_pairs: [(Task, int)] = tasks_free_hours,
                    added_hours: int = added_hours, min_free_hours: int = None) -> CheckResult:
                result = CheckResult(close_deadline=False, task=task, max_free_hours=min_free_hours)
                if len(task_hours_pairs) == 0:
                    return result
                for i in range(len(task_hours_pairs)):
                    for j in range(len(task_hours_pairs)):
                        if i != j:
                            task_hours_pairs[j][1] -= task.work_hours
                    print(f"main task id={i} -> " + ", ".join(
                        map(lambda pair: f"{pair[0].id}:{pair[1]}", task_hours_pairs)))
                    min_hours_task = min(task_hours_pairs, key=lambda pair: pair[1])
                    min_free_hours = min(min_free_hours, min_hours_task[1]) if min_free_hours is not None else \
                        min_hours_task[1]
                    result = CheckResult(close_deadline=False, task=task, max_free_hours=min_free_hours)
                    # if min_hours_task[1] < 0:
                    #     return CheckResult(close_deadline=True, task=min_hours_task[0], max_free_hours=max_free_hours)
                    rec_result = rec(task_hours_pairs[:i] + task_hours_pairs[i + 1:],
                                     added_hours + task_hours_pairs[i][0].work_hours, min_free_hours)
                    print(result, rec_result)
                    # if result.max_free_hours is None:
                    #     result.max_free_hours = CheckResult(close_deadline=result.close_deadline,
                    #                                         task=result.close_deadline,
                    #                                         max_free_hours=rec_result.max_free_hours)
                    # elif rec_result.max_free_hours is None:
                    #     result.max_free_hours = CheckResult(close_deadline=rec_result.close_deadline,
                    #                                         task=result.close_deadline,
                    #                                         max_free_hours=rec_result.max_free_hours)
                    result = max(result, rec_result, key=lambda res: res.max_free_hours)

                return result

            return rec()

        self.clean_calendar()
        failed_tasks = set()
        srt_tasks = sorted(self.tasks, key=lambda task: (1 / task.interest, 1 / task.importance, task.deadline))
        index = 0
        check_result = check_deadlines(srt_tasks[index:], self._added_hours)
        print(check_result)
        # while len(srt_tasks):
        #     while srt_tasks[i].work_hours == 0 or srt_tasks[i].work_hours > self._hours_before_date(srt_tasks[i].deadline):
        #         i += 1
        #         if i < len(srt_tasks):
        #             task = srt_tasks[i]
        #         else:
        #             break

        #
        # while srt_int[int_i] not in tasks_set or srt_int[int_i].work_hours == 0 or srt_int[
        #     int_i].work_hours > self._hours_before_date(srt_int[int_i].deadline):
        #     tasks_set.discard(srt_int[int_i])
        #     int_i += 1
        #     if int_i < len(srt_int):
        #         int_task = srt_int[int_i]
        #     else:
        #         break
        # while imp_i < len(srt_imp) and (
        #         srt_imp[imp_i] not in tasks_set or srt_imp[imp_i].work_hours == 0 or srt_imp[
        #     imp_i].work_hours > self._hours_before_date(
        #     srt_imp[imp_i].deadline)):
        #     tasks_set.discard(srt_imp[imp_i])
        #     imp_i += 1
        # if imp_i < len(srt_imp):
        #     imp_task = srt_imp[imp_i]
        # else:
        #     break
        # print("Входим в рекурсию")
        # check_result = check_deadlines(srt_imp[imp_i:], self._added_hours + 1)
        # if not check_result.close_deadline and int_i < len(srt_int):
        #     if imp_i > len(srt_imp):
        #         for srt:
        #             self.add_task()
        #     self.add_task(int_task, 1)
        #     print(f"Добавляем 1 час {int_task}")
        #     int_task.work_hours -= 1
        # elif check_result.close_deadline and imp_i < len(srt_imp):
        #     self.add_task(imp_task, 1)
        #     print(f"Добавляем 1 часов {imp_task}")
        #     imp_task.work_hours -= 1

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
