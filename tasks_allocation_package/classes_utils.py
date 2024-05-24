from datetime import timedelta
from copy import deepcopy

from .classes import Task, Day


def create_calendar(tasks: [Task], spec_days: [Day]) -> [Day]:
    result = []
    # cur_date = date.today()
    min_deadline_date = min(tasks, key=lambda t: t.deadline).deadline
    # while cur_date < max(filter(lambda d: not d.is_weekend(), spec_days),
    #                      key=lambda d: d.date).date:
    max_deadline_date = max(tasks, key=lambda t: t.deadline).deadline
    if len(spec_days) != 0:
        max_spec_days_date = max(filter(lambda d: not d.is_weekend(), spec_days),
                                 key=lambda d: d.date).date
        min_spec_days_date = min(spec_days, key=lambda d: d.date).date
        max_date = max(max_deadline_date, max_spec_days_date)
        cur_date = min(min_deadline_date, min_spec_days_date)
    else:
        max_date = max_deadline_date
        cur_date = min_deadline_date
    while cur_date < max_date:
        work_hours = 4
        spec_dates = dict(zip(map(lambda d: d.date, spec_days),
                              map(lambda d: d.work_hours, spec_days)))
        if cur_date in spec_dates.keys():
            work_hours = spec_dates[cur_date]
        result.append(Day(cur_date, work_hours=work_hours))
        cur_date += timedelta(days=1)
    return result


def guaranteed_sort(tasks):
    copy_tasks = deepcopy(tasks)
    new_tasks = []
    deadlines_set = sorted(set(map(lambda task_: task_.deadline, copy_tasks)))
    for deadline in deadlines_set:
        tasks_by_deadline = list(filter(lambda task_: task_.deadline == deadline, copy_tasks))
        for flag in (True, False):
            must_do_tasks = list(filter(lambda task_: task_.must_do == flag, tasks_by_deadline))
            must_do_tasks.sort(key=lambda task_: task_.interest, reverse=True)
            new_tasks.extend(must_do_tasks)
    return new_tasks
    # task_attrs = ["name", "deadline", "interest", "must_do"]
    # print_class_objs(new_tasks, *task_attrs)


def allocate_tasks(tasks, calendar):
    copy_tasks = deepcopy(tasks)
    new_calendar = deepcopy(calendar)
    calendar_iterator = iter(new_calendar)
    day_ = next(calendar_iterator)
    day_work_hours = day_.work_hours
    for task_ in tasks:
        while day_.is_weekend():
            day_ = next(calendar_iterator)
            day_work_hours = day_.work_hours
        task_work_hours = task_.work_hours
        task_schedule = day_.task_schedule
        while task_work_hours != 0:
            if task_work_hours <= day_work_hours:
                task_schedule[task_.task_id] = task_work_hours
                day_work_hours -= task_work_hours
                task_work_hours = 0
            else:
                task_schedule[task_.task_id] = task_work_hours
                task_work_hours -= day_work_hours
                day_work_hours = 0
    return new_calendar


def validate_allocation(tasks, calendar):
    copy_tasks = deepcopy(tasks)
    cur_date = min(tasks, key=lambda t: t.deadline).deadline

    cur_task = copy_tasks[0]
    for day_ in calendar:
        pass
    return True
