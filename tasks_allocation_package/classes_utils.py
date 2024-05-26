from datetime import timedelta
from copy import deepcopy, copy

from .classes import Task, Day
from .utils import get_instance_by_attr, to_str_instance


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
        work_hours = Day.get_default_work_hours()
        spec_dates = dict(zip(map(lambda d: d.date, spec_days),
                              map(lambda d: d.work_hours, spec_days)))
        if cur_date in spec_dates.keys():
            work_hours = spec_dates[cur_date]
        result.append(Day(cur_date, work_hours=work_hours))
        cur_date += timedelta(days=1)
    return result


def get_hours_before_deadline(date_, deadline, calendar):
    days_before_deadline = list(filter(lambda d: date_ < d.date < deadline, calendar))
    return sum(map(lambda d: d.work_hours, days_before_deadline))


def deadline_mustdo_sort(tasks):
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


def smart_sort(tasks, calendar):
    def calc_mustdo_coef(must_do: bool):
        return 1.5 if must_do else 1

    def chck_upcoming_ddlns(hrs_ddln_dct: dict):
        if len(hrs_ddln_dct) == 0:
            return False, None
        first_iteration_flag = True
        first_id = 1
        for local_task_id_, hrs_ddln in hrs_ddln_dct.items():
            local_task = get_instance_by_attr(tasks, "task_id", local_task_id_)
            if first_iteration_flag:
                first_id = local_task_id_
                first_iteration_flag = False
            if local_task.work_hours == hrs_ddln:
                return True, local_task.task_id
        nxt_hrs_ddln_dct = copy(hrs_ddln_dct)
        del nxt_hrs_ddln_dct[first_id]
        return chck_upcoming_ddlns(dict(map(lambda pair: (pair[0], pair[1] - hrs_ddln_dct[0]), nxt_hrs_ddln_dct)))

    copy_tasks = deepcopy(tasks)
    actual_date = Day.get_actual_date()
    work_hours_list = []
    hours_to_last_deadline = get_hours_before_deadline(
        actual_date, max(tasks, key=lambda task_: task_.deadline), calendar)

    srt_hours_to_deadline_dict = sorted(copy_tasks, key=lambda task_: (
        get_hours_before_deadline(actual_date, task_.deadline, calendar),
        1 - task_.must_do,
        1 / task_.sum_interest))
    # srt_hours_to_deadline_dict = map(lambda task_: task_.task_id, srt_hours_to_deadline_dict)
    # srt_hours_to_deadline_dict = dict(zip(
    #     srt_hours_to_deadline_dict,
    #     map(lambda task_id_:
    #         get_hours_before_deadline(actual_date, get_instance_by_attr(tasks, "task_id", task_id_).deadline, calendar),
    #         srt_hours_to_deadline_dict)
    # ))
    srt_hours_to_deadline_dict = dict(map(lambda task_:
                                          (
                                              task_.task_id,
                                              get_hours_before_deadline(actual_date, task_.deadline, calendar)
                                          ),
                                          srt_hours_to_deadline_dict))

    # srt_sum_interest_dict = sorted(copy_tasks, key=lambda task_: (
    #     task_.sum_interest, task_.must_do, 1 / get_hours_before_deadline(actual_date, task_.deadline, calendar)),
    #                                reverse=True)
    # srt_sum_interest_dict = map(lambda task_: task_.task_id, srt_sum_interest_dict)
    # srt_sum_interest_dict = dict(zip(srt_sum_interest_dict, map(lambda task_: [task_.sum_interest, task_.work_hours], tasks)))

    srt_interest_dict = sorted(copy_tasks, key=lambda task_: (
        task_.interest,
        calc_mustdo_coef(task_.must_do) * 1
        / get_hours_before_deadline(actual_date, task_.deadline, calendar)
    ), reverse=True)
    srt_interest_dict = dict(map(lambda task_:
                                 (
                                     task_.task_id,
                                     get_hours_before_deadline(actual_date, task_.deadline, calendar)
                                 ),
                                 srt_interest_dict))
    # srt_interest_dict = map(lambda task_: task_.task_id, srt_interest_dict)
    # srt_interest_dict = dict(zip(
    #     srt_interest_dict,
    #     map(lambda task_: [task_.interest, task_.work_hours], srt_interest_dict)
    # ))

    while len(srt_hours_to_deadline_dict) > 0 and len(srt_interest_dict) > 0:
        upcoming_ddln_flag, task_id_ = chck_upcoming_ddlns(srt_hours_to_deadline_dict)
        while upcoming_ddln_flag:
            task_ = get_instance_by_attr(tasks, "task_id", task_id_)
            for wrk_hr in range(task_.work_hours):
                work_hours_list.append(task_id_)
            del srt_hours_to_deadline_dict[task_id_]
            del srt_interest_dict[task_id_]
            upcoming_ddln_flag, task_id_ = chck_upcoming_ddlns(srt_hours_to_deadline_dict)

        interest_iterator = iter(srt_interest_dict)
        task_id_ = next(interest_iterator)
        work_hours_list.append(task_id_)
        srt_interest_dict[task_id_] -= 1
        srt_hours_to_deadline_dict[task_id_] -= 1
        if srt_interest_dict[task_id_] == 0:
            del srt_hours_to_deadline_dict[task_id_]
            del srt_interest_dict[task_id_]

    return work_hours_list

def allocate_work_hours(work_hours_list, calendar):
    new_calendar = deepcopy(calendar)
    for work_hour in work_hours_list:
        pass


def allocate_tasks(tasks, calendar):
    copy_tasks = deepcopy(tasks)
    new_calendar = deepcopy(calendar)

    try:
        tasks_iterator = iter(copy_tasks)
        task_ = next(tasks_iterator)
        task_work_hours = task_.work_hours

        calendar_iterator = iter(new_calendar)
        day_ = next(calendar_iterator)
        while day_.is_weekend():
            day_ = next(calendar_iterator)
        day_work_hours = day_.work_hours

        task_schedule = day_.task_schedule
        while True:
            if day_work_hours >= task_work_hours:
                task_schedule[task_.task_id] = task_work_hours
                day_work_hours -= task_work_hours
                task_ = next(tasks_iterator)
                # print("Next task")
                task_work_hours = task_.work_hours
                if day_work_hours == 0:
                    day_ = next(calendar_iterator)
                    # print("Next day")
                    day_work_hours = day_.work_hours
                    task_schedule = day_.task_schedule
            else:
                task_schedule[task_.task_id] = day_work_hours
                task_work_hours -= day_work_hours
                day_ = next(calendar_iterator)
                # print("Next day")
                day_work_hours = day_.work_hours
                task_schedule = day_.task_schedule
    except StopIteration:
        return new_calendar


def validate_allocation(calendar, tasks):
    failed_task_ids = set()
    for day_ in calendar:
        task_schedule = day_.task_schedule
        for task_id_, schedule_task_hours in task_schedule.items():
            task_ = get_instance_by_attr(tasks, "task_id", task_id_)
            if day_.date >= task_.deadline:
                failed_task_ids.add(task_id_)
    return failed_task_ids


"""
checking failed tasks for must_do
"""


def contains_must_do(failed_tasks):
    for task_ in failed_tasks:
        if task_.must_do:
            return True
    return False


def print_calendar_with_schedule(calendar, tasks):
    for day_ in calendar:
        if day_.has_tasks():
            print(f"Day {day_.date} with work_hours={day_.work_hours} have tasks:")
            for task_id, schedule_task_hours in day_.task_schedule.items():
                task_ = get_instance_by_attr(tasks, "task_id", task_id)
                output_attrs = ["name", "deadline", "interest", "must_do"]
                print(f"{schedule_task_hours} work hours at {to_str_instance(task_, *output_attrs)}")
            print()
