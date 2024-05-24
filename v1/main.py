from datetime import timedelta, datetime, date
from copy import deepcopy

from Task import Task, TooDistantDateError
from Day import Day


def create_calendar(tasks: [Task], spec_days: [Day]) -> [Day]:
    result = []
    # cur_date = date.today()
    cur_date = min(tasks, key=lambda t: t.deadline).deadline

    # while cur_date < max(filter(lambda d: not d.is_weekend(), spec_days),
    #                      key=lambda d: d.date).date:
    max_deadline_date = max(tasks, key=lambda t: t.deadline).deadline
    if len(spec_days) != 0:
        max_spec_days_date = max(filter(lambda d: not d.is_weekend(), spec_days),
                                 key=lambda d: d.date).date
        max_date = max(max_deadline_date, max_spec_days_date)
    else:
        max_date = max_deadline_date
    while cur_date < max_date:
        work_hours = 4
        spec_dates = dict(zip(map(lambda d: d.date, spec_days),
                              map(lambda d: d.work_hours, spec_days)))
        if cur_date in spec_dates.keys():
            work_hours = get_hours_from_timedelta(spec_dates[cur_date])
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


def read_class_objs(file_name: str, class_init, *pos_attr_names: []) -> []:
    result = []
    with open(file_name, 'r') as input_file:
        lines = input_file.readlines()
        for line in lines:
            attrs = line.strip().split(",")
            kw_attrs = dict()
            pos_attrs = []
            for i in range(len(attrs)):
                attr_str = attrs[i].strip()
                if i < len(pos_attr_names):
                    pos_attrs.append(attr_str)
                elif ":" in attr_str:
                    key, val = attr_str.split(":")
                    kw_attrs[key.strip()] = val.strip()
                elif "=" in attr_str:
                    key, val = attr_str.split("=")
                    kw_attrs[key.strip()] = val.strip()
            try:
                result.append(class_init(*pos_attrs, **kw_attrs))
            except TooDistantDateError as err:
                print(err)
    return result


def print_class_objs(input_list: [], *attrs):
    for elem in input_list:
        # print(attrs)
        for attr in attrs:
            # print(attr)
            result = getattr(elem, attr, "No attr")
            if isinstance(result, datetime):
                result = result.date()
            print(f"{attr}={result}", end=", ")
        print()


def get_hours_before_deadline(date_, deadline, calendar):
    days_before_deadline = list(filter(lambda d: date_ < d.date < deadline, calendar))
    return sum(map(lambda d: d.work_hours, days_before_deadline))


def get_hours_from_timedelta(td_obj: timedelta) -> int:
    return td_obj.seconds // 3600


def get_obj_by_attr(obj_list, attr_name, attr_value):
    for obj in obj_list:
        if getattr(obj, attr_name) == attr_value:
            return obj
    return None


if __name__ == "__main__":
    # types: better_first, better_last, mixed
    allocation_type = "better_first"
    weekends = []
    tasks_file_name = "../tasks2.txt"
    days_file_name = "../days2.txt"
    default_task_work_hours = 2
    default_day_work_hours = 4
    Task.set_default_work_hours(default_task_work_hours)
    Day.set_default_work_hours(default_day_work_hours)

    # get class lists
    task_pos_attr_names = ["name"]
    tasks = read_class_objs(tasks_file_name, Task, task_pos_attr_names)
    day_pos_attr_names = ["date"]
    spec_days = read_class_objs(days_file_name, Day, day_pos_attr_names)

    # print class lists
    print("Tasks:")
    task_attrs = ["name", "interest", "deadline", "work_hours"]
    print_class_objs(sorted(tasks, key=lambda tsk: tsk.interest, reverse=True),
                     *task_attrs)

    print("\nSpecial days:")
    day_attrs = ["date", "work_hours"]
    print_class_objs(sorted(spec_days, key=lambda d: d.date), *day_attrs)
    print()

    print("Calendar max_day:")
    calendar = create_calendar(tasks, spec_days)
    print(max(calendar, key=lambda d: d.date))
    print()

    print("Hours before deadline:")
    # task_name = "Java spring tutor project"
    # example_date = date.today()
    # example_deadline = next(filter(lambda t: t.name.lower() == task_name.lower(), tasks)).deadline
    example_date = date(day=1, month=1, year=2024)
    example_deadline = tasks[5].deadline
    print(get_hours_before_deadline(example_date, example_deadline, calendar))
    print()

    print("Guaranteed sort tasks:")
    sorted_tasks = guaranteed_sort(tasks)
    task_attrs = ["name", "deadline", "interest", "must_do"]
    print_class_objs(sorted_tasks, *task_attrs)
    print()

    print("Calendar with guaranteed sort tasks:")
    allocated_calendar = allocate_tasks(sorted_tasks, calendar)
    print(allocated_calendar)
