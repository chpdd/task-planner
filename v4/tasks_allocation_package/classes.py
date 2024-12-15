import datetime as dt
from copy import deepcopy, copy

from .utils import date_to_normal_str, read_class_instances, to_str_instance, get_instance_by_attr


class Task:
    """ID counter"""
    __id_counter = 0

    def __init__(self, name: str, deadline: dt.date = None, interest: int = 5, work_hours: int = 2,
                 importance: int = 5):
        self._id = Task.__generate_id()
        self._name = name
        self._deadline = deadline
        self._interest = interest
        self._work_hours = work_hours
        self._importance = importance

    def __str__(self):
        return (f"Task with id: {self.id}, name: {self.name}, deadline: {self.deadline}, "
                f"interest: {self.interest}/10, work_hours: {self.work_hours}, "
                f"importance: {self.importance}/10 ")

    def __repr__(self):
        return (f"Task(task_id={self.id}, name={self.name}, deadline={self.deadline}, "
                f"interest={self.interest}, work_hours={self.work_hours}, "
                f"importance={self.importance})")

    @classmethod
    def __generate_id(cls):
        cls.__id_counter += 1
        return cls.__id_counter

    @property
    def id(self):
        return self._id

    @property
    def interest(self):
        return self._interest

    @interest.setter
    def interest(self, interest):
        self._interest = interest

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def deadline(self):
        return self._deadline

    @deadline.setter
    def deadline(self, deadline: dt.date):
        self._deadline = deadline

    @property
    def importance(self):
        return self._importance

    @importance.setter
    def importance(self, importance):
        self._importance = importance

    @property
    def work_hours(self):
        return self._work_hours

    @work_hours.setter
    def work_hours(self, work_hours):
        self._work_hours = work_hours

    @property
    def sum_interest(self):
        return self._work_hours * self.interest

    def present_print_rus(self):
        print(f"{self.id}. {self.name}, "
              f"{f"дедлайн {date_to_normal_str(self.deadline)}" if self.deadline is not None else ""}, интерес: {self.interest}/10,"
              f" время выполнения в часах: {self.work_hours}, обязательность: {self.importance}")


class DaySchedule:
    def __init__(self, work_hours: int, task_schedule=None):
        self._work_hours: int = work_hours
        self._task_schedule: {Task: int} = {} if task_schedule is None else task_schedule

    def __str__(self):
        str_list = [f"{key}: {val}" for key, val in self.task_schedule.items()]
        return_str = "{\n" + "\n".join(str_list) + "}"
        return f"DaySchedule({return_str})"

    def __repr__(self):
        return_str_list = [{key: val} for key, val in self.task_schedule.items()]
        return f"DaySchedule({self.task_schedule})"

    @property
    def work_hours(self):
        return self._work_hours

    @property
    def task_schedule(self):
        return self._task_schedule

    @property
    def sum_hours(self):
        return sum(self.task_schedule.values())

    def add_task(self, task: Task, work_hours: int):
        if self.sum_hours + work_hours <= self.work_hours:
            add_work_hours = work_hours
        else:
            add_work_hours = self.work_hours - self.sum_hours
        return_work_hours = work_hours - add_work_hours
        self._task_schedule[task] = self.task_schedule.get(task, 0) + add_work_hours
        return task, return_work_hours


class Day:
    def __init__(self, date: dt.date, work_hours: int = 2, task_schedule=None):
        self._date = date
        self._work_hours = work_hours
        self._day_schedule = DaySchedule(work_hours, task_schedule)

    def __repr__(self):
        return f"Day(date={self.date}, day_work_hours={self.work_hours}, task_schedule=\n{self.day_schedule})"

    def __str__(self):
        return f"Day date: {self.date}, day_work_hours={self.work_hours}, task_schedule: \n{self.day_schedule}"

    # def __copy__(self):
    #     copy_tasks = deepcopy(self.task_schedule)
    #     return Day(self.date, wotk_hours=self.work_hours, tasks=copy_tasks)

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        self._date = date

    @property
    def work_hours(self):
        return self._work_hours

    @work_hours.setter
    def work_hours(self, work_hours):
        self._work_hours = work_hours

    @property
    def day_schedule(self):
        return self._day_schedule

    @day_schedule.setter
    def day_schedule(self, day_schedule):
        self._day_schedule = day_schedule

    def is_weekend(self):
        if self.work_hours == 0:
            return True
        return False

    def is_task_filled(self):
        if self.work_hours == self.day_schedule.sum_hours:
            return True
        return False

    def add_task(self, task: Task, work_hours: int):
        return self.day_schedule.add_task(task, work_hours)

    def has_tasks(self):
        if len(self.day_schedule.task_schedule) != 0:
            return True
        return False


class Planner:
    def __init__(self, tasks: [Task], manual_days=None, start_date=dt.date.today(), dflt_day_work_hours=4,
                 dflt_task_work_hours=2):
        self._manual_days = [] if manual_days is None else manual_days
        self._manual_date_work_hours = {day.date: day.work_hours for day in manual_days}
        self._tasks = tasks
        self._dflt_day_wrk_hrs = dflt_day_work_hours
        self._dflt_tsk_wrk_hrs = dflt_task_work_hours
        self._start_date = start_date
        self._calendar: [Day] = []
        self._filling_day_index: int = -1
        self._actual_date = start_date
        self._failed_tasks: {Task} = None

        self.next_filling_day()

    @property
    def actual_date(self):
        return self._actual_date

    @property
    def manual_days(self):
        return self._manual_days

    @property
    def manual_date_work_hours(self):
        return self._manual_date_work_hours

    @property
    def tasks(self):
        return self._tasks

    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, start_date):
        self._start_date = start_date

    @property
    def dflt_day_wrk_hrs(self) -> int:
        return self._dflt_day_wrk_hrs

    @dflt_day_wrk_hrs.setter
    def dflt_day_wrk_hrs(self, dflt_day_wrk_hrs: int):
        self._dflt_day_wrk_hrs = dflt_day_wrk_hrs

    @property
    def dflt_tsk_wrk_hrs(self) -> int:
        return self._dflt_tsk_wrk_hrs

    @dflt_tsk_wrk_hrs.setter
    def dflt_tsk_wrk_hrs(self, dflt_tsk_wrk_hrs: int):
        self._dflt_tsk_wrk_hrs = dflt_tsk_wrk_hrs

    @property
    def calendar(self):
        return self._calendar

    @calendar.setter
    def calendar(self, calendar):
        self._calendar = calendar

    @property
    def filling_day_index(self):
        return self._filling_day_index

    @filling_day_index.setter
    def filling_day_index(self, index):
        self._filling_day_index = index

    @property
    def filling_day(self):
        return self.calendar[self.filling_day_index]

    @property
    def failed_tasks(self):
        return self._failed_tasks

    @failed_tasks.setter
    def failed_tasks(self, tasks: [Task]):
        self._failed_tasks = tasks

    def increment_act_date(self):
        self._actual_date += dt.timedelta(days=1)

    def add_day(self):
        date = self.actual_date
        work_hours = self.manual_date_work_hours.get(date, self.dflt_day_wrk_hrs)
        self.calendar.append(Day(date=date, work_hours=work_hours))
        self.increment_act_date()

    def next_filling_day(self):
        self.add_day()
        self.filling_day_index += 1

    def add_task(self, task, work_hours):
        while work_hours:
            day = self.filling_day
            return_task, work_hours = day.add_task(task, work_hours)
            if day.is_task_filled():
                self.next_filling_day()

    def get_act_wk_hrs_bfr_ddln(self, deadline):
        act_date = self.filling_day.date
        if act_date < deadline:
            hours_before_deadline = 0
            hours_before_deadline = self.filling_day.day_schedule.work_hours - self.filling_day.day_schedule.sum_hours
            act_date += dt.timedelta(days=1)
            while act_date < deadline:
                hours_before_deadline += self.manual_date_work_hours.get(act_date, self.dflt_day_wrk_hrs)
                act_date += dt.timedelta(days=1)
            return hours_before_deadline
        return 0

    def importance_first_sort(self):
        tasks_with_deadline = []
        tasks_without_deadline = []
        failed_tasks = set()
        for task in self.tasks:
            if task.deadline is None:
                tasks_without_deadline.append(task)
            else:
                tasks_with_deadline.append(task)
        sorted_deadline_tasks = sorted(tasks_with_deadline,
                                       key=lambda task: (task.importance <= 5, task.deadline, 1 / task.interest))
        sorted_non_deadline_tasks = sorted(tasks_without_deadline,
                                           key=lambda task: (task.importance * task.interest),
                                           reverse=True)
        for task in sorted_deadline_tasks:
            # print(f"filling_day={self.filling_day},\n task={task},\n wrk_hrs_bfr_ddln={self.get_act_wk_hrs_bfr_ddln(task.deadline)}")
            if self.get_act_wk_hrs_bfr_ddln(task.deadline) >= task.work_hours:
                self.add_task(task, task.work_hours)
                # print("Задача добавлена", end="\n\n")
            else:
                failed_tasks.add(task)
                # print("Задача не добавлена", end="\n\n")
        self.failed_tasks = failed_tasks
        for task in sorted_non_deadline_tasks:
            self.add_task(task, task.work_hours)

    def intrst_frst_imprt_close_ddln_sort(self):
        pass

    def interest_importance_sort(self):
        pass

    def validate_allocation(self):
        failed_tasks = set()
        for day in self.calendar:
            for task, work_hours in day.day_schedule.task_schedule.items():
                if task.deadline is not None and day.date >= task.deadline:
                    failed_tasks.add(task)
        self.failed_tasks = failed_tasks

    def print_failed_tasks_rus(self):
        if len(self.failed_tasks):
            print("Невыполненные задачи:")
            for task in self.failed_tasks:
                task.present_print_rus()

    def print_calendar_with_schedule(self):
        for day in self.calendar:
            if day.has_tasks():
                print(f"Day {day.date} with work_hours={day.work_hours} have tasks:")
                for task, work_hours in day.day_schedule.task_schedule.items():
                    output_attrs = ["name", "deadline", "interest", "importance"]
                    print(f"{work_hours} work hours at {to_str_instance(task, *output_attrs)}")
                print()

    def print_calendar_with_schedule_rus(self):
        print("Календарь с распределёнными задачами:")
        for day in self.calendar:
            if day.has_tasks():
                print(f"{((date_to_normal_str(day.date)))}:")
                for task, work_hours in day.day_schedule.task_schedule.items():
                    print(f'Делать задачу "{task.name}" на протяжении {work_hours} часов/а')
                print()

    @staticmethod
    def get_tasks_from_file(tasks_file_name):
        task_positional_attr_names = ["name"]
        tasks = read_class_instances(tasks_file_name, Task, task_positional_attr_names)
        return tasks

    @staticmethod
    def get_days_from_file(days_file_name):
        day_pos_attr_names = ["date"]
        manual_days = read_class_instances(days_file_name, Day, day_pos_attr_names)
        return manual_days

    @staticmethod
    def print_present_tasks_rus(tasks: [Task]):
        for task in tasks:
            task.present_print_rus()

    @staticmethod
    def dt_add_day(date: dt.date):
        return date + dt.timedelta(days=1)

    # @staticmethod
    # def smart_sort_v1(tasks, calendar) -> {int: int}:
    #     def calc_mustdo_coef(must_do: bool):
    #         return 1.5 if must_do else 1
    # 
    #     def create_id_hours_dict(local_tasks):
    #         return dict(map(lambda task_:
    #                         (
    #                             task_.task_id,
    #                             Planner.get_hours_before_deadline(start_date, task_.deadline, calendar),
    #                         ),
    #                         local_tasks))
    # 
    #     def substract_hours(id_hours_dict: {}, hrs: int):
    #         return dict(map(lambda pair: (pair[0], pair[1] - hrs),
    #                         id_hours_dict.items()))
    # 
    #     def chck_upcoming_ddlns(hrs_ddln_dct: {int: int}):
    #         if len(hrs_ddln_dct) == 0:
    #             return False, None
    #         first_iteration_flag = True
    #         first_id = 1
    #         for local_task_id_, hrs_ddln in hrs_ddln_dct.items():
    #             local_task = get_instance_by_attr(copy_tasks, "task_id", local_task_id_)
    #             if first_iteration_flag:
    #                 first_id = local_task_id_s
    #                 first_iteration_flag = False
    #             if local_task.work_hours >= hrs_ddln:
    #                 return True, local_task_id_
    #         nxt_hrs_ddln_dct = copy(hrs_ddln_dct)
    #         del nxt_hrs_ddln_dct[first_id]
    #         nxt_hrs_ddln_dct = substract_hours(nxt_hrs_ddln_dct, hrs_ddln_dct[first_id])
    #         return chck_upcoming_ddlns(nxt_hrs_ddln_dct)
    # 
    #     copy_tasks = deepcopy(tasks)
    #     start_date = Day.get_start_date()
    #     work_hours_list = []
    #     hours_to_last_deadline = Planner.get_hours_before_deadline(
    #         start_date, max(copy_tasks, key=lambda task_: task_.deadline).deadline, calendar)
    # 
    #     srt_hours_to_deadline_dict = sorted(copy_tasks, key=lambda task_: (
    #         Planner.get_hours_before_deadline(start_date, task_.deadline, calendar),
    #         1 - task_.must_do,
    #         1 / task_.sum_interest))
    #     srt_hours_to_deadline_dict = create_id_hours_dict(srt_hours_to_deadline_dict)
    # 
    #     srt_interest_dict = sorted(copy_tasks, key=lambda task_: (
    #         task_.interest,
    #         calc_mustdo_coef(task_.must_do) * 1
    #         / (Planner.get_hours_before_deadline(start_date, task_.deadline, calendar) + 1)
    #     ), reverse=True)
    #     srt_interest_dict = create_id_hours_dict(srt_interest_dict)
    # 
    #     failed_tasks = []
    # 
    #     while len(srt_hours_to_deadline_dict) > 0 and len(srt_interest_dict) > 0:
    #         upcoming_ddln_flag, task_id_ = chck_upcoming_ddlns(srt_hours_to_deadline_dict)
    #         while upcoming_ddln_flag:
    #             task_ = get_instance_by_attr(copy_tasks, "task_id", task_id_)
    #             if srt_hours_to_deadline_dict[task_id_] < task_.work_hours:
    #                 failed_tasks.append(task_id_)
    #                 del srt_hours_to_deadline_dict[task_id_]
    #                 del srt_interest_dict[task_id_]
    #                 upcoming_ddln_flag, task_id_ = chck_upcoming_ddlns(srt_hours_to_deadline_dict)
    #                 continue
    #             for wrk_hr in range(task_.work_hours):
    #                 work_hours_list.append(task_id_)
    #             srt_hours_to_deadline_dict = substract_hours(srt_hours_to_deadline_dict, task_.work_hours)
    #             srt_interest_dict = substract_hours(srt_interest_dict, task_.work_hours)
    #             task_.work_hours = 0
    #             del srt_hours_to_deadline_dict[task_id_]
    #             del srt_interest_dict[task_id_]
    #             upcoming_ddln_flag, task_id_ = chck_upcoming_ddlns(srt_hours_to_deadline_dict)
    # 
    #         try:
    #             interest_iterator = iter(srt_interest_dict)
    #             task_id_ = next(interest_iterator)
    #             task_ = get_instance_by_attr(copy_tasks, "task_id", task_id_)
    #             work_hours_list.append(task_id_)
    #             srt_hours_to_deadline_dict = substract_hours(srt_hours_to_deadline_dict, 1)
    #             srt_interest_dict = substract_hours(srt_interest_dict, 1)
    #             task_.work_hours -= 1
    #             if task_.work_hours == 0:
    #                 del srt_hours_to_deadline_dict[task_id_]
    #                 del srt_interest_dict[task_id_]
    #         except StopIteration:
    #             break
    # 
    #     return work_hours_list

    # @staticmethod
    # def smart_sort(tasks, calendar) -> {int: int}:
    #     def calc_mustdo_coef(must_do: bool):
    #         return 1.5 if must_do else 1
    # 
    #     def create_id_hours_dict(local_tasks):
    #         return dict(map(lambda task_:
    #                         (
    #                             task_.task_id,
    #                             Planner.get_hours_before_deadline(start_date, task_.deadline, calendar),
    #                         ),
    #                         local_tasks))
    # 
    #     def substract_hours(id_hours_dict: {}, hrs: int):
    #         return dict(map(lambda pair: (pair[0], pair[1] - hrs),
    #                         id_hours_dict.items()))
    # 
    #     def chck_upcoming_ddlns(hrs_ddln_dct: {int: int}):
    #         if len(hrs_ddln_dct) == 0:
    #             print("No upcmng ddln")
    #             return False, None
    #         print(hrs_ddln_dct)
    #         first_iteration_flag = True
    #         first_id = 1
    #         for local_task_id_, hrs_ddln in hrs_ddln_dct.items():
    #             local_task = get_instance_by_attr(copy_tasks, "task_id", local_task_id_)
    #             if first_iteration_flag:
    #                 first_id = local_task_id_
    #                 first_iteration_flag = False
    #             if local_task.work_hours >= hrs_ddln:
    #                 print(f"Upcmng ddln to {local_task_id_}")
    #                 return True, local_task_id_
    #         nxt_hrs_ddln_dct = copy(hrs_ddln_dct)
    #         del nxt_hrs_ddln_dct[first_id]
    #         nxt_hrs_ddln_dct = substract_hours(nxt_hrs_ddln_dct, hrs_ddln_dct[first_id])
    #         return chck_upcoming_ddlns(nxt_hrs_ddln_dct)
    # 
    #     copy_tasks = deepcopy(tasks)
    #     start_date = Day.get_start_date()
    #     work_hours_list = []
    #     hours_to_last_deadline = Planner.get_hours_before_deadline(
    #         start_date, max(copy_tasks, key=lambda task_: task_.deadline).deadline, calendar)
    # 
    #     srt_hours_to_deadline_dict = sorted(copy_tasks, key=lambda task_: (
    #         Planner.get_hours_before_deadline(start_date, task_.deadline, calendar),
    #         1 - task_.must_do,
    #         1 / task_.sum_interest))
    #     srt_hours_to_deadline_dict = create_id_hours_dict(srt_hours_to_deadline_dict)
    # 
    #     srt_interest_dict = sorted(copy_tasks, key=lambda task_: (
    #         task_.interest,
    #         calc_mustdo_coef(task_.must_do) * 1
    #         / (Planner.get_hours_before_deadline(start_date, task_.deadline, calendar) + 1)
    #     ), reverse=True)
    #     srt_interest_dict = create_id_hours_dict(srt_interest_dict)
    # 
    #     failed_tasks = []
    # 
    #     while len(srt_hours_to_deadline_dict) > 0 and len(srt_interest_dict) > 0:
    #         print("Start rec")
    #         upcoming_ddln_flag, task_id_ = chck_upcoming_ddlns(srt_hours_to_deadline_dict)
    #         while upcoming_ddln_flag:
    #             task_ = get_instance_by_attr(copy_tasks, "task_id", task_id_)
    #             if srt_hours_to_deadline_dict[task_id_] < task_.work_hours:
    #                 print(f"Failed in deadline {task_id_}")
    #                 failed_tasks.append(task_id_)
    #                 del srt_hours_to_deadline_dict[task_id_]
    #                 del srt_interest_dict[task_id_]
    #                 print("Start rec")
    #                 upcoming_ddln_flag, task_id_ = chck_upcoming_ddlns(srt_hours_to_deadline_dict)
    #                 continue
    #             for wrk_hr in range(task_.work_hours):
    #                 work_hours_list.append(task_id_)
    #             print(f"Completed in deadline {task_id_}")
    #             srt_hours_to_deadline_dict = substract_hours(srt_hours_to_deadline_dict, task_.work_hours)
    #             srt_interest_dict = substract_hours(srt_interest_dict, task_.work_hours)
    #             task_.work_hours = 0
    #             del srt_hours_to_deadline_dict[task_id_]
    #             del srt_interest_dict[task_id_]
    #             print("Start rec")
    #             upcoming_ddln_flag, task_id_ = chck_upcoming_ddlns(srt_hours_to_deadline_dict)
    #             print()
    # 
    #         try:
    #             interest_iterator = iter(srt_interest_dict)
    #             task_id_ = next(interest_iterator)
    #             task_ = get_instance_by_attr(copy_tasks, "task_id", task_id_)
    #             work_hours_list.append(task_id_)
    #             srt_hours_to_deadline_dict = substract_hours(srt_hours_to_deadline_dict, 1)
    #             srt_interest_dict = substract_hours(srt_interest_dict, 1)
    #             task_.work_hours -= 1
    #             if task_.work_hours == 0:
    #                 print(f"Completed in interest: {task_id_}")
    #                 del srt_hours_to_deadline_dict[task_id_]
    #                 del srt_interest_dict[task_id_]
    #                 print()
    #         except StopIteration:
    #             break
    # 
    #     return work_hours_list

    # def create_schedule(self):
    #     schedule = []
    #     start_date = self.start_date
    #     manual_days = self.manual_days
    #     tasks = self.tasks
    #     max_deadline_date = max(tasks, key=lambda t: t.deadline).deadline
    #     if len(manual_days) != 0:
    #         max_manual_days_date = max(filter(lambda d: not d.is_weekend(), manual_days),
    #                                    key=lambda d: d.date).date
    #         max_date = max(max_deadline_date, max_manual_days_date)
    #     else:
    #         max_date = max_deadline_date
    #
    #     mnl_days_dict = {d.date: d.work_hours for d in manual_days}
    #     while start_date <= max_date:
    #         day_work_hours = mnl_days_dict.get(start_date, self.dflt_day_wrk_hrs)
    #         schedule.append(Day(start_date, work_hours=day_work_hours))
    #         start_date += dt.timedelta(days=1)
    #     return schedule
